"""
Script de prueba para verificar que el modelo YOLO carga correctamente
y puede procesar imágenes.
"""

from ultralytics import YOLO
import cv2
import numpy as np

# Mapeo de enfermedades
DISEASE_NAMES_ES = {
    'Aortic_Enlargement': 'Agrandamiento Aórtico',
    'Atelectasis': 'Atelectasia',
    'Calcification': 'Calcificación',
    'Cardiomegaly': 'Cardiomegalia',
    'Consolidation': 'Consolidación',
    'ILD': 'Enfermedad Pulmonar Intersticial (EPI)',
    'Infiltration': 'Infiltración',
    'Lung_Opacity': 'Opacidad Pulmonar',
    'Nodule-Mass': 'Nódulo-Masa',
    'Other_Lesion': 'Otra Lesión',
    'Pleural_Effusion': 'Derrame Pleural',
    'Pleural_Thickening': 'Engrosamiento Pleural',
    'Pneumothorax': 'Neumotórax',
    'Pulmonary_Fibrosis': 'Fibrosis Pulmonar'
}

def test_model():
    print("="*60)
    print("TEST DE MODELO YOLO - LabVision")
    print("="*60)
    
    # Cargar modelo
    print("\n1. Cargando modelo best.pt...")
    try:
        model = YOLO('best.pt')
        print("   ✓ Modelo cargado exitosamente")
    except Exception as e:
        print(f"   ✗ Error al cargar modelo: {e}")
        return
    
    # Verificar clases
    print(f"\n2. Clases detectables por el modelo: {len(model.names)}")
    print("\n   Código | Nombre en inglés | Nombre en español")
    print("   " + "-"*56)
    for class_id, class_name in model.names.items():
        class_name_es = DISEASE_NAMES_ES.get(class_name, "Sin traducción")
        print(f"   {class_id:>6} | {class_name:<30} | {class_name_es}")
    
    # Crear imagen de prueba
    print("\n3. Creando imagen de prueba (negro)...")
    test_img = np.zeros((640, 640, 3), dtype=np.uint8)
    print("   ✓ Imagen de prueba creada")
    
    # Realizar predicción de prueba
    print("\n4. Realizando predicción de prueba...")
    try:
        results = model(test_img, verbose=False)
        print(f"   ✓ Predicción exitosa")
        print(f"   Detecciones encontradas: {len(results[0].boxes)}")
    except Exception as e:
        print(f"   ✗ Error en predicción: {e}")
        return
    
    print("\n" + "="*60)
    print("✓ TODOS LOS TESTS PASARON CORRECTAMENTE")
    print("="*60)
    print("\nEl sistema está listo para analizar radiografías.")
    print("Inicia el servidor con: python app.py")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_model()
