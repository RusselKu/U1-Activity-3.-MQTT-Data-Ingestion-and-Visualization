#!/usr/bin/env python3
"""
Script de verificación para asegurar que el proyecto está correctamente configurado.
Ejecutar antes de iniciar los servicios.
"""

import os
import sys
import json
from pathlib import Path

def check_file_exists(filepath):
    """Verificar que un archivo existe"""
    if Path(filepath).exists():
        print(f"✅ {filepath} - OK")
        return True
    else:
        print(f"❌ {filepath} - NO ENCONTRADO")
        return False

def check_docker_installed():
    """Verificar que Docker está instalado"""
    result = os.system("docker --version > /dev/null 2>&1")
    if result == 0:
        print("✅ Docker - OK")
        return True
    else:
        print("❌ Docker - NO INSTALADO")
        return False

def check_docker_compose_installed():
    """Verificar que Docker Compose está instalado"""
    result = os.system("docker-compose --version > /dev/null 2>&1")
    if result == 0:
        print("✅ Docker Compose - OK")
        return True
    else:
        print("❌ Docker Compose - NO INSTALADO")
        return False

def check_python_installed():
    """Verificar que Python 3.11+ está instalado"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python {version.major}.{version.minor} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} - Requiere 3.11+")
        return False

def main():
    print("\n" + "="*50)
    print("🔍 VERIFICACIÓN DEL PROYECTO IoT MQTT")
    print("="*50 + "\n")
    
    # Verificar archivos requeridos
    print("📁 Verificando archivos...")
    files_to_check = [
        "docker-compose.yml",
        "Dockerfile",
        "requirements.txt",
        "ElementosClaveParaLevantarTodo.md",
        ".gitignore",
        "Project_Elements/publisher.ipynb",
        "Project_Elements/suscriber.ipynb",
        "subscriber/subscriber.py",
        "streamlit_app/Dockerfile",
        "README.md",
        ".env.example"
    ]
    
    files_ok = all(check_file_exists(f) for f in files_to_check)
    
    print("\n🔧 Verificando herramientas...")
    tools_ok = all([
        check_docker_installed(),
        check_docker_compose_installed(),
        check_python_installed()
    ])
    
    print("\n" + "="*50)
    if files_ok and tools_ok:
        print("✅ VERIFICACIÓN COMPLETADA - TODO OK")
        print("\nPróximos pasos:")
        print("1. Crear archivo .env desde .env.example")
        print("2. Ejecutar: docker-compose build")
        print("3. Ejecutar: docker-compose up -d")
        print("4. Crear tablas en PostgreSQL (ver ElementosClaveParaLevantarTodo.md)")
        print("5. Ejecutar Publisher: jupyter notebook Project_Elements/publisher.ipynb")
        print("6. Ejecutar Subscriber: python subscriber/subscriber.py")
        print("7. Ver datos en Streamlit: http://localhost:8501")
    else:
        print("❌ VERIFICACIÓN FALLÓ")
        print("\nSoluciona los problemas anteriores e intenta de nuevo.")
        sys.exit(1)
    
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
