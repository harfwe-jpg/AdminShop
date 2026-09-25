# Archivos de Respaldo

Este directorio contiene los respaldos automáticos de la base de datos del sistema POS.

## Tipos de Respaldo

1. **Binario (.db)**: Copia exacta de la base de datos SQLite
2. **SQL Dump (.sql)**: Exportación en formato SQL legible

## Frecuencia

- **Automático**: Al cerrar turno
- **Manual**: Botón "Respaldar DB" en productos y bitácora

## Restauración

Para restaurar un respaldo:

1. Detén la aplicación
2. Copia el archivo de respaldo a `instance/pos_system.db`
3. Reinicia la aplicación

## Nota

Los respaldos se nombran con timestamp: `backup_pos_YYYYMMDD_HHMMSS.db`
