# Configuración de LabVision

# Puerto del servidor
PORT = 5000

# Ruta del modelo YOLO
MODEL_PATH = 'best.pt'

# Carpeta de salida para imágenes analizadas
OUTPUT_FOLDER = 'imgfoto'

# Nivel de confianza mínimo para detecciones (0-1)
# Solo se mostrarán detecciones con confianza >= 60%
CONFIDENCE_THRESHOLD = 0.60

# Tamaño máximo de archivo de imagen (en MB)
MAX_IMAGE_SIZE_MB = 16

# Formatos de imagen permitidos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}

# Configuración de YOLO
YOLO_IMG_SIZE = 640  # Tamaño de imagen para YOLO
YOLO_IOU_THRESHOLD = 0.45  # IoU threshold para NMS
