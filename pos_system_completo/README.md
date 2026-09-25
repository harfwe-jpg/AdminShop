# Sistema de Punto de Venta (POS) - 2026

Sistema administrativo de punto de venta con gestión de inventario, ventas, turnos y licencias. Desarrollado con Flask (Python) y frontend responsive en HTML/CSS/JS.

## 🚀 Características Principales

- **Sistema de Licencias**: Activación con claves de prueba (1 mes), permanente y móvil/tablet
- **Gestión de Negocio**: Registro con nombre, usuario y contraseña de 4 dígitos
- **Control de Turnos**: Turnos 1 y 2 con cantidad inicial de caja
- **Punto de Venta**: 
  - Búsqueda por nombre o código de barras
  - Calculadora con billetes ($20, $50, $100, $200, $500)
  - Métodos de pago: efectivo, tarjeta, transferencia
  - Cálculo automático de cambio
- **Inventario de Productos**:
  - Tipos: pieza, kilo, paquete
  - Control de stock con alertas (≤3 piezas)
  - Margen de ganancia automático
  - No duplicación de nombres
- **Bitácora de Ventas**: Registro con hora y fecha
- **Respaldos Automáticos**: Copias de seguridad .db y .sql
- **Responsive**: Funciona en desktop, celular y tablet
- **Multi-dispositivo**: Hasta 3 dispositivos con licencia móvil

## 📁 Estructura del Proyecto

```
pos_system/
├── app.py                 # Aplicación Flask principal
├── database.py            # Modelos y utilidades de base de datos
├── requirements.txt       # Dependencias de Python
├── README.md             # Este archivo
├── static/
│   ├── css/
│   │   └── styles.css    # Estilos responsive
│   └── js/
│       └── main.js       # Lógica del frontend
├── templates/
│   ├── activation.html   # Activación de licencia
│   ├── welcome.html      # Bienvenida
│   ├── register.html     # Registro de negocio
│   ├── login.html        # Inicio de sesión
│   ├── shift.html        # Inicio de turno
│   ├── dashboard.html    # Panel principal
│   ├── sales.html        # Punto de venta
│   ├── products.html     # Gestión de productos
│   └── log.html          # Bitácora
└── backups/              # Respaldos de base de datos
```

## 🔑 Claves de Activación

| Tipo | Clave | Dispositivos | Duración |
|------|-------|--------------|----------|
| Prueba | `MEM-1M-2026-XOXTL-79F4K` | 1 | 1 mes |
| Permanente | `LIFETIME-VIP-2026-XOXTL-99Z8X` | 1 | Ilimitada |
| Móvil/Tablet | `MOB-TAB-ACC-2026-XOXTL-5D2W9` | 3 | Según contrato |

## 📦 Instalación

### 1. Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 2. Instalación de Dependencias

```bash
cd pos_system
pip install -r requirements.txt
```

### 3. Ejecutar la Aplicación

```bash
python app.py
```

El servidor se iniciará automáticamente y abrirá el navegador en:
- **URL**: `http://127.0.0.1:5000` o `http://[tu-ip-local]:5000`

## 🎯 Flujo de Uso

### Primer Uso

1. **Activar Licencia**: Ingresa una clave de activación
2. **Leer Bienvenida**: Revisa los términos de tu licencia
3. **Registrar Negocio**:
   - Nombre del negocio (aparece en reportes)
   - Usuario (nombre del dueño)
   - Contraseña (4 dígitos numéricos)
4. **Iniciar Sesión**: Con usuario y contraseña
5. **Iniciar Turno**: Selecciona turno (1 o 2) e ingresa cantidad inicial
6. **¡Listo!**: Comienza a vender

### Operaciones Diarias

1. **Ventas**:
   - Busca productos por nombre o código de barras
   - Agrega al carrito
   - Selecciona método de pago
   - Ingresa cantidad recibida (efectivo)
   - Finaliza venta

2. **Productos**:
   - Agrega nuevos productos
   - Modifica stock (confirmación requerida)
   - Visualiza márgenes de ganancia
   - Crea respaldos manuales

