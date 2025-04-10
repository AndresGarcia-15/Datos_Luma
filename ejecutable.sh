#!/bin/bash
set -e  # Detener el script si ocurre un error

# Configurar la localización
export LANG=en_US.UTF-8
# sudo -i

# Navegar al directorio del proyecto
cd /home/pipe15200/LumaExecutable || { echo "Error: No se pudo acceder a /root/LumaExecutable"; exit 1; }

# Verificar si el entorno virtual existe antes de activarlo
if [ -d ".venv" ]; then
    source /home/pipe15200/LumaExecutable/.venv/bin/activate
else
    echo "Error: No se encontró el entorno virtual .venv. Creándolo..."
    sudo python3 -m venv .venv
    source /home/pipe15200/LumaExecutable/.venv/bin/activate
fi

# Instalar los requisitos
pip install -r requirements.txt

# Ejecutar el script en Python
exec python3 geturls.py  # Usa exec para reemplazar el proceso actual