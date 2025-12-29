#!/bin/bash
echo "Preparando entorno para Video Converter en Codespaces..."

# 1. Actualizar e instalar FFmpeg (necesario en Linux)
echo "Instalando FFmpeg..."
sudo apt-get update && sudo apt-get install -y ffmpeg

# 2. Instalar dependencias de Python
echo "Instalando librerías de Python..."
pip install -r requirements.txt

echo "------------------------------------------------"
echo "¡Todo listo!"
echo "Para iniciar la aplicación web, ejecuta:"
echo "streamlit run converter_web.py"
echo "------------------------------------------------"
