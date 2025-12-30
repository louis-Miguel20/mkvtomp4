import streamlit as st
import subprocess
import os
import time
import re
import shutil

# Configuración de la página
st.set_page_config(page_title="Conversor de Video MP4", page_icon="🎬", layout="centered")

st.title("🎬 Conversor de Video Universal")
st.markdown("""
Convierte tus videos (MKV, AVI, MOV...) a **MP4** compatible con todo.
""")

# --- FUNCIONES ---

def get_video_duration(input_path):
    """Obtiene la duración del video en segundos usando ffmpeg."""
    try:
        cmd = ["ffmpeg", "-i", input_path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        # Buscar "Duration: 00:00:00.00" en stderr
        match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2}\.\d{2})", result.stderr)
        if match:
            h, m, s = map(float, match.groups())
            return h * 3600 + m * 60 + s
    except:
        pass
    return 0

def time_to_seconds(time_str):
    """Convierte HH:MM:SS.ms a segundos."""
    try:
        h, m, s = time_str.split(':')
        return int(h) * 3600 + int(m) * 60 + float(s)
    except:
        return 0

# --- INTERFAZ ---

# Selector de modo simplificado
input_method = st.radio(
    "Método de entrada:", 
    ["📁 Subir Video (Desde tu PC)", "🌐 Descargar desde URL (Más rápido para la nube)", "🔗 Usar archivo existente en el servidor"]
)

input_path = None
uploaded_temp_file = "temp_input_video"

if input_method == "🌐 Descargar desde URL (Más rápido para la nube)":
    st.info("💡 Opción recomendada para archivos muy grandes si están en internet.")
    url = st.text_input("Pega el enlace directo del video (o de YouTube):")
    
    if url:
        if "youtube.com" in url or "youtu.be" in url:
            st.warning("⚠️ Para YouTube necesitas tener 'yt-dlp' instalado. (Aún no implementado en este script básico)")
        
        elif "drive.google.com" in url:
            if st.button("⬇ Descargar desde Google Drive"):
                try:
                    import gdown
                    output_file = "video_drive.mp4"
                    st.text(f"Descargando desde Drive...")
                    
                    # gdown maneja archivos grandes y confirmaciones automáticamente
                    output = gdown.download(url, output_file, quiet=False, fuzzy=True)
                    
                    if output:
                        st.success(f"✅ Descarga de Drive completada: {output}")
                        input_path = output
                    else:
                        st.error("No se pudo descargar. Asegúrate de que el enlace sea 'Público' (Cualquiera con el enlace).")
                except Exception as e:
                    st.error(f"Error con gdown: {e}")
                    st.info("Intenta instalar gdown: `pip install gdown` en la terminal.")

        else:
            if st.button("⬇ Descargar al servidor"):
                try:
                    import urllib.request
                    filename = url.split("/")[-1]
                    if not filename: filename = "video_descargado.mp4"
                    
                    # Limpiar query params
                    if "?" in filename: filename = filename.split("?")[0]
                    
                    st.text(f"Descargando: {filename}...")
                    
                    # Barra de progreso simple
                    progress_bar_dl = st.progress(0)
                    
                    def dl_hook(count, block_size, total_size):
                        if total_size > 0:
                            percent = int(count * block_size * 100 / total_size)
                            progress_bar_dl.progress(min(percent, 100))

                    urllib.request.urlretrieve(url, filename, reporthook=dl_hook)
                    st.success(f"✅ Descarga completada: {filename}")
                    input_path = filename
                    
                except Exception as e:
                    st.error(f"Error al descargar: {e}")

