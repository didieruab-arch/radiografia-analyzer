from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ultralytics import YOLO
import cv2
import os
from datetime import datetime
import base64
import numpy as np
import pandas as pd
try:
    from config import *
except ImportError:
    # Valores por defecto si no existe config.py
    PORT = 5000
    MODEL_PATH = 'best.pt'
    OUTPUT_FOLDER = 'imgfoto'
    CONFIDENCE_THRESHOLD = 0.60  # Solo mostrar detecciones con confianza >= 60%
    YOLO_IMG_SIZE = 640
    YOLO_IOU_THRESHOLD = 0.45

app = Flask(__name__)
CORS(app)  # Permitir solicitudes desde el frontend

# Mapeo de enfermedades: inglés -> español
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

# Mapeo de nombres del modelo YOLO a nombres en el Excel
YOLO_TO_EXCEL_MAPPING = {
    'Aortic_Enlargement': 'Agrandamiento Aórtico',
    'Cardiomegaly': 'Cardiomegalia',
    'Atelectasis': 'Atelectasia',
    'Consolidation': 'Consolidación',
    'Infiltration': 'Opacidad Pulmonar / Infiltración',
    'Lung_Opacity': 'Opacidad Pulmonar / Infiltración',
    'Pleural_Effusion': 'Derrame Pleural',
    'Pneumothorax': 'Neumotórax',
    'Pleural_Thickening': 'Engrosamiento Pleural',
    'Nodule-Mass': 'Nódulo-Masa',
    'Calcification': 'Calcificación',
    'ILD': 'EPI / Fibrosis Pulmonar',
    'Pulmonary_Fibrosis': 'EPI / Fibrosis Pulmonar',
    'Other_Lesion': 'Otra Lesión'
}

# Cargar el Excel una vez al inicio
EXCEL_FILE = 'infoenfermedades.xlsx'
disease_info_df = None

try:
    disease_info_df = pd.read_excel(EXCEL_FILE)
    print(f"✓ Excel cargado correctamente: {len(disease_info_df)} enfermedades")
except Exception as e:
    print(f"⚠ Error cargando Excel: {e}")

# Cargar el modelo YOLO
print(f"Cargando modelo YOLO desde {MODEL_PATH}...")
try:
    model = YOLO(MODEL_PATH)
    print(f"✓ Modelo cargado exitosamente")
    print(f"  Clases detectables: {list(model.names.values())}")
except Exception as e:
    print(f"✗ Error al cargar el modelo: {e}")
    model = None

