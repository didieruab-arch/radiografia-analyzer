#!/bin/bash

# 🚀 Script Rápido para Deploy en Render
# Ejecuta estos comandos en orden

echo "========================================="
echo "  PREPARANDO PROYECTO PARA RENDER"
echo "========================================="

# 1. Inicializar git si no existe
if [ ! -d .git ]; then
    echo "📦 Inicializando repositorio Git..."
    git init
    echo "✅ Git inicializado"
else
    echo "✅ Repositorio Git ya existe"
fi

# 2. Agregar todos los archivos
echo ""
echo "📝 Agregando archivos al staging..."
git add .

# 3. Hacer commit
echo ""
echo "💾 Creando commit..."
git commit -m "Preparar proyecto para deployment en Render - $(date '+%Y-%m-%d %H:%M:%S')"

# 4. Instrucciones para GitHub
echo ""
echo "========================================="
echo "  SIGUIENTES PASOS:"
echo "========================================="
echo ""
echo "1️⃣  Crea un repositorio en GitHub:"
echo "    👉 https://github.com/new"
echo ""
echo "2️⃣  Conecta tu repositorio local:"
echo "    git remote add origin https://github.com/TU_USUARIO/TU_REPO.git"
echo ""
echo "3️⃣  Sube tu código:"
echo "    git branch -M main"
echo "    git push -u origin main"
echo ""
echo "4️⃣  Ve a Render y crea tu Web Service:"
echo "    👉 https://dashboard.render.com/select-repo?type=web"
echo ""
echo "5️⃣  Configura tu servicio:"
echo "    - Build Command: pip install -r requirements.txt"
echo "    - Start Command: gunicorn app:app"
echo "    - Runtime: Python 3"
echo ""
echo "========================================="
echo "✅ ¡Preparación completada!"
echo "========================================="