elif input_method == "📁 Subir Video (Desde tu PC)":
    st.warning("⚠️ NOTA IMPORTANTE: Si ves un 'Error 413' o la subida falla con archivos muy grandes (+1GB), es una restricción de GitHub Codespaces, no de esta App.")
    
    with st.expander("💡 ¿Cómo subir archivos GIGANTES sin errores? (Leer aquí)", expanded=True):
        st.markdown("""
        **Opción A (Recomendada):**
        1. Mira a la izquierda de tu pantalla, donde está la lista de archivos (`video_converter.py`, etc.).
        2. **Arrastra tu video de 7GB directamente a esa lista** (fuera de esta página web, en el editor de código).
        3. Espera a que se suba (verás un círculo de carga en VS Code).
        4. Cuando termine, selecciona arriba la opción: **"🔗 Usar archivo existente en el servidor"**.
        
        **Opción B:**
        Sube tu video a Google Drive, hazlo público y usa la opción **"🌐 Descargar desde URL"** de esta app.
        """)
        
    uploaded_file = st.file_uploader("Arrastra tu video aquí (Intentar vía Web)", type=['mkv', 'avi', 'mov', 'flv', 'wmv', 'webm', 'mp4'])
    
    if uploaded_file is not None:
        # Guardar el archivo subido en el disco para que FFmpeg pueda leerlo
        # Usamos un nombre fijo temporal para no llenar el disco
        with open(uploaded_temp_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Renombrar con la extensión correcta para que ffmpeg no se queje
        file_ext = os.path.splitext(uploaded_file.name)[1]
        input_path = f"video_input{file_ext}"
        if os.path.exists(input_path):
            os.remove(input_path)
        os.rename(uploaded_temp_file, input_path)
        
        st.success(f"✅ Archivo cargado: {uploaded_file.name} ({uploaded_file.size / (1024*1024):.1f} MB)")

else:
    # Listar archivos locales
    files = [f for f in os.listdir('.') if f.lower().endswith(('.mkv', '.avi', '.mov', '.flv', '.wmv', '.webm', '.mp4')) and "_convertido" not in f]
    if not files:
        st.warning("No hay videos en la carpeta del servidor. Sube uno primero o usa git clone.")
    else:
        selected_file = st.selectbox("Elige un archivo:", files)
        if selected_file:
            input_path = selected_file

# Opciones
with st.expander("⚙️ Configuración avanzada", expanded=True):
    fast_mode = st.checkbox("⚡ Modo Rápido (Recomendado)", value=True, help="Usa el preset 'ultrafast'. Archivos un poco más grandes pero conversión muy rápida.")

# Botón y Proceso
if input_path:
    output_filename = os.path.splitext(input_path)[0] + "_convertido.mp4"
    
    # Botón grande
    if st.button("▶ COMENZAR CONVERSIÓN", type="primary", use_container_width=True):
        
        # 1. Preparación
        progress_bar = st.progress(0)
        status_text = st.empty()
        log_expander = st.expander("Ver detalles del proceso")
        log_text = ""
        
        status_text.info("⏳ Analizando video...")
        
        # Obtener duración total para la barra
        total_duration = get_video_duration(input_path)
        if total_duration > 0:
            status_text.info(f"⏱ Duración detectada: {total_duration/60:.1f} minutos. Convirtiendo...")
        
        # Configurar FFmpeg
        preset = "ultrafast" if fast_mode else "medium"
        cmd = [
            "ffmpeg", 
            "-y", 
            "-i", input_path,
            "-c:v", "libx264",
            "-preset", preset,
            "-crf", "23",
            "-c:a", "aac",
            "-movflags", "+faststart",
            output_filename
        ]
        
        # 2. Ejecución
        start_time = time.time()
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            universal_newlines=True
        )
        
        # 3. Monitoreo en tiempo real
        for line in process.stdout:
            # log_text += line
            # log_expander.code(log_text[-1000:]) # Mostrar últimas líneas
            
            if "time=" in line:
                # Parsear tiempo: time=00:01:23.45
                time_match = re.search(r"time=(\d{2}:\d{2}:\d{2}\.\d{2})", line)
                if time_match and total_duration > 0:
                    current_seconds = time_to_seconds(time_match.group(1))
                    percent = int((current_seconds / total_duration) * 100)
                    progress_bar.progress(min(percent, 100))
                    status_text.text(f"🚀 Convirtiendo... {percent}%")
        
        process.wait()
        
        # 4. Finalización
        if process.returncode == 0:
            progress_bar.progress(100)
            end_time = time.time()
            st.success(f"🎉 ¡TERMINADO! Tiempo total: {end_time - start_time:.1f}s")
            
            # Botón de descarga
            with open(output_filename, "rb") as f:
                st.download_button(
                    label="⬇️ DESCARGAR VIDEO MP4",
                    data=f,
                    file_name=output_filename,
                    mime="video/mp4",
                    use_container_width=True
                )
        else:
            st.error("❌ Ocurrió un error en la conversión.")
            st.error("Revisa los logs para más detalles.")

else:
    st.info("👆 Sube un video o selecciona uno para empezar.")
