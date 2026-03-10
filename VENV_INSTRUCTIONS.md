# Guía de Uso del Entorno Virtual (venv)

## ✅ El entorno virtual ya está creado y las dependencias instaladas

### 📌 Cómo ACTIVAR el entorno virtual

**En PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**En CMD (Símbolo del sistema):**
```cmd
.\venv\Scripts\activate.bat
```

**Cuando está activado verás:**
- El nombre `(venv)` aparece al inicio de tu línea de comandos
- Ejemplo: `(venv) PS C:\radiografia-analyzer>`

---

### 📌 Cómo DESACTIVAR el entorno virtual

Simplemente escribe en la terminal:
```powershell
deactivate
```

Esto funciona tanto en PowerShell como en CMD.

---

### 🚀 Cómo iniciar el proyecto

1. **Activar el entorno virtual:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Iniciar el servidor:**
   ```powershell
   python app.py
   ```
   O simplemente ejecuta:
   ```powershell
   .\start.bat
   ```

3. **Abrir el navegador en:**
   ```
   http://localhost:5000
   ```

---

### 📦 Paquetes instalados

✅ Flask - Framework web
✅ Flask-CORS - Manejo de CORS
✅ Ultralytics - YOLOv11
✅ OpenCV - Procesamiento de imágenes
✅ NumPy - Operaciones numéricas
✅ Pillow - Manipulación de imágenes
✅ PyTorch - Deep Learning (requerido por YOLO)

---

### ⚠️ Nota sobre PowerShell

Si obtienes un error de permisos al activar el entorno en PowerShell, ejecuta:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego intenta activar nuevamente.

---

### 🔄 Comandos rápidos

```powershell
# Activar venv + iniciar servidor (todo en uno)
.\venv\Scripts\Activate.ps1; python app.py

# Verificar que numpy está instalado
.\venv\Scripts\Activate.ps1; python -c "import numpy; print('NumPy version:', numpy.__version__)"

# Ver todos los paquetes instalados
.\venv\Scripts\Activate.ps1; pip list

# Actualizar un paquete
.\venv\Scripts\Activate.ps1; pip install --upgrade nombre_paquete
```

---

### 📁 Estructura del proyecto

```
radiografia-analyzer/
├── venv/                  ← Entorno virtual (NO subir a git)
├── imgfoto/              ← Imágenes analizadas
├── app.py                ← Servidor Flask con YOLO
├── best.pt               ← Modelo YOLOv11
├── index.html            ← Frontend
├── script.js             ← Lógica JavaScript
├── styles.css            ← Estilos
├── requirements.txt      ← Dependencias
├── config.py             ← Configuración
├── start.bat             ← Script de inicio rápido
└── VENV_INSTRUCTIONS.md  ← Este archivo
```

---

### 🎯 Resumen

| Acción | Comando |
|--------|---------|
| Activar | `.\venv\Scripts\Activate.ps1` |
| Desactivar | `deactivate` |
| Iniciar servidor | `python app.py` |
| Ver paquetes | `pip list` |
| Instalar paquete | `pip install nombre_paquete` |
