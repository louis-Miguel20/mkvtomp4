@echo off
echo Iniciando Conversor de Video...
py video_converter.py
if %errorlevel% neq 0 (
    echo.
    echo No se pudo iniciar con 'py'. Intentando con 'python'...
    python video_converter.py
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: No se encontro Python.
        echo Por favor instala Python desde https://www.python.org/downloads/
        echo Asegurate de marcar "Add Python to PATH" durante la instalacion.
        pause
    )
)
pause
