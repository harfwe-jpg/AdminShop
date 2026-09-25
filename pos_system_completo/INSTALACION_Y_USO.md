# 📋 Guía de Instalación y Uso - Sistema POS

## Requisitos del Sistema

- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows, macOS o Linux
- **Navegador**: Chrome, Firefox, Edge o Safari (últimas versiones)
- **RAM**: Mínimo 2GB
- **Almacenamiento**: 100MB libres

## 🚀 Instalación Paso a Paso

### Paso 1: Descargar/Clonar el Proyecto

```bash
# Si usas Git
git clone [repositorio]
cd pos_system

# O simplemente navega a la carpeta pos_system
```

### Paso 2: Instalar Python (si no lo tienes)

1. Ve a https://www.python.org/downloads/
2. Descarga la versión más reciente (3.8+)
3. Ejecuta el instalador
4. ✅ Marca "Add Python to PATH"
5. Haz clic en "Install Now"

### Paso 3: Instalar Dependencias

Abre una terminal/consola en la carpeta `pos_system`:

```bash
cd pos_system
pip install -r requirements.txt
```

**En Windows**, si `pip` no funciona, usa:
```bash
python -m pip install -r requirements.txt
```

### Paso 4: Ejecutar la Aplicación

```bash
python app.py
```

O usa el script de inicio:
```bash
python start.py
```

### Paso 5: Abrir en el Navegador

La aplicación se abrirá automáticamente en:
- `http://127.0.0.1:5000`

Si no se abre automáticamente, escribe esa URL en tu navegador.

---

## 🎯 Primer Uso del Sistema

### 1. Activar Licencia

En la pantalla de activación, ingresa una de estas claves:

| Tipo | Clave | Duración |
|------|-------|----------|
| **Prueba** | `MEM-1M-2026-XOXTL-79F4K` | 1 mes gratis |
| **Permanente** | `LIFETIME-VIP-2026-XOXTL-99Z8X` | Para siempre |
| **Móvil** | `MOB-TAB-ACC-2026-XOXTL-5D2W9` | 3 dispositivos |

### 2. Leer Términos

Después de activar, lee la pantalla de bienvenida que explica:
- La licencia es solo para este dispositivo
- Después del mes de prueba requiere pago
- La clave permanente activa el sistema para siempre

### 3. Registrar tu Negocio

Ingresa:
- **Nombre del negocio**: Ej. "Tienda El Sol" (aparece en reportes)
- **Usuario**: Tu nombre (ej. "Juan")
- **Contraseña**: 4 dígitos numéricos (ej. "1234")

⚠️ **Importante**: Recuerda tu contraseña, la necesitarás para:
- Iniciar sesión diariamente
- Cerrar turnos
- Acceder al sistema completo

### 4. Iniciar Sesión

Usa el usuario y contraseña que registraste.

### 5. Iniciar Turno

Selecciona:
- **Número de turno**: 1 o 2
- **Cantidad inicial**: Dinero con el que inicia la caja (ej. 500.00)

### 6. ¡Listo! Comienza a Vender

Ahora tienes acceso completo al sistema.

---

## 💼 Operaciones Diarias

### Registrar un Producto

1. Ve a la pestaña **Productos**
2. Llena el formulario:
   - **Código de barras**: El número impreso en el producto
   - **Nombre**: Nombre único del producto
   - **Tipo**: Pieza, Kilo (jitomate), o Paquete (arroz)
   - **Stock**: Cantidad de piezas (requiere confirmación)
   - **Precio público**: A cuánto vendes
   - **Precio proveedor**: A cuánto te cuesta
3. Haz clic en **Guardar Producto**

⚠️ **Notas**:
- No puedes duplicar nombres de productos
- El sistema calcula automáticamente el margen de ganancia
- Stock ≤ 3 muestra alerta de "agotándose"

### Realizar una Venta

1. Ve a la pestaña **Ventas**
2. **Buscar producto**:
   - Por nombre en la barra principal
   - Por código de barras en la segunda barra
3. Haz clic en el producto para agregarlo al carrito
4. Repite hasta tener todos los productos
5. **Selecciona método de pago**:
   - 💵 Efectivo (puedes usar calculadora de billetes)
   - 💳 Tarjeta (no requiere cantidad)
   - 🏦 Transferencia (no requiere cantidad)
