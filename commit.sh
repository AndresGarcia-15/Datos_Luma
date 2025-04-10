#!/bin/bash
# filepath: c:/Users/adria/Desktop/Luma_api_sunspot/soho/commit.sh

# Cambiar al directorio del repositorio que se va a actualizar
cd /home/ubuntu/Lumaweb/Web || exit

# Obtener la fecha y hora actual
datetime=$(date +"%Y%m%d%H%M")

# Extraer año, mes, día, hora y minutos
year=${datetime:0:4}
month=${datetime:4:2}
day=${datetime:6:2}
hour=${datetime:8:2}
minute=${datetime:10:2}

# Imprimir la fecha y hora en el formato deseado
git add --all
git commit -m "autoCommit DATA $day/$month/$year $hour:$minute"
git push

