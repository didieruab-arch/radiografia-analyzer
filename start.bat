@echo off
echo ========================================
echo LabVision - Iniciando Sistema
echo ========================================
echo.

echo Activando entorno virtual...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo [OK] Entorno virtual activado
) else (
    echo [!] Entorno virtual no encontrado
    echo Creando entorno virtual...
    py -m venv venv
    call venv\Scripts\activate.bat
    echo Instalando dependencias...
    pip install -r requirements.txt
)
echo.

echo Verificando dependencias...
python -c "import flask, ultralytics, cv2, numpy" 2>nul
if errorlevel 1 (
    echo [!] Algunas dependencias faltan. Instalando...
    pip install -r requirements.txt
    echo.
)

echo [OK] Dependencias verificadas
echo.

echo Iniciando servidor Flask...
echo El servidor estara disponible en: http://localhost:5000
echo Presiona Ctrl+C para detener el servidor
echo.
echo ========================================
echo.

python app.py
