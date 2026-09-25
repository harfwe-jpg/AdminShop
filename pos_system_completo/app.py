"""
Sistema de Punto de Venta (POS) - Aplicación Principal
Flask Backend con gestión de licencias, inventario y ventas
"""

import os
import socket
import webbrowser
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash

# Importaciones de la base de datos y generador de PDF
from database import db, License, Business, Product, Shift, Sale, SaleItem, RegisteredDevice, init_db, create_backup, create_sql_backup, get_low_stock_products
from pdf_generator import generate_sale_receipt_pdf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-pos-2026-xoxtl'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pos_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar base de datos
init_db(app)

# Claves de licencia válidas
VALID_LICENSES = {
    'TRIAL': 'MEM-1M-2026-XOXTL-79F4K',
    'LIFETIME': 'LIFETIME-VIP-2026-XOXTL-99Z8X',
    'MOBILE': 'MOB-TAB-ACC-2026-XOXTL-5D2W9'
}

# ==================== DECORADORES ====================

def license_required(f):
    """Decorador para verificar que hay una licencia activa"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'license_activated' not in session or not session['license_activated']:
            flash('Primero debes activar tu licencia', 'warning')
            return redirect(url_for('activation'))
        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    """Decorador para verificar que el usuario ha iniciado sesión"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def shift_required(f):
    """Decorador para verificar que hay un turno activo"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'shift_id' not in session:
            flash('Debes iniciar un turno para acceder', 'warning')
            return redirect(url_for('shift_start'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== RUTAS DE ACTIVACIÓN ====================

@app.route('/')
def index():
    """Página principal - Redirige según el estado del sistema"""
    if 'license_activated' in session and session['license_activated']:
        if 'user_id' not in session:
            return redirect(url_for('login'))
        elif 'shift_id' not in session:
            return redirect(url_for('shift_start'))
        else:
            return redirect(url_for('dashboard'))

    business_count = Business.query.count()
    if business_count > 0 and 'license_activated' not in session:
        return redirect(url_for('login'))

    return redirect(url_for('activation'))


@app.route('/activation', methods=['GET', 'POST'])
def activation():
    """Página de activación de licencia"""
    if request.method == 'POST':
        license_key = request.form.get('license_key', '').strip()

        license_type = None
        max_devices = 1

        if license_key == VALID_LICENSES['TRIAL']:
            license_type = 'TRIAL'
            max_devices = 1
        elif license_key == VALID_LICENSES['LIFETIME']:
            license_type = 'LIFETIME'
            max_devices = 1
        elif license_key == VALID_LICENSES['MOBILE']:
            license_type = 'MOBILE'
            max_devices = 3
        else:
            flash('Clave de activación inválida', 'error')
            return render_template('activation.html')

        device_id = request.remote_addr + '-' + str(datetime.now().timestamp())

        new_license = License(
            license_key=license_key,
            license_type=license_type,
            device_id=device_id,
            expires_at=datetime.now() + timedelta(days=30) if license_type == 'TRIAL' else None,
            max_devices=max_devices,
            registered_devices=1
        )

        db.session.add(new_license)
        db.session.commit()

        device_type = 'mobile' if license_type == 'MOBILE' else 'desktop'
        new_device = RegisteredDevice(
            license_id=new_license.id,
            device_id=device_id,
            device_type=device_type
        )
        db.session.add(new_device)
        db.session.commit()

        session['license_activated'] = True
        session['license_type'] = license_type
        session['license_id'] = new_license.id
        session['device_id'] = device_id

        flash('Licencia activada exitosamente', 'success')
        return redirect(url_for('welcome'))

    return render_template('activation.html')


@app.route('/welcome')
def welcome():
    """Página de bienvenida con información de la licencia"""
    if 'license_activated' not in session:
        return redirect(url_for('activation'))

    license_type = session.get('license_type', 'TRIAL')
    return render_template('welcome.html', license_type=license_type)


# ==================== RUTAS DE REGISTRO ====================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registro del negocio y dueño"""
    if 'license_activated' not in session:
        return redirect(url_for('activation'))

    if request.method == 'POST':
        business_name = request.form.get('business_name', '').strip()
        owner_username = request.form.get('owner_username', '').strip()
        owner_password = request.form.get('owner_password', '').strip()

        if not business_name or not owner_username or not owner_password:
            flash('Todos los campos son obligatorios', 'error')
            return render_template('register.html')

        if not owner_password.isdigit() or len(owner_password) != 4:
            flash('La contraseña debe ser de 4 dígitos numéricos', 'error')
            return render_template('register.html')

        existing = Business.query.filter_by(owner_username=owner_username).first()
        if existing:
            flash('Este nombre de usuario ya está registrado', 'error')
            return render_template('register.html')

        new_business = Business(
            name=business_name,
            owner_username=owner_username,
            owner_password=owner_password
        )

        db.session.add(new_business)
        db.session.commit()

        create_backup('instance/pos_system.db', 'backups')
        create_sql_backup('instance/pos_system.db', 'backups')

        flash('Negocio registrado exitosamente. Ahora inicia sesión', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# ==================== RUTAS DE AUTENTICACIÓN ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Inicio de sesión del dueño"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        business = Business.query.filter_by(owner_username=username, owner_password=password).first()

        if business:
            session['user_id'] = business.id
            session['username'] = business.owner_username
            session['business_name'] = business.name
            session['shift_open'] = False

            flash(f'Bienvenido, {business.owner_username}', 'success')
            return redirect(url_for('shift_start'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))


# ==================== RUTAS DE TURNOS ====================

@app.route('/shift/start', methods=['GET', 'POST'])
@login_required
def shift_start():
    """Iniciar turno"""
    if request.method == 'POST':
        shift_number = int(request.form.get('shift_number', 1))
        initial_amount = float(request.form.get('initial_amount', 0))

        new_shift = Shift(
            business_id=session['user_id'],
            shift_number=shift_number,
            initial_amount=initial_amount
        )

        db.session.add(new_shift)
        db.session.commit()

        session['shift_id'] = new_shift.id
        session['shift_number'] = shift_number
        session['shift_open'] = True

        flash(f'Turno {shift_number} iniciado con ${initial_amount:.2f}', 'success')
        return redirect(url_for('dashboard'))

    if 'shift_id' in session:
        return redirect(url_for('dashboard'))

    return render_template('shift.html')


@app.route('/shift/close', methods=['POST'])
@login_required
def shift_close():
    """Cerrar turno con verificación de contraseña"""
    password = request.form.get('password', '')
    business = Business.query.get(session['user_id'])

    if not business or business.owner_password != password:
        flash('Contraseña incorrecta', 'error')
        return redirect(url_for('dashboard'))

    shift = Shift.query.get(session['shift_id'])
    if shift:
        shift.is_closed = True
        shift.closed_at = datetime.now()
        shift.closed_by = business.owner_username
        db.session.commit()

        create_backup('instance/pos_system.db', 'backups')

        session.pop('shift_id', None)
        session.pop('shift_number', None)
        session['shift_open'] = False

        flash('Turno cerrado exitosamente', 'success')

    return redirect(url_for('shift_start'))


# ==================== RUTAS PRINCIPALES ====================

@app.route('/dashboard')
@login_required
@shift_required
def dashboard():
    """Panel principal"""
    low_stock = get_low_stock_products(session['user_id'], min_stock=3)
    current_sales = Sale.query.filter_by(shift_id=session['shift_id']).all()
    total_sales = sum(sale.total_amount for sale in current_sales)

    return render_template('dashboard.html', 
                           low_stock=low_stock, 
                           total_sales=total_sales,
                           sales_count=len(current_sales))


@app.route('/sales')
@login_required
@shift_required
def sales():
    """Punto de venta"""
    return render_template('sales.html')


@app.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    """Gestión de productos"""
    if request.method == 'POST':
        barcode = request.form.get('barcode', '').strip()
        name = request.form.get('name', '').strip()
        product_type = request.form.get('product_type', 'pieza')
        public_price = float(request.form.get('public_price', 0))
        supplier_price = float(request.form.get('supplier_price', 0))
        stock = int(request.form.get('stock', 0))
        product_id = request.form.get('product_id')

        if product_id:
            product = Product.query.get(int(product_id))
            if product:
                if request.form.get('action') == 'delete':
                    db.session.delete(product)
                    flash('Producto eliminado', 'success')
                else:
                    product.barcode = barcode
                    product.name = name
                    product.product_type = product_type
                    product.public_price = public_price
                    product.supplier_price = supplier_price
                    product.stock = stock
                    flash('Producto actualizado', 'success')
        else:
            existing = Product.query.filter_by(name=name, business_id=session['user_id']).first()
            if existing:
                flash('Ya existe un producto con este nombre', 'error')
            else:
                new_product = Product(
                    business_id=session['user_id'],
                    barcode=barcode,
                    name=name,
                    product_type=product_type,
                    public_price=public_price,
                    supplier_price=supplier_price,
                    stock=stock
                )
                db.session.add(new_product)
                flash('Producto agregado', 'success')

        db.session.commit()
        return redirect(url_for('products'))

    products_list = Product.query.filter_by(business_id=session['user_id']).all()
    return render_template('products.html', products=products_list)


@app.route('/log')
@login_required
def log():
    """Bitácora de ventas del día"""
    today = datetime.now().date()
    sales = Sale.query.join(Shift).filter(
        Sale.business_id == session['user_id'],
        db.func.date(Sale.sale_date) == today
    ).order_by(Sale.sale_date.desc()).all()

    return render_template('log.html', sales=sales)


# ==================== API ENDPOINTS ====================

@app.route('/api/products/search')
@login_required
def api_search_products():
    """Buscar productos por nombre o código de barras"""
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify([])

    products = Product.query.filter(
        Product.business_id == session['user_id'],
        db.or_(
            Product.name.ilike(f'%{query}%'),
            Product.barcode.ilike(f'%{query}%')
        )
    ).limit(20).all()

    return jsonify([{
        'id': p.id,
        'name': p.name,
        'barcode': p.barcode,
        'price': p.public_price,
        'stock': p.stock,
        'type': p.product_type
    } for p in products])


@app.route('/api/products/<int:product_id>')
@login_required
def api_get_product(product_id):
    """Obtener información de un producto"""
    product = Product.query.filter_by(
        id=product_id,
        business_id=session['user_id']
    ).first_or_404()

    return jsonify({
        'id': product.id,
        'name': product.name,
        'barcode': product.barcode,
        'public_price': product.public_price,
        'supplier_price': product.supplier_price,
        'stock': product.stock,
        'product_type': product.product_type,
        'profit_margin': product.get_profit_margin()
    })


@app.route('/api/sales', methods=['POST'])
@login_required
@shift_required
def api_create_sale():
    """Registrar una nueva venta"""
    data = request.get_json()

    items = data.get('items', [])
    payment_method = data.get('payment_method', 'efectivo')
    cash_received = data.get('cash_received', 0)

    if not items:
        return jsonify({'error': 'No hay productos en la venta'}), 400

    total = sum(item['subtotal'] for item in items)
    change = cash_received - total if payment_method == 'efectivo' else 0

    new_sale = Sale(
        business_id=session['user_id'],
        shift_id=session['shift_id'],
        total_amount=total,
        payment_method=payment_method,
        cash_received=cash_received if payment_method == 'efectivo' else None,
        change=change
    )

    db.session.add(new_sale)
    db.session.flush()

    for item in items:
        product = Product.query.get(item['product_id'])
        if product and product.stock >= item['quantity']:
            sale_item = SaleItem(
                sale_id=new_sale.id,
                product_id=product.id,
                quantity=item['quantity'],
                unit_price=product.public_price,
                subtotal=item['subtotal']
            )
            db.session.add(sale_item)

            product.stock -= int(item['quantity']) if item['quantity'] == int(item['quantity']) else item['quantity']

    db.session.commit()

    return jsonify({
        'success': True,
        'sale_id': new_sale.id,
        'total': total,
        'change': change
    })


@app.route('/api/backup', methods=['POST'])
@login_required
def api_create_backup():
    """Crear respaldo manual de la base de datos"""
    backup_path = create_backup('instance/pos_system.db', 'backups')
    sql_path = create_sql_backup('instance/pos_system.db', 'backups')

    if backup_path and sql_path:
        return jsonify({'success': True, 'message': 'Respaldo creado'})
    return jsonify({'success': False, 'message': 'Error al crear respaldo'}), 500


@app.route('/api/sales/<int:sale_id>/pdf')
@login_required
def download_sale_pdf(sale_id):
    """Genera y descarga el PDF de un ticket de venta"""
    pdf_path = generate_sale_receipt_pdf(sale_id)
    if pdf_path and os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True, download_name=f"ticket_{sale_id}.pdf")
    return jsonify({'error': 'No se pudo generar el PDF'}), 404


# ==================== INICIO DEL SERVIDOR ====================

def get_local_ip():
    """Obtener IP local para abrir el navegador"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


if __name__ == '__main__':
    if not os.path.exists('backups'):
        os.makedirs('backups')

    local_ip = get_local_ip()
    port = 5000

    print(f"\n{'='*50}")
    print(f"Sistema POS iniciado")
    print(f"{'='*50}")
    print(f"Accede en: http://{local_ip}:{port}")
    print(f"{'='*50}\n")

    def open_browser():
        import time
        time.sleep(2)
        webbrowser.open(f'http://{local_ip}:{port}')

    import threading
    threading.Thread(target=open_browser, daemon=True).start()

    app.run(host='0.0.0.0', port=port, debug=True)