# Crear carpeta de salida si no existe
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
    print(f"✓ Carpeta '{OUTPUT_FOLDER}' creada")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        # Verificar que el modelo esté cargado
        if model is None:
            return jsonify({'error': 'El modelo YOLO no está disponible. Verifica que best.pt exista.'}), 500
        
        if 'image' not in request.files:
            return jsonify({'error': 'No se encontró ninguna imagen'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'Nombre de archivo vacío'}), 400
        
        # Leer la imagen
        image_bytes = file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'error': 'No se pudo decodificar la imagen'}), 400
        
        print(f"\n{'='*50}")
        print(f"Analizando imagen: {file.filename}")
        print(f"Dimensiones: {img.shape[1]}x{img.shape[0]}")
        print(f"Umbral de confianza: {CONFIDENCE_THRESHOLD:.0%} (solo se mostrarán detecciones >= {CONFIDENCE_THRESHOLD:.0%})")
        
        # Realizar la predicción con YOLO (confianza mínima 60%)
        results = model(
            img,
            conf=CONFIDENCE_THRESHOLD,  # 0.60 = 60% mínimo
            iou=YOLO_IOU_THRESHOLD,
            imgsz=YOLO_IMG_SIZE
        )
        
        # Dibujar los bounding boxes en la imagen con porcentajes de confianza
        annotated_img = results[0].plot(
            conf=True,  # Mostrar porcentaje de confianza en cada bounding box
            line_width=3,  # Grosor de línea de los recuadros
            font_size=14,  # Tamaño de fuente para etiquetas
            labels=True  # Mostrar etiquetas con nombres
        )
        
        # Guardar la imagen con los bounding boxes
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f'analisis_{timestamp}.jpg'
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        cv2.imwrite(output_path, annotated_img)
        print(f"✓ Imagen guardada en: {output_path}")
        
        # Extraer información de las detecciones
        detections = []
        boxes = results[0].boxes
        
        print(f"Detecciones encontradas: {len(boxes)}")
        
        for i, box in enumerate(boxes):
            # Obtener información del bounding box
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            class_name_es = DISEASE_NAMES_ES.get(class_name, class_name)
            
            print(f"  [{i+1}] {class_name} ({class_name_es}) - Confianza: {confidence:.2%}")
            
            detections.append({
                'class': class_name,
                'class_es': class_name_es,
                'confidence': confidence,
                'bbox': [x1, y1, x2, y2]
            })
        
        # Convertir la imagen anotada a base64 para enviarla al frontend
        _, buffer = cv2.imencode('.jpg', annotated_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        print(f"{'='*50}\n")
        
        return jsonify({
            'success': True,
            'image_path': output_path,
            'image_base64': img_base64,
            'detections': detections,
            'num_detections': len(detections),
            'model_classes': list(model.names.values())
        })
    
    except Exception as e:
        print(f"✗ Error al analizar imagen: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/imgfoto/<filename>')
def serve_result(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

@app.route('/disease_info/<disease_name>')
def get_disease_info(disease_name):
    """Obtiene información detallada de una enfermedad desde el Excel"""
    try:
        if disease_info_df is None:
            return jsonify({'error': 'Excel no disponible'}), 500
        
        # Mapear el nombre del YOLO al nombre del Excel
        excel_name = YOLO_TO_EXCEL_MAPPING.get(disease_name, disease_name)
        
        # Buscar la enfermedad en el Excel
        disease_row = disease_info_df[disease_info_df['Patología'] == excel_name]
        
        if disease_row.empty:
            return jsonify({
                'success': False,
                'message': f'No se encontró información para: {disease_name}'
            })
        
        # Extraer la información
        row = disease_row.iloc[0]
        return jsonify({
            'success': True,
            'disease_name': disease_name,
            'disease_name_es': DISEASE_NAMES_ES.get(disease_name, disease_name),
            'excel_name': excel_name,
            'descripcion': row['Descripción Radiológica (Qué se ve)'],
            'causas': row['Principales Causas'],
            'medidas': row['Medidas y Soluciones Principales (Extendido)']
        })
    
    except Exception as e:
        print(f"Error obteniendo información de enfermedad: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/generate_report', methods=['POST'])
def generate_report():
    """Genera un reporte PDF profesional con toda la información del análisis"""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
        from io import BytesIO
        
        data = request.json
        detections = data.get('detections', [])
        analysis_date = data.get('analysis_date', datetime.now().strftime('%d/%m/%Y'))
        analysis_time = data.get('analysis_time', datetime.now().strftime('%H:%M:%S'))
        
        # Crear el PDF en memoria
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, 
                              topMargin=50, bottomMargin=50)
        
        # Contenedor de elementos
        elements = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a73e8'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1a73e8'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=6
        )
        
        # ENCABEZADO CON LOGO
        header_data = [
            [Paragraph('<b><font size=20 color="#1a73e8">LabVision</font></b>', styles['Normal']),
             Paragraph('<font size=10>Sistema de Análisis de Radiografías<br/>Powered by YOLOv11</font>', 
                      ParagraphStyle('right', parent=styles['Normal'], alignment=2))]
        ]
        header_table = Table(header_data, colWidths=[3*inch, 3*inch])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Línea separadora
        line_data = [['']]
        line_table = Table(line_data, colWidths=[6.5*inch])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#1a73e8')),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # TÍTULO
        elements.append(Paragraph('REPORTE DE ANÁLISIS RADIOLÓGICO', title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # INFORMACIÓN GENERAL
        info_data = [
            ['Fecha de análisis:', analysis_date, 'Hora:', analysis_time],
            ['Umbral de confianza:', '60%', 'Total detecciones:', str(len(detections))],
        ]
        info_table = Table(info_data, colWidths=[1.5*inch, 1.5*inch, 1.2*inch, 1.3*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f0fe')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#e8f0fe')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # RESUMEN DE DETECCIONES
        if len(detections) == 0:
            elements.append(Paragraph('RESULTADO DEL ANÁLISIS', heading_style))
            elements.append(Paragraph(
                '<font color="green"><b>✓ No se detectaron patologías</b></font><br/>'
                'La radiografía analizada no muestra hallazgos significativos con el umbral de confianza establecido (60%). '
                'Este resultado debe ser validado por un profesional médico.',
                normal_style
            ))
        else:
            # Agrupar detecciones por enfermedad
            disease_count = {}
            for det in detections:
                key = det.get('class_es', det.get('class'))
                if key not in disease_count:
                    disease_count[key] = {
                        'name_es': det.get('class_es', det.get('class')),
                        'name_en': det.get('class'),
                        'count': 0,
                        'confidences': []
                    }
                disease_count[key]['count'] += 1
                disease_count[key]['confidences'].append(det.get('confidence', 0))
            
            elements.append(Paragraph('RESUMEN DE PATOLOGÍAS DETECTADAS', heading_style))
            
            # Tabla de resumen
            summary_data = [['#', 'Patología', 'Detecciones', 'Confianza Máx.', 'Confianza Prom.']]
            for i, (key, disease) in enumerate(disease_count.items(), 1):
                max_conf = max(disease['confidences']) * 100
                avg_conf = sum(disease['confidences']) / len(disease['confidences']) * 100
                summary_data.append([
                    str(i),
                    f"{disease['name_es']}\n({disease['name_en']})",
                    str(disease['count']),
                    f"{max_conf:.1f}%",
                    f"{avg_conf:.1f}%"
                ])
            
            summary_table = Table(summary_data, colWidths=[0.4*inch, 2.5*inch, 1*inch, 1.2*inch, 1.2*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))
            elements.append(summary_table)
            elements.append(Spacer(1, 0.3*inch))
            
            # INFORMACIÓN DETALLADA DE CADA ENFERMEDAD
            elements.append(PageBreak())
            elements.append(Paragraph('INFORMACIÓN DETALLADA DE PATOLOGÍAS', heading_style))
            elements.append(Spacer(1, 0.2*inch))
            
            for disease in disease_count.values():
                # Obtener información del Excel
                excel_name = YOLO_TO_EXCEL_MAPPING.get(disease['name_en'], disease['name_en'])
                disease_row = disease_info_df[disease_info_df['Patología'] == excel_name]
                
                if not disease_row.empty:
                    row = disease_row.iloc[0]
                    
                    # Título de la enfermedad
                    elements.append(Paragraph(
                        f'<font color="#1a73e8"><b>{disease["name_es"]}</b></font> ({disease["name_en"]})',
                        ParagraphStyle('disease_title', parent=styles['Heading3'], fontSize=12, 
                                     textColor=colors.HexColor('#1a73e8'), spaceAfter=8)
                    ))
                    
                    # Descripción Radiológica
                    elements.append(Paragraph('<b>Descripción Radiológica:</b>', 
                                            ParagraphStyle('bold', parent=normal_style, fontName='Helvetica-Bold')))
                    elements.append(Paragraph(str(row['Descripción Radiológica (Qué se ve)']), normal_style))
                    elements.append(Spacer(1, 0.1*inch))
                    
                    # Principales Causas
                    elements.append(Paragraph('<b>Principales Causas:</b>', 
                                            ParagraphStyle('bold', parent=normal_style, fontName='Helvetica-Bold')))
                    elements.append(Paragraph(str(row['Principales Causas']), normal_style))
                    elements.append(Spacer(1, 0.1*inch))
                    
                    # Medidas y Soluciones
                    elements.append(Paragraph('<b>Medidas y Soluciones:</b>', 
                                            ParagraphStyle('bold', parent=normal_style, fontName='Helvetica-Bold')))
                    elements.append(Paragraph(str(row['Medidas y Soluciones Principales (Extendido)']), normal_style))
                    elements.append(Spacer(1, 0.2*inch))
                    
                    # Línea separadora
                    elements.append(Table([['']], colWidths=[6.5*inch], style=TableStyle([
                        ('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.grey),
                    ])))
                    elements.append(Spacer(1, 0.2*inch))
        
        # PIE DE PÁGINA
        elements.append(Spacer(1, 0.3*inch))
        footer_style = ParagraphStyle('footer', parent=styles['Normal'], fontSize=8, 
                                     textColor=colors.grey, alignment=TA_CENTER)
        elements.append(Paragraph(
            '<b>AVISO IMPORTANTE:</b> Este reporte es generado automáticamente mediante inteligencia artificial (YOLOv11) '
            'y tiene fines de apoyo diagnóstico únicamente. Los resultados deben ser validados por un profesional médico '
            'calificado. NO utilice este reporte como diagnóstico final sin supervisión médica apropiada.',
            ParagraphStyle('disclaimer', parent=styles['Normal'], fontSize=8, 
                         textColor=colors.HexColor('#d32f2f'), alignment=TA_JUSTIFY,
                         borderWidth=1, borderColor=colors.HexColor('#d32f2f'),
                         borderPadding=10, spaceAfter=10)
        ))
        
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph(
            f'Generado por LabVision - {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
            footer_style
        ))
        
        # Construir el PDF
        doc.build(elements)
        
        # Enviar el PDF
        buffer.seek(0)
        from flask import send_file
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'reporte_radiografia_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
            mimetype='application/pdf'
        )
    
    except Exception as e:
        print(f"Error generando PDF: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Endpoint para verificar el estado del servidor"""
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None,
        'model_classes': list(model.names.values()) if model else [],
        'output_folder': OUTPUT_FOLDER,
        'excel_loaded': disease_info_df is not None
    })

if __name__ == '__main__':
    # Usar puerto de Render si está disponible, sino usar el de config
    port = int(os.environ.get('PORT', PORT))
    
    print("\n" + "="*50)
    print("LabVision - Sistema de Análisis de Radiografías")
    print("="*50)
    print(f"Puerto: {port}")
    print(f"URL: http://localhost:{port}")
    print(f"Modelo: {MODEL_PATH}")
    print(f"Carpeta de salida: {OUTPUT_FOLDER}")
    print("="*50 + "\n")
    
    app.run(debug=False, port=port, host='0.0.0.0')
