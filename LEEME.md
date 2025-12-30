# 🎬 Conversor de Video Universal (MKV a MP4)

Una herramienta potente y sencilla para convertir videos pesados (MKV, AVI, MOV, etc.) a formato **MP4** compatible con todos los dispositivos (TV, Celulares, Windows, Mac).

**Características:**
- ⚡ **Modo Rápido:** Convierte películas de varios GB en minutos.
- 📉 **Compresión Inteligente:** Mantiene buena calidad reduciendo el peso.
- 🌍 **Multi-Plataforma:** Funciona en tu PC (Windows) o en la Nube (GitHub Codespaces).

---

## 🖥️ Opción 1: Uso en Windows (Local)

Ideal si quieres convertir archivos que ya tienes en tu disco duro.

### 📋 Requisitos
1. Tener **Python** instalado.
2. **FFmpeg**: El programa intentará descargarlo automáticamente si no lo tienes.

### 🚀 Pasos
1. Descarga este repositorio (botón "Code" > "Download ZIP") y descomprímelo.
2. Haz doble clic en el archivo **`iniciar_programa.bat`**.
3. Se abrirá la ventana del conversor.
   - Si falta FFmpeg, te preguntará si quieres descargarlo. Di que **Sí**.
4. Selecciona tu video, marca "Modo Rápido" y dale a **Convertir**.

---

## ☁️ Opción 2: Uso en GitHub Codespaces (Nube)

**¡Recomendado!** Usa esta opción si:
- Tu PC es lenta.
- Tienes videos gigantes (10GB+).
- Quieres aprovechar la velocidad de internet de los servidores de GitHub (descargas/subidas ultra rápidas).

### 🚀 Pasos para iniciar
1. En la página de GitHub de este repositorio, haz clic en el botón verde **"Code"** > pestaña **"Codespaces"** > **"Create codespace on main"**.
2. Espera a que cargue el entorno (verás una terminal en la parte inferior).
3. Copia y pega este comando en la terminal para instalar todo:
   ```bash
   bash setup_codespaces.sh
   ```
4. Inicia la aplicación web con este comando:
   ```bash
   streamlit run converter_web.py
   ```
5. Se abrirá una pestaña en tu navegador con el conversor.

### 📂 ¿Cómo convertir archivos GIGANTES (+1GB) en Codespaces?

La web tiene límites de subida, pero hay trucos para saltárselos:

**Método A: Arrastrar a VS Code (El mejor para archivos locales)**
1. En tu Codespace, mira la barra lateral izquierda (donde están los archivos `LEEME.md`, `converter_web.py`, etc.).
2. **Arrastra tu video desde tu PC y suéltalo ahí mismo**, en la lista de archivos.
3. Espera a que suba (VS Code lo maneja mejor que el navegador).
4. En la App Web, selecciona: **"🔗 Usar archivo existente en el servidor"**.

**Método B: Google Drive (El más rápido)**
1. Ten tu video en Google Drive.
2. Haz clic derecho > Compartir > **Cualquier persona con el enlace**.
3. En la App Web, selecciona: **"🌐 Descargar desde URL"**.
4. Pega el enlace. ¡Se descargará en segundos usando el internet de GitHub!

---

## 🛠️ Solución de Problemas Frecuentes

**Error: "Request failed with status code 413" en la web**
- Significa que el archivo es muy grande para subirlo por el navegador.
- **Solución:** Usa el "Método A" descrito arriba (Arrastrar a la lista de archivos de VS Code).

**Error: "Falta FFmpeg" en Windows**
- Asegúrate de estar conectado a internet la primera vez para que el programa pueda descargarlo.
- Si falla, descarga `ffmpeg.exe` manualmente desde [gyan.dev](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z) y ponlo en la carpeta del programa.
