# LabVision - Análisis Inteligente de Radiografías

Sistema de análisis de radiografías usando YOLOv11 para detectar anomalías y enfermedades.

## 🚀 Deploy en Render

Este proyecto está preparado para deployarse en Render. Lee [DEPLOYMENT_RENDER.md](DEPLOYMENT_RENDER.md) para instrucciones completas.

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Instala las dependencias de Python:
```powershell
pip install -r requirements.txt
```

## Uso

1. Inicia el servidor backend:
```powershell
python app.py
```

2. Abre tu navegador y accede a:
```
http://localhost:5000
```

3. Sube una imagen de radiografía y haz clic en "Analizar Radiografía"

4. El sistema:
   - Procesará la imagen con el modelo YOLOv11 (`best.pt`)
   - Detectará anomalías y enfermedades
   - Dibujará bounding boxes en las áreas detectadas
   - Guardará la imagen anotada en la carpeta `imgfoto/`
   - Mostrará los resultados en la interfaz web

## Estructura del Proyecto

```
radiografia-analyzer/
├── app.py              # Servidor Flask con el modelo YOLO
├── best.pt             # Modelo YOLOv11 entrenado
├── index.html          # Interfaz web
├── script.js           # Lógica del frontend
├── styles.css          # Estilos
├── requirements.txt    # Dependencias de Python
├── imgfoto/           # Carpeta donde se guardan los resultados
└── README.md          # Este archivo
```

## Funcionamiento

1. **Frontend (HTML/JS)**: 
   - Permite al usuario subir una imagen
   - Envía la imagen al servidor Flask
   - Muestra los resultados del análisis

2. **Backend (Flask + YOLO)**:
   - Recibe la imagen
   - La procesa con el modelo YOLOv11
   - Detecta enfermedades/anomalías
   - Dibuja bounding boxes
   - Guarda la imagen anotada en `imgfoto/`
   - Devuelve los resultados al frontend

## Características

- ✅ Detección automática de anomalías en radiografías
- ✅ Visualización de bounding boxes en áreas detectadas
- ✅ Guardado automático de imágenes analizadas
- ✅ Reporte detallado con niveles de confianza
- ✅ Interfaz web intuitiva y responsive
- ✅ Descarga de reportes en formato texto

## Notas Importantes

- Los resultados son de apoyo diagnóstico únicamente
- Siempre consultar con un profesional médico certificado
- El modelo debe ser validado clínicamente antes de uso real
- Las imágenes analizadas se guardan en la carpeta `imgfoto/`

## Solución de Problemas

### El servidor no inicia
- Verifica que todas las dependencias estén instaladas
- Asegúrate de que el archivo `best.pt` exista en la carpeta principal

### Error al analizar imagen
- Verifica que el servidor esté corriendo (http://localhost:5000)
- Asegúrate de subir una imagen válida (JPG, PNG, etc.)
- Revisa la consola del navegador para más detalles

### La imagen no se guarda
- Verifica que la carpeta `imgfoto/` exista y tenga permisos de escritura

## Tecnologías

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python, Flask, Flask-CORS
- **IA**: YOLOv11 (Ultralytics)
- **Procesamiento**: OpenCV, NumPy
