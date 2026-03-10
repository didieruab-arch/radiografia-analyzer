# Comandos Útiles - LabVision

## 🚀 Inicio Rápido

### Opción 1: Usar el script automático
```powershell
.\start.bat
```
Este script hace todo automáticamente: activa el venv e inicia el servidor.

### Opción 2: Manual
```powershell
# 1. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 2. Iniciar servidor
python app.py
```

---

## 📋 Gestión del Entorno Virtual

### Activar venv
```powershell
# PowerShell
.\venv\Scripts\Activate.ps1

# CMD
.\venv\Scripts\activate.bat
```

### Desactivar venv
```powershell
deactivate
```

### Verificar que está activado
Cuando está activado verás `(venv)` al inicio de la línea de comandos:
```
(venv) PS C:\radiografia-analyzer>
```

---

## 🔍 Verificación de Dependencias

### Verificar NumPy
```powershell
python -c "import numpy; print(numpy.__version__)"
```

### Verificar YOLO/Ultralytics
```powershell
python -c "import ultralytics; print(ultralytics.__version__)"
```

### Verificar OpenCV
```powershell
python -c "import cv2; print(cv2.__version__)"
```

### Verificar Flask
```powershell
python -c "import flask; print(flask.__version__)"
```

### Ver TODOS los paquetes instalados
```powershell
pip list
```

---

## 🔧 Mantenimiento

### Instalar un paquete nuevo
```powershell
pip install nombre_paquete
```

### Actualizar requirements.txt después de instalar algo nuevo
```powershell
pip freeze > requirements.txt
```

### Reinstalar todas las dependencias
```powershell
pip install -r requirements.txt --force-reinstall
```

### Actualizar pip
```powershell
python -m pip install --upgrade pip
```

---

## 🧪 Pruebas

### Probar que el modelo YOLO carga
```powershell
python -c "from ultralytics import YOLO; model = YOLO('best.pt'); print('Modelo cargado OK')"
```

### Probar el servidor sin navegador
```powershell
# En una terminal inicia el servidor:
python app.py

# En otra terminal, prueba el endpoint de salud:
curl http://localhost:5000/health
```

---

## 🐛 Solución de Problemas

### Error: "cannot be loaded because running scripts is disabled"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "No module named 'numpy'" (u otro módulo)
```powershell
# Asegúrate de que el venv esté activado
.\venv\Scripts\Activate.ps1

# Reinstala las dependencias
pip install -r requirements.txt
```

### El servidor no inicia
```powershell
# Verifica que best.pt existe
dir best.pt

# Verifica el puerto 5000 no esté en uso
netstat -ano | findstr :5000
```

### Limpiar caché de Python
```powershell
# Eliminar archivos __pycache__
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Force -Recurse

# Eliminar archivos .pyc
Get-ChildItem -Path . -Filter *.pyc -Recurse | Remove-Item -Force
```

---

## 📂 Gestión de Archivos

### Ver imágenes procesadas
```powershell
dir imgfoto
```

### Limpiar imágenes antiguas
```powershell
# Ver cuántas hay
(Get-ChildItem imgfoto -File).Count

# Eliminar todas
Remove-Item imgfoto\*.jpg
```

### Ver tamaño del entorno virtual
```powershell
"{0:N2} MB" -f ((Get-ChildItem venv -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB)
```

---

## 🌐 URLs Importantes

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:5000 |
| Health Check | http://localhost:5000/health |
| Endpoint de análisis | http://localhost:5000/analyze |
| Imágenes procesadas | http://localhost:5000/imgfoto/ |

---

## 💡 Tips

1. **Siempre activa el venv antes de trabajar**
2. **Usa `start.bat` para inicio rápido**
3. **Revisa la consola para ver logs del servidor**
4. **Las imágenes procesadas se guardan en `imgfoto/`**
5. **Presiona Ctrl+C para detener el servidor**

---

## 📚 Documentación

- Flask: https://flask.palletsprojects.com/
- Ultralytics YOLO: https://docs.ultralytics.com/
- OpenCV: https://docs.opencv.org/
- NumPy: https://numpy.org/doc/
