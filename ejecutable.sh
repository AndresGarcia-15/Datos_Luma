#!/bin/bash
set -e  # Detener el script si ocurre un error

# Configurar la localización
export LANG=en_US.UTF-8

# Navegar al directorio del proyecto
cd /home/pipe15200/LumaExecutable || { echo "Error: No se pudo acceder a /home/pipe15200/LumaExecutable"; exit 1; }

# Verificar si el entorno virtual existe antes de activarlo
if [ -d ".venv" ]; then
    echo "Activando entorno virtual existente..."
    source .venv/bin/activate
else
    echo "No se encontró el entorno virtual .venv. Creándolo..."
    python3 -m venv .venv
    source .venv/bin/activate
fi

# Asegurar que pip esté actualizado
pip install --upgrade pip

# Instalar los requisitos
if ! pip install -r requirements.txt; then
    echo "❌ Error al instalar los paquetes. Revisa los permisos o el contenido del archivo requirements.txt."
    exit 1
fi
sleep 1
# Ejecutar el script en Python
exec python3 geturls.py