# Conversor de Video a MP4 (Rápido y Fácil)

Este es un programa sencillo para convertir videos pesados (MKV, AVI, MOV, etc.) a formato MP4 compatible con cualquier dispositivo.

## 🚀 Requisitos Previos (Importante)

Para que este programa funcione, necesitas **FFmpeg**. Es el motor que hace la conversión.

### ¿Cómo instalar FFmpeg?

**Opción A (La más fácil - Sin instalar nada):**
1. Descarga FFmpeg desde [gyan.dev](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z) o [ffmpeg.org](https://ffmpeg.org/download.html).
2. Abre el archivo descargado (necesitarás 7-Zip o WinRAR).
3. Entra en la carpeta `bin`.
4. Copia el archivo `ffmpeg.exe`.
5. **Pégalo en la misma carpeta donde está este script (`video_converter.py`).**
   - Tu carpeta debería tener: `video_converter.py` y `ffmpeg.exe`.

**Opción B (Instalación en el sistema):**
Si ya tienes FFmpeg instalado y agregado al PATH de tu sistema, el programa lo detectará automáticamente.

## 🏃‍♂️ Cómo usar

1. Asegúrate de tener Python instalado.
2. Haz doble clic en el archivo `iniciar_programa.bat` (esto abrirá el programa automáticamente).
3. Se abrirá una ventana:
   - Haz clic en **"Seleccionar"** y busca tu video pesado.
   - Marca la casilla **"Modo Rápido"** si quieres que la conversión sea veloz (recomendado para archivos muy grandes).
   - Haz clic en **"Convertir a MP4"**.
4. El nuevo video se guardará en la misma carpeta que el original, con el nombre `_convertido.mp4`.

## ⚙️ Características

- **Modo Rápido:** Usa el preset "ultrafast" para convertir archivos de varios gigabytes en poco tiempo.
- **Universal:** Convierte a MP4 con códec H.264 y audio AAC (compatible con TV, iPhone, Android, Windows).
- **Interfaz Simple:** Sin comandos complicados.
