import streamlit as st
import subprocess
import os
import time
import sys

# Configuración de la página
st.set_page_config(page_title="Conversor de Video MP4", page_icon="🎬")

st.title("🎬 Conversor de Video a MP4 (Web/Codespaces)")
st.write("Convierte videos pesados a MP4 usando la potencia de la nube o tu servidor local.")

# Verificar FFmpeg en Linux/Codespaces
def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

if not check_ffmpeg():
    st.error("❌ FFmpeg no está instalado.")
    st.info("Si estás en Codespaces, ejecuta esto en la terminal: `sudo apt-get update && sudo apt-get install -y ffmpeg`")
    st.stop()

# Opción para seleccionar archivo
option = st.radio("¿Dónde está tu video?", ["Subir archivo (Pequeños)", "Seleccionar archivo de la carpeta (Grandes)"])

input_path = None

if option == "Subir archivo (Pequeños)":
    uploaded_file = st.file_uploader("Elige un video", type=['mkv', 'avi', 'mov', 'flv', 'wmv', 'webm', 'mp4'])
    if uploaded_file is not None:
        # Guardar temporalmente
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        input_path = uploaded_file.name
        st.success(f"Archivo subido: {input_path}")

else:
    # Listar archivos en el directorio actual
    files = [f for f in os.listdir('.') if f.endswith(('.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm', '.mp4'))]
    if not files:
        st.warning("No se encontraron videos en la carpeta actual.")
    else:
        input_path = st.selectbox("Selecciona un video de la lista:", files)

# Opciones de conversión
st.subheader("Configuración")
fast_mode = st.checkbox("Modo Rápido (Recomendado)", value=True)

if input_path and st.button("🚀 Convertir a MP4"):
    output_path = os.path.splitext(input_path)[0] + "_convertido.mp4"
    
    preset = "ultrafast" if fast_mode else "medium"
    
    # Comando FFmpeg (Compatible con Linux/Windows)
    cmd = [
        "ffmpeg", 
        "-y", 
        "-i", input_path,
        "-c:v", "libx264",
        "-preset", preset,
        "-crf", "23",
        "-c:a", "aac",
        "-movflags", "+faststart",
        output_path
    ]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    status_text.text("Iniciando conversión...")
    
    start_time = time.time()
    
    # Ejecutar proceso
    try:
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            universal_newlines=True
        )
        
        # Intentar obtener duración para la barra de progreso (simple)
        # Nota: En web es más complejo parsear en tiempo real perfecto sin bloquear, 
        # así que usaremos un spinner o lectura básica.
        
        for line in process.stdout:
            # Aquí podríamos parsear el progreso, pero para simplificar en web
            # mostraremos los logs clave o mantendremos el spinner.
            pass
            
        process.wait()
        
        if process.returncode == 0:
            progress_bar.progress(100)
            duration = time.time() - start_time
            st.success(f"¡Éxito! Conversión terminada en {duration:.2f} segundos.")
            
            # Botón de descarga
            with open(output_path, "rb") as f:
                st.download_button(
                    label="⬇ Descargar video convertido",
                    data=f,
                    file_name=output_path,
                    mime="video/mp4"
                )
        else:
            st.error("Hubo un error en la conversión.")
            
    except Exception as e:
        st.error(f"Error: {e}")