6. Si es efectivo, ingresa cantidad recibida o usa botones de billetes
7. Haz clic en **Realizar Venta**
8. Verás notificación con total y cambio

### Consultar Bitácora

1. Ve a la pestaña **Bitácora**
2. Verás todas las ventas del día con:
   - Hora exacta
   - Folio de venta
   - Turno
   - Método de pago
   - Total y cambio

### Cerrar Turno

1. Ve al **Dashboard**
2. En "Cerrar Turno", ingresa tu contraseña (4 dígitos)
3. Haz clic en **Cerrar Turno**
4. Se genera PDF de cierre
5. La bitácora se limpia para el siguiente turno

---

## 📱 Uso en Celular/Tablet

### Con Licencia Móvil

La clave `MOB-TAB-ACC-2026-XOXTL-5D2W9` permite:
- Registrar hasta 3 dispositivos
- Interfaz optimizada para touch
- Botones más grandes
- Menú colapsable

### Acceder desde otro dispositivo

1. En el dispositivo principal, nota la IP que muestra la consola
   - Ej: `http://192.168.1.100:5000`
2. En el celular/tablet, abre el navegador
3. Ingresa esa IP
4. Activa con la clave móvil
5. ¡Listo!

---

## 💾 Respaldos de Base de Datos

### Automáticos

Se crean automáticamente:
- Al cerrar turno
- Al registrar el negocio

### Manuales

1. Ve a **Productos** o **Bitácora**
2. Haz clic en **💾 Respaldar DB**
3. Los archivos se guardan en `backups/`

### Tipos de Respaldo

- `.db`: Copia binaria exacta (para restaurar)
- `.sql`: Exportación legible (para migrar)

### Restaurar un Respaldo

```bash
# Método 1: Copiar manualmente
cp backups/backup_pos_20260101_120000.db instance/pos_system.db

# Método 2: Usar script
python backup_utils.py restore backups/backup_pos_20260101_120000.db
```

---

## 🔧 Solución de Problemas Comunes

### "ModuleNotFoundError: No module named 'flask'"

```bash
pip install -r requirements.txt
```

### "Database is locked"

1. Cierra la aplicación (Ctrl+C en la consola)
2. Cierra todos los navegadores
3. Vuelve a ejecutar `python app.py`

### "Address already in use"

El puerto 5000 está ocupado. Cambia el puerto en `app.py`:

```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Cambia 5000 por 5001
```

### No se abre el navegador

Abre manualmente:
- `http://127.0.0.1:5000`
- `http://localhost:5000`

### Olvidé mi contraseña

1. Abre el archivo `instance/pos_system.db` con un editor SQLite
2. Busca la tabla `businesses`
3. Modifica el campo `owner_password`
4. O elimina el registro y regístrate de nuevo (pierdes datos)

### Productos duplicados

El sistema previene nombres duplicados. Si necesitas corregir:
1. Ve a Productos
2. Edita el producto existente
3. O elimina y crea uno nuevo

---

## 📊 Consejos de Uso

### Para Tiendas de Abarrotes

1. **Productos por kilo**: Configura jitomate, cebolla, etc. como "Kilo"
2. **Productos por pieza**: Refrescos, dulces, etc. como "Pieza"
3. **Productos por paquete**: Arroz, sopa, etc. como "Paquete"

### Para Máxima Eficiencia

1. **Usa código de barras**: Escanea productos directamente
2. **Calculadora de billetes**: Agrega rápido la cantidad recibida
3. **Turnos definidos**: Mañana (1) y Tarde (2)
4. **Respaldos diarios**: Antes de cerrar

### Para Inventario

1. **Revisa alertas**: Productos con ≤3 piezas en Dashboard
2. **Margen de ganancia**: Mantén al menos 20-30%
3. **Actualiza precios**: Cuando cambien costos de proveedor

---

## 📞 Soporte Técnico

Si tienes problemas:

1. Revisa este documento completo
2. Verifica los logs en la consola
3. Revisa que Python esté actualizado
4. Reinstala dependencias si es necesario

---

**Versión**: 1.0.0  
**Año**: 2026  
**Idioma**: Español
