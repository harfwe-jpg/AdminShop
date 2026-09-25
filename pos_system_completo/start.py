#!/usr/bin/env python3
"""
Script de Inicio Rápido para Sistema POS
Verifica dependencias e inicia la aplicación
"""

import sys
import subprocess
import os

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    required = ['flask', 'flask_sqlalchemy', 'werkzeug', 'reportlab']
    missing = []

    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    return missing


def install_dependencies():
    """Instala las dependencias faltantes"""
    print("📦 Instalando dependencias...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    print("✅ Dependencias instaladas")


def main():
    print("="*50)
    print("🚀 Sistema POS - Iniciando")
    print("="*50)

    # Verificar dependencias
    missing = check_dependencies()

    if missing:
        print(f"⚠️  Faltan dependencias: {', '.join(missing)}")
        response = input("¿Instalar ahora? (s/n): ").strip().lower()

        if response == 's':
            install_dependencies()
        else:
            print("❌ No se pueden continuar sin las dependencias")
            sys.exit(1)

    # Crear directorios necesarios
    os.makedirs('instance', exist_ok=True)
    os.makedirs('backups', exist_ok=True)

    # Importar e iniciar aplicación
    print("\n🌐 Iniciando servidor...")
    from app import app

    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
