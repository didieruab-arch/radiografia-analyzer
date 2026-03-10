# 🚀 Guía de Deployment en Render

## 📋 Preparación Completada

Ya se han creado/actualizado los siguientes archivos necesarios para Render:

- ✅ `requirements.txt` - Actualizado con gunicorn y opencv-python-headless
- ✅ `Procfile` - Comando de inicio con gunicorn
- ✅ `render.yaml` - Configuración de Render
- ✅ `runtime.txt` - Versión de Python
- ✅ `app.py` - Modificado para usar variable de entorno PORT

## 🌐 Pasos para Deployar en Render

### 1️⃣ Preparar tu Repositorio Git

```bash
# Inicializar repositorio si no existe
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Preparar proyecto para deployment en Render"

# Crear repositorio en GitHub y conectarlo
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git branch -M main
git push -u origin main
```

### 2️⃣ Crear Cuenta en Render

1. Ve a [https://render.com](https://render.com)
2. Crea una cuenta o inicia sesión
3. Conecta tu cuenta de GitHub

### 3️⃣ Crear Nuevo Web Service

1. Click en **"New +"** → **"Web Service"**
2. Conecta tu repositorio de GitHub
3. Configura los siguientes campos:

   - **Name**: `radiografia-analyzer` (o el nombre que prefieras)
   - **Region**: Selecciona la región más cercana
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### 4️⃣ Configurar Variables de Entorno (Opcional)

Si necesitas configurar variables adicionales:

```
CONFIDENCE_THRESHOLD=0.60
YOLO_IMG_SIZE=640
YOLO_IOU_THRESHOLD=0.45
```

### 5️⃣ Configurar el Plan

- **Free Tier**: Disponible pero con limitaciones
  - 750 horas/mes gratis
  - Se duerme después de 15 min de inactividad
  - 512 MB RAM
  
- **Starter Plan**: ~$7/mes
  - Siempre activo
  - 512 MB RAM
  - Mejor rendimiento

### 6️⃣ Deploy

1. Click en **"Create Web Service"**
2. Render automáticamente:
   - Clonará tu repositorio
   - Instalará las dependencias
   - Iniciará tu aplicación

3. Espera a que el deploy termine (puede tomar 5-10 minutos)

### 7️⃣ Acceder a tu Aplicación

Una vez completado el deploy:
- URL: `https://radiografia-analyzer.onrender.com` (o el nombre que elegiste)
- Panel de control: Podrás ver logs, métricas y configuración

## ⚠️ Consideraciones Importantes

### Modelo YOLO (`best.pt`)

El archivo `best.pt` es grande. Tienes 2 opciones:

**Opción A: Incluirlo en el repositorio**
```bash
# Asegúrate de que best.pt esté en el repo
git add best.pt
git commit -m "Agregar modelo YOLO"
git push
```

**Opción B: Usar Git LFS (recomendado para archivos grandes)**
```bash
# Instalar Git LFS
git lfs install

# Trackear archivos .pt
git lfs track "*.pt"
git add .gitattributes
git add best.pt
git commit -m "Usar Git LFS para modelo"
git push
```

### Archivos de Salida

La carpeta `imgfoto/` se creará dinámicamente en el servidor. Los archivos se perderán si el servicio se reinicia (esto es normal en Render Free).

### RAM y Procesamiento

- YOLO requiere memoria considerable
- El plan Free (512MB) puede ser limitado
- Considera el plan Starter para mejor rendimiento

## 🔧 Configuración Adicional

### Usar una Base de Datos (Opcional)

Si quieres guardar resultados permanentemente:

1. Crear una base de datos en Render
2. Agregar `psycopg2-binary` a requirements.txt
3. Modificar app.py para usar PostgreSQL

### Almacenamiento de Imagenes (Opcional)

Para guardar imágenes permanentemente, usa:
- **Cloudinary**: Para almacenamiento de imágenes
- **AWS S3**: Para archivos grandes
- **Render Disks**: Para persistencia de datos

## 📝 Comandos Útiles Post-Deployment

```bash
# Ver logs en tiempo real
# Ve a tu dashboard de Render → "Logs"

# Forzar re-deploy
# Dashboard → "Manual Deploy" → "Deploy latest commit"

# Ver variables de entorno
# Dashboard → "Environment" → "Environment Variables"
```

## 🐛 Troubleshooting

### Error: "Module not found"
- Verifica que todas las dependencias estén en `requirements.txt`
- Usa `pip freeze > requirements.txt` localmente

### Error: "Port already in use"
- Render asigna el puerto automáticamente (variable PORT)
- Código ya configurado para usar `os.environ.get('PORT')`

### Error: "Out of memory"
- Reduce `YOLO_IMG_SIZE` a 416 o 320
- Considera upgrade a plan con más RAM

### Aplicación muy lenta
- El plan Free se duerme después de inactividad
- Primera request después de dormir toma ~30 segundos
- Upgrade a plan Starter para mantenerlo activo

## 📞 Soporte

- Documentación Render: https://render.com/docs
- Foro: https://community.render.com

## ✅ Checklist Final

- [ ] Repositorio en GitHub creado y actualizado
- [ ] Archivos de configuración commiteados
- [ ] Modelo `best.pt` incluido en el repo
- [ ] Cuenta de Render creada
- [ ] Web Service configurado
- [ ] Deploy exitoso
- [ ] URL funcionando correctamente
- [ ] Prueba de análisis de radiografía exitosa

¡Tu aplicación está lista para deployar! 🎉
