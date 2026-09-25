#!/usr/bin/env python3
"""
Script de Respaldo Manual para Sistema POS
Crea copias de seguridad de la base de datos
"""

import sqlite3
import os
import shutil
from datetime import datetime

def create_backup(source_db='instance/pos_system.db', backup_dir='backups'):
    """Crea un respaldo binario de la base de datos"""

    # Crear directorio si no existe
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Verificar que la base de datos existe
    if not os.path.exists(source_db):
        print(f"❌ Error: La base de datos {source_db} no existe")
        return None

    # Generar nombre con timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"backup_pos_manual_{timestamp}.db"
    backup_path = os.path.join(backup_dir, backup_filename)

    try:
        # Método 1: Copia directa del archivo
        shutil.copy2(source_db, backup_path)
        print(f"✅ Respaldo binario creado: {backup_path}")

        # Método 2: Respaldo SQL
        sql_backup_path = backup_path.replace('.db', '.sql')
        create_sql_backup(source_db, sql_backup_path)

        return backup_path

    except Exception as e:
        print(f"❌ Error al crear respaldo: {e}")
        return None


def create_sql_backup(source_db, output_path):
    """Crea un respaldo en formato SQL"""

    try:
        conn = sqlite3.connect(source_db)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"-- Respaldo SQL de POS System\n")
            f.write(f"-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            for line in conn.iterdump():
                f.write(f'{line}\n')

        conn.close()
        print(f"✅ Respaldo SQL creado: {output_path}")

    except Exception as e:
        print(f"❌ Error al crear respaldo SQL: {e}")


def list_backups(backup_dir='backups'):
    """Lista todos los respaldos disponibles"""

    if not os.path.exists(backup_dir):
        print(f"El directorio {backup_dir} no existe")
        return

    files = os.listdir(backup_dir)
    db_files = [f for f in files if f.endswith('.db')]
    sql_files = [f for f in files if f.endswith('.sql')]

    print(f"\n📁 Respaldos en {backup_dir}:")
    print(f"{'='*50}")

    if db_files:
        print(f"\n📦 Archivos .db ({len(db_files)}):")
        for f in sorted(db_files):
            filepath = os.path.join(backup_dir, f)
            size = os.path.getsize(filepath)
            print(f"  - {f} ({size:,} bytes)")

    if sql_files:
        print(f"\n📄 Archivos .sql ({len(sql_files)}):")
        for f in sorted(sql_files):
            filepath = os.path.join(backup_dir, f)
            size = os.path.getsize(filepath)
            print(f"  - {f} ({size:,} bytes)")

    if not db_files and not sql_files:
        print("  No hay respaldos disponibles")


def restore_backup(backup_file, target_db='instance/pos_system.db'):
    """Restaura un respaldo"""

    if not os.path.exists(backup_file):
        print(f"❌ Error: El archivo {backup_file} no existe")
        return False

    try:
        # Crear respaldo del estado actual antes de restaurar
        if os.path.exists(target_db):
            create_backup(target_db, 'backups')

        # Copiar respaldo a la ubicación original
        shutil.copy2(backup_file, target_db)
        print(f"✅ Respaldo restaurado exitosamente")
        return True

    except Exception as e:
        print(f"❌ Error al restaurar: {e}")
        return False


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'backup':
            create_backup()
        elif command == 'list':
            list_backups()
        elif command == 'restore' and len(sys.argv) > 2:
            restore_backup(sys.argv[2])
        else:
            print("Comandos disponibles:")
            print("  python backup_utils.py backup  - Crear respaldo")
            print("  python backup_utils.py list    - Listar respaldos")
            print("  python backup_utils.py restore <archivo> - Restaurar respaldo")
    else:
        # Ejecutar respaldo por defecto
        print("🔄 Creando respaldo automático...")
        create_backup()
        print("\n✅ Proceso completado")