3. **Bitácora**:
   - Consulta ventas del día
   - Exporta reportes (PDF)

4. **Cierre de Turno**:
   - Ingresa contraseña del dueño
   - Genera reporte PDF
   - Limpia bitácora del turno

## 🗄️ Base de Datos

La aplicación usa SQLite con SQLAlchemy ORM. Los archivos se generan automáticamente:

- **Principal**: `instance/pos_system.db`
- **Respaldos**: `backups/backup_pos_YYYYMMDD_HHMMSS.db`
- **SQL Dump**: `backups/backup_pos_YYYYMMDD_HHMMSS.sql`

### Tablas Principales

- `licenses`: Licencias activadas
- `businesses`: Negocios registrados
- `products`: Inventario de productos
- `shifts`: Turnos de venta
- `sales`: Ventas realizadas
- `sale_items`: Detalles de cada venta
- `registered_devices`: Dispositivos registrados

## 📱 Responsive Design

La interfaz está optimizada para:

- **Desktop**: Navegación completa con todas las funciones
- **Tablet**: Diseño adaptado con menú colapsable
- **Móvil**: Interfaz touch-friendly con botones grandes

### Licencia Móvil

La clave `MOB-TAB-ACC-2026-XOXTL-5D2W9` permite:
- Registrar hasta 3 dispositivos
- Sincronización independiente por dispositivo
- Ideal para equipos de ventas móviles

## 🔒 Seguridad

- Contraseña de 4 dígitos para el dueño
- Sesión persistente hasta cierre manual
- Verificación de contraseña para cerrar turno
- Límite de dispositivos por licencia
- Respaldos automáticos de base de datos

## 🛠️ Personalización

### Cambiar Claves de Licencia

Edita `app.py` y modifica el diccionario `VALID_LICENSES`:

```python
VALID_LICENSES = {
    'TRIAL': 'TU-CLAVE-TRIAL',
    'LIFETIME': 'TU-CLAVE-PERMANENTE',
    'MOBILE': 'TU-CLAVE-MOVIL'
}
```

### Modificar Stock Mínimo de Alerta

En `database.py`, cambia el valor por defecto:

```python
min_stock_alert = db.Column(db.Integer, default=3)  # Cambia 3 por tu valor
```

### Cambiar Puerto del Servidor

En `app.py`, modifica:

```python
app.run(host='0.0.0.0', port=5000, debug=True)  # Cambia 5000 por otro puerto
```

## 📊 Reportes

### Cierre de Turno (PDF)

El reporte incluye:
- Nombre del negocio
- Número de turno
- Hora de inicio y cierre
- Total de ventas
- Cantidad inicial de caja
- Productos con stock bajo

### Bitácora Diaria

Muestra:
- Todas las ventas del día
- Hora de cada venta
- Método de pago
- Total y cambio

## 🐛 Solución de Problemas

### Error: "Database is locked"

Cierra todas las instancias de la aplicación y elimina:
```bash
rm instance/pos_system.db
```
Luego reinicia la aplicación.

### Error: "Module not found"

Reinstala las dependencias:
```bash
pip install -r requirements.txt --force-reinstall
```

### No se abre el navegador automáticamente

Accede manualmente a:
- `http://127.0.0.1:5000`
- `http://localhost:5000`

### Problemas en móvil

- Asegúrate de usar HTTPS si estás en red externa
- Verifica que el firewall permita el puerto 5000
- Usa la licencia móvil para hasta 3 dispositivos

## 📞 Soporte

Para soporte técnico o personalizaciones adicionales, contacta al desarrollador.
CARLOS ALBERTO SANCHEZ GARCIA 

---

**Versión**: 1.0.0  
**Año**: 2026  
**Desarrollado con**: Flask, SQLAlchemy, HTML5, CSS3, JavaScript
PUEDE CONTENER ERRORES NO ENGO UN PAPEL QUE ME ABALE COMO PROGRAMADOR TODO ES MIESFUERZO Y PASION POR HACER LA VIDA MAS FACIL 
