"""
Módulo de gestión de base de datos para el sistema POS
Maneja SQLite con SQLAlchemy ORM
"""

import sqlite3
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

# Tabla de activación de licencias
class License(db.Model):
    __tablename__ = 'licenses'

    id = db.Column(db.Integer, primary_key=True)
    license_key = db.Column(db.String(100), unique=True, nullable=False)
    license_type = db.Column(db.String(50), nullable=False)  # TRIAL, LIFETIME, MOBILE
    device_id = db.Column(db.String(100), unique=True)
    activated_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    max_devices = db.Column(db.Integer, default=1)
    registered_devices = db.Column(db.Integer, default=0)


# Tabla de negocios
class Business(db.Model):
    __tablename__ = 'businesses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    owner_username = db.Column(db.String(100), unique=True, nullable=False)
    owner_password = db.Column(db.String(10), nullable=False)  # 4 dígitos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relación con productos y ventas
    products = db.relationship('Product', backref='business', lazy=True, cascade='all, delete-orphan')
    sales = db.relationship('Sale', backref='business', lazy=True, cascade='all, delete-orphan')
    shifts = db.relationship('Shift', backref='business', lazy=True, cascade='all, delete-orphan')


# Tabla de productos
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    barcode = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False, unique=True)
    product_type = db.Column(db.String(50), default='pieza')  # pieza, kilo, paquete
    public_price = db.Column(db.Float, nullable=False)
    supplier_price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    min_stock_alert = db.Column(db.Integer, default=3)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_profit_margin(self):
        """Calcula el margen de ganancia"""
        if self.supplier_price > 0:
            return ((self.public_price - self.supplier_price) / self.supplier_price) * 100
        return 0


# Tabla de turnos
class Shift(db.Model):
    __tablename__ = 'shifts'

    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    shift_number = db.Column(db.Integer, nullable=False)  # 1 o 2
    initial_amount = db.Column(db.Float, nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime, nullable=True)
    is_closed = db.Column(db.Boolean, default=False)
    closed_by = db.Column(db.String(100), nullable=True)


# Tabla de ventas
class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    shift_id = db.Column(db.Integer, db.ForeignKey('shifts.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # efectivo, tarjeta, transferencia
    cash_received = db.Column(db.Float, nullable=True)
    change = db.Column(db.Float, default=0)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)
    sale_time = db.Column(db.Time, default=datetime.utcnow().time)

    # Relación con detalles de venta
    items = db.relationship('SaleItem', backref='sale', lazy=True, cascade='all, delete-orphan')

    # Relación con turno
    shift = db.relationship('Shift', backref='sales')


# Tabla de detalles de venta
class SaleItem(db.Model):
    __tablename__ = 'sale_items'

    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    # Relación con producto
    product = db.relationship('Product', backref='sale_items')


# Tabla de dispositivos registrados
class RegisteredDevice(db.Model):
    __tablename__ = 'registered_devices'

    id = db.Column(db.Integer, primary_key=True)
    license_id = db.Column(db.Integer, db.ForeignKey('licenses.id'), nullable=False)
    device_id = db.Column(db.String(100), unique=True, nullable=False)
    device_type = db.Column(db.String(50), default='desktop')  # desktop, mobile, tablet
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    license = db.relationship('License', backref='devices')


def init_db(app):
    """Inicializa la base de datos"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("Base de datos inicializada correctamente")


def create_backup(db_path, backup_dir='backups'):
    """
    Crea un respaldo binario de la base de datos SQLite
    """
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"backup_pos_{timestamp}.db"
    backup_path = os.path.join(backup_dir, backup_filename)

    try:
        # Conectar a la base de datos original
        source_conn = sqlite3.connect(db_path)
        # Conectar a la base de datos de respaldo
        backup_conn = sqlite3.connect(backup_path)

        # Usar el método backup de SQLite
        source_conn.backup(backup_conn)

        # Cerrar conexiones
        backup_conn.close()
        source_conn.close()

        print(f"Respaldo creado exitosamente: {backup_path}")
        return backup_path

    except Exception as e:
        print(f"Error al crear respaldo: {e}")
        return None


def create_sql_backup(db_path, backup_dir='backups'):
    """
    Crea un respaldo SQL (dump) de la base de datos
    """
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"backup_pos_{timestamp}.sql"
    backup_path = os.path.join(backup_dir, backup_filename)

    try:
        conn = sqlite3.connect(db_path)

        with open(backup_path, 'w', encoding='utf-8') as f:
            for line in conn.iterdump():
                f.write(f'{line}\n')

        conn.close()

        print(f"Respaldo SQL creado exitosamente: {backup_path}")
        return backup_path

    except Exception as e:
        print(f"Error al crear respaldo SQL: {e}")
        return None


def get_low_stock_products(business_id, min_stock=3):
    """
    Obtiene productos con stock bajo
    """
    low_stock = Product.query.filter(
        Product.business_id == business_id,
        Product.stock <= min_stock
    ).all()
    return low_stock
