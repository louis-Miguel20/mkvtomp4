import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import subprocess
import threading
import os
import sys
import time
import re

class VideoConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Video a MP4")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        # Variables
        self.input_file = tk.StringVar()
        self.status_msg = tk.StringVar(value="Esperando archivo...")
        self.is_converting = False

        # UI Setup
        self.create_widgets()
        
        # Check FFmpeg on startup
        self.check_ffmpeg()

    def create_widgets(self):
        # Header
        header = tk.Label(self.root, text="Conversor Rápido a MP4", font=("Helvetica", 16, "bold"))
        header.pack(pady=15)

        # File Selection Frame
        frame_input = tk.Frame(self.root)
        frame_input.pack(pady=10, padx=20, fill="x")

        lbl_input = tk.Label(frame_input, text="Archivo de Video:", font=("Helvetica", 10))
        lbl_input.pack(anchor="w")

        entry_input = tk.Entry(frame_input, textvariable=self.input_file, state="readonly", width=50)
        entry_input.pack(side="left", fill="x", expand=True, pady=5)

        btn_browse = tk.Button(frame_input, text="Seleccionar", command=self.browse_file)
        btn_browse.pack(side="right", padx=(10, 0))

        # Options Frame (Simple for now)
        frame_options = tk.Frame(self.root)
        frame_options.pack(pady=5, padx=20, fill="x")
        
        self.fast_mode = tk.BooleanVar(value=True)
        chk_fast = tk.Checkbutton(frame_options, text="Modo Rápido (Menor compresión, más velocidad)", variable=self.fast_mode)
        chk_fast.pack(anchor="w")

        # Convert Button
        self.btn_convert = tk.Button(self.root, text="Convertir a MP4", command=self.start_conversion_thread, 
                                     bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), height=2)
        self.btn_convert.pack(pady=(20, 10), fill="x", padx=100)

        # Progress Bar
        frame_progress = tk.Frame(self.root)
        frame_progress.pack(pady=5, padx=20, fill="x")
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(frame_progress, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(side="left", fill="x", expand=True)
        
        self.lbl_percentage = tk.Label(frame_progress, text="0%", width=5)
        self.lbl_percentage.pack(side="right", padx=(5, 0))

        # Log/Output Area
        lbl_log = tk.Label(self.root, text="Registro de Progreso:", font=("Helvetica", 9))
        lbl_log.pack(anchor="w", padx=20)

        self.log_area = scrolledtext.ScrolledText(self.root, height=10, state="disabled", font=("Consolas", 9))
        self.log_area.pack(padx=20, pady=(0, 20), fill="both", expand=True)

    def log(self, message):
        self.root.after(0, self._log_internal, message)

    def _log_internal(self, message):
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state="disabled")

    def check_ffmpeg(self):
        """Checks if ffmpeg is accessible."""
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
            self.log("✓ FFmpeg detectado correctamente.")
        except FileNotFoundError:
            # Try to find ffmpeg in current directory explicitly
            if os.path.exists("ffmpeg.exe"):
                # If it exists in CWD but not in PATH, we might need to use ./ffmpeg.exe in commands, 
                # but subprocess usually finds it if it's in CWD.
                # However, let's verify if we can run it.
                try:
                    subprocess.run(["./ffmpeg.exe", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)
                    self.log("✓ FFmpeg detectado en carpeta local.")
                    return
                except:
                    pass

            self.log("⚠ ERROR: FFmpeg no encontrado.")
            answer = messagebox.askyesno("Falta FFmpeg", "No se encontró FFmpeg. ¿Quieres que lo descargue automáticamente?\n(Se requiere conexión a Internet)")
            if answer:
                self.download_ffmpeg_thread()
            else:
                self.log("Por favor, descarga FFmpeg manualmente y colócalo aquí.")
                self.btn_convert.config(state="disabled")

    def download_ffmpeg_thread(self):
        thread = threading.Thread(target=self.download_ffmpeg)
        thread.daemon = True
        thread.start()

    def download_ffmpeg(self):
        self.log("⬇ Iniciando descarga de FFmpeg...")
        self.btn_convert.config(state="disabled", text="Descargando FFmpeg...")
        
        import urllib.request
        import zipfile
        import shutil

        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        zip_path = "ffmpeg.zip"

        def progress_hook(count, block_size, total_size):
            if total_size > 0:
                percent = int(count * block_size * 100 / total_size)
                # Update button text with percentage (limit updates to avoid lag)
                if percent % 5 == 0: 
                    self.root.after(0, lambda: self.btn_convert.config(text=f"Descargando... {percent}%"))

        try:
            # Download
            self.log(f"Descargando desde: {url}")
            self.log("Esto puede tardar unos minutos (aprox. 120 MB)...")
            urllib.request.urlretrieve(url, zip_path, reporthook=progress_hook)
            self.log("Descarga completada. Extrayendo...")
            self.root.after(0, lambda: self.btn_convert.config(text="Extrayendo archivos..."))

            # Extract
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Find the ffmpeg.exe path inside the zip
                ffmpeg_src = None
                for file in zip_ref.namelist():
                    if file.endswith("bin/ffmpeg.exe"):
                        ffmpeg_src = file
                        break
                
                if ffmpeg_src:
                    zip_ref.extract(ffmpeg_src, ".")
                    # Move to root
                    # ffmpeg_src is like 'ffmpeg-6.0-essentials_build/bin/ffmpeg.exe'
                    # We extracted it, so the folder structure exists locally now
                    shutil.move(ffmpeg_src, "ffmpeg.exe")
                    self.log("✓ ffmpeg.exe extraído y colocado correctamente.")
                    
                    # Cleanup folders
                    top_folder = ffmpeg_src.split("/")[0]
                    if os.path.exists(top_folder):
                        shutil.rmtree(top_folder)
                else:
                    self.log("❌ Error: No se encontró ffmpeg.exe dentro del ZIP.")

            # Cleanup zip
            if os.path.exists(zip_path):
                os.remove(zip_path)

            # Verify again
            if os.path.exists("ffmpeg.exe"):
                self.log("✓ Instalación automática completada.")
                self.btn_convert.config(state="normal", text="Convertir a MP4")
                messagebox.showinfo("Éxito", "FFmpeg se ha descargado e instalado correctamente.\nYa puedes convertir videos.")
            else:
                self.log("❌ Error: Algo falló al mover los archivos.")

        except Exception as e:
            self.log(f"❌ Error en la descarga: {str(e)}")
            messagebox.showerror("Error Descarga", f"No se pudo descargar FFmpeg automáticamente.\nError: {e}")
            self.btn_convert.config(state="disabled")

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar video",
            filetypes=[("Archivos de Video", "*.mkv *.avi *.mov *.flv *.wmv *.webm *.mp4"), ("Todos los archivos", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            self.log(f"Archivo seleccionado: {os.path.basename(filename)}")

    def start_conversion_thread(self):
        if not self.input_file.get():
            messagebox.showerror("Error", "Por favor selecciona un archivo primero.")
            return

        if self.is_converting:
            return

        thread = threading.Thread(target=self.convert_video)
        thread.daemon = True
        thread.start()

    def convert_video(self):
        self.is_converting = True
        self.btn_convert.config(state="disabled", text="Convirtiendo...")
        self.progress_var.set(0)
        self.lbl_percentage.config(text="0%")
        
        input_path = self.input_file.get()
        # Create output path: same name but .mp4 extension
        output_path = os.path.splitext(input_path)[0] + "_convertido.mp4"
        
        # Get duration
        total_duration = self.get_video_duration(input_path)
        if total_duration > 0:
            self.log(f"Duración detectada: {total_duration:.2f} segundos")

        # Determine settings based on Fast Mode
        # -preset ultrafast: Very fast encoding, larger file size
        # -preset medium: Slower, better compression
        preset = "ultrafast" if self.fast_mode.get() else "medium"
        crf = "23" # Standard quality
        
        # Build command
        # -y: Overwrite output files
        # -i: Input file
        # -c:v libx264: Use H.264 video codec (widely supported)
        # -c:a aac: Use AAC audio codec
        # -movflags +faststart: Move metadata to start of file (good for web playback)
        # -progress pipe:1 : Output progress info to stdout in a format easier to parse (key=value)
        cmd = [
            "ffmpeg", 
            "-y", 
            "-i", input_path,
            "-c:v", "libx264",
            "-preset", preset,
            "-crf", crf,
            "-c:a", "aac",
            "-movflags", "+faststart",
            output_path
        ]

        self.log("-" * 40)
        self.log(f"Iniciando conversión de: {os.path.basename(input_path)}")
        self.log(f"Modo: {'Rápido (Ultrafast)' if self.fast_mode.get() else 'Balanceado'}")
        
        start_time = time.time()

        try:
            # Run FFmpeg
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                universal_newlines=True,
                startupinfo=startupinfo
            )

            # Read output line by line
            for line in process.stdout:
                line = line.strip()
                # Parse time=HH:MM:SS.ms
                if "time=" in line:
                    time_match = re.search(r"time=(\d{2}:\d{2}:\d{2}\.\d{2})", line)
                    if time_match:
                        current_time_str = time_match.group(1)
                        current_seconds = self.time_to_seconds(current_time_str)
                        
                        if total_duration > 0:
                            percent = (current_seconds / total_duration) * 100
                            if percent > 100: percent = 100
                            
                            # Update UI safely
                            self.root.after(0, self.update_progress, percent)

            process.wait()

            end_time = time.time()
            duration = end_time - start_time

            if process.returncode == 0:
                self.root.after(0, self.update_progress, 100)
                self.log(f"✓ ÉXITO! Video guardado en:")
                self.log(f"{output_path}")
                self.log(f"Tiempo total: {duration:.2f} segundos")
                messagebox.showinfo("Éxito", f"Video convertido correctamente!\nGuardado como: {os.path.basename(output_path)}")
            else:
                self.log("❌ ERROR: La conversión falló.")
                messagebox.showerror("Error", "Ocurrió un error durante la conversión. Revisa si el archivo es válido.")

        except Exception as e:
            self.log(f"❌ Error crítico: {str(e)}")
            messagebox.showerror("Error Crítico", str(e))
        
        finally:
            self.is_converting = False
            self.root.after(0, self.reset_button)

    def update_progress(self, percent):
        self.progress_var.set(percent)
        self.lbl_percentage.config(text=f"{int(percent)}%")

    def get_video_duration(self, input_path):
        """Get video duration in seconds using ffmpeg."""
        try:
            cmd = ["ffmpeg", "-i", input_path]
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            # FFmpeg prints file info to stderr when no output is specified
            result = subprocess.run(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                startupinfo=startupinfo,
                universal_newlines=True
            )
            output = result.stderr
            
            # Search for "Duration: 00:00:00.00"
            match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2}\.\d{2})", output)
            if match:
                hours = int(match.group(1))
                minutes = int(match.group(2))
                seconds = float(match.group(3))
                return hours * 3600 + minutes * 60 + seconds
        except:
            pass
        return 0

    def time_to_seconds(self, time_str):
        # time_str format: HH:MM:SS.ms
        try:
            h, m, s = time_str.split(':')
            return int(h) * 3600 + int(m) * 60 + float(s)
        except:
            return 0

    def reset_button(self):
        self.btn_convert.config(state="normal", text="Convertir a MP4")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConverterApp(root)
    root.mainloop()
