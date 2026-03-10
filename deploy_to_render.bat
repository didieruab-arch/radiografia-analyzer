@echo off
REM 🚀 Script Rápido para Deploy en Render (Windows)
REM Ejecuta este archivo para preparar tu proyecto

echo =========================================
echo   PREPARANDO PROYECTO PARA RENDER
echo =========================================

REM 1. Verificar si existe git
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Git no está instalado. Descárgalo de: https://git-scm.com/
    pause
    exit /b 1
)

REM 2. Inicializar git si no existe
if not exist .git (
    echo 📦 Inicializando repositorio Git...
    git init
    echo ✅ Git inicializado
) else (
    echo ✅ Repositorio Git ya existe
)

REM 3. Agregar todos los archivos
echo.
echo 📝 Agregando archivos al staging...
git add .

REM 4. Hacer commit
echo.
echo 💾 Creando commit...
git commit -m "Preparar proyecto para deployment en Render - %date% %time%"

REM 5. Instrucciones para GitHub
echo.
echo =========================================
echo   SIGUIENTES PASOS:
echo =========================================
echo.
echo 1️⃣  Crea un repositorio en GitHub:
echo     👉 https://github.com/new
echo.
echo 2️⃣  Conecta tu repositorio local:
echo     git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
echo.
echo 3️⃣  Sube tu código:
echo     git branch -M main
echo     git push -u origin main
echo.
echo 4️⃣  Ve a Render y crea tu Web Service:
echo     👉 https://dashboard.render.com/select-repo?type=web
echo.
echo 5️⃣  Configura tu servicio en Render:
echo     - Build Command: pip install -r requirements.txt
echo     - Start Command: gunicorn app:app
echo     - Runtime: Python 3
echo.
echo =========================================
echo ✅ ¡Preparación completada!
echo =========================================
echo.
pause
