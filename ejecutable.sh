#!/bin/bash
set -e  # Detiene el script si ocurre un error

# Configurar la localización
export LANG=en_US.UTF-8

# Navegar al directorio del proyecto
cd /home/ubuntu/Lumaweb/Datos_Luma || { echo "❌ Error: No se pudo acceder a /home/ubuntu/Lumaweb/Datos_Luma"; exit 1; }

# Limpiar el entorno virtual anterior (por si tenía problemas de permisos)
if [ -d ".venv" ]; then
    echo "🧹 Eliminando entorno virtual anterior con permisos incorrectos..."
    rm -rf .venv
fi

# Crear entorno virtual nuevo
echo "📦 Creando entorno virtual nuevo..."
python3 -m venv .venv
source .venv/bin/activate

# Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip

# Instalar requerimientos
echo "📥 Instalando dependencias..."
if ! pip install -r requirements.txt; then
    echo "❌ Error al instalar los paquetes. Revisa los permisos o el contenido del archivo requirements.txt."
    exit 1
fi

# Ejecutar el script principal
echo "🚀 Ejecutando geturls.py..."
exec python3 geturls.py
