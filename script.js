// Smooth scrolling
function scrollToAnalysis() {
    document.getElementById('analisis').scrollIntoView({ behavior: 'smooth' });
}

// File upload handling
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const previewContainer = document.getElementById('previewContainer');
const imagePreview = document.getElementById('imagePreview');
const loading = document.getElementById('loading');
const resultsContainer = document.getElementById('resultsContainer');

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#00a8e8';
    uploadArea.style.background = '#e3f2fd';
});

uploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#0066cc';
    uploadArea.style.background = 'white';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#0066cc';
    uploadArea.style.background = 'white';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

// Click to upload
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

// Handle file
function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        alert('Por favor, selecciona un archivo de imagen válido.');
        return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        uploadArea.style.display = 'none';
        previewContainer.style.display = 'block';
        resultsContainer.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

// Clear image
function clearImage() {
    imagePreview.src = '';
    imagePreview.classList.remove('analyzed');
    fileInput.value = '';
    uploadArea.style.display = 'block';
    previewContainer.style.display = 'none';
    resultsContainer.style.display = 'none';
    document.getElementById('detectionsSummary').style.display = 'none';
    document.getElementById('imageTitle').style.display = 'none';
    document.getElementById('analyzeBtn').style.display = 'block';
}

// Show detections summary
function showDetectionsSummary(detections) {
    const summaryDiv = document.getElementById('detectionsSummary');
    const listDiv = document.getElementById('detectionsList');
    
    if (!detections || detections.length === 0) {
        listDiv.innerHTML = `
            <div class="no-detections">
                <i class="fas fa-info-circle"></i>
                <p><strong>No se detectaron enfermedades en esta radiografía</strong></p>
                <p style="margin-top: 1rem; font-size: 0.95rem;">
                    El sistema analiza 14 patologías pero solo muestra detecciones con <strong>confianza superior al 60%</strong>.
                    No se encontraron hallazgos que cumplan este criterio.
                </p>
                <p style="margin-top: 1rem; font-size: 0.9rem; color: var(--gray-color);">
                    Esto puede significar:
                    • La radiografía no presenta patologías detectables<br>
                    • Las anomalías presentes tienen baja confianza (&lt;60%)<br>
                    • La calidad de imagen no permite detección precisa
                </p>
                <p style="margin-top: 1rem; color: var(--warning-color); font-weight: 600;">
                    <i class="fas fa-exclamation-triangle"></i> 
                    Si sospecha que debería haber hallazgos, intente:
                </p>
                <ul style="text-align: left; margin: 1rem auto; max-width: 500px; line-height: 1.8;">
                    <li>Analizar con una imagen de mejor calidad y contraste</li>
                    <li>Asegurarse de que la imagen sea una radiografía de tórax clara</li>
                    <li>Verificar que la imagen tenga buena iluminación</li>
                    <li><strong>Consultar con un profesional médico para diagnóstico definitivo</strong></li>
                </ul>
            </div>
        `;
    } else {
        // Contar ocurrencias de cada enfermedad
        const diseaseCount = {};
        detections.forEach(det => {
            const key = det.class_es || det.class;
            if (!diseaseCount[key]) {
                diseaseCount[key] = {
                    name_es: det.class_es || det.class,
                    name_en: det.class,
                    count: 0,
                    maxConfidence: 0
                };
            }
            diseaseCount[key].count++;
            diseaseCount[key].maxConfidence = Math.max(
                diseaseCount[key].maxConfidence,
                det.confidence
            );
        });

        // Ordenar por confianza descendente
        const sortedDiseases = Object.values(diseaseCount).sort(
            (a, b) => b.maxConfidence - a.maxConfidence
        );

        // Crear HTML para cada enfermedad
        listDiv.innerHTML = sortedDiseases.map(disease => {
            const confidence = Math.round(disease.maxConfidence * 100);
            let confidenceClass = 'high';
            if (confidence < 50) confidenceClass = 'low';
            else if (confidence < 75) confidenceClass = 'medium';

            return `
                <div class="detection-item">
                    <div class="detection-item-header">
                        <div class="detection-name">
                            <i class="fas fa-exclamation-triangle"></i>
                            <div>
                                <div>${disease.name_es}</div>
                                <div class="detection-name-en">${disease.name_en}</div>
                            </div>
                        </div>
                        <div class="detection-confidence ${confidenceClass}">
                            ${confidence}%
                        </div>
                    </div>
                    ${disease.count > 1 ? `<div style="color: var(--gray-color); font-size: 0.9rem; margin-top: 0.5rem;">
                        <i class="fas fa-layer-group"></i> ${disease.count} detección(es)
                    </div>` : ''}
                </div>
            `;
        }).join('');
    }
    
    summaryDiv.style.display = 'block';
    
    // Scroll suave al resumen
    setTimeout(() => {
        summaryDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 300);
}

// Analyze image (con YOLO real)
async function analyzeImage() {
    // Verificar primero que hay un archivo antes de hacer cambios en la UI
    const file = fileInput.files[0];
    if (!file) {
        alert('Por favor, selecciona una imagen primero');
        return;
    }

    // Ahora sí, mostrar el loading y ocultar otros elementos
    loading.style.display = 'block';
    resultsContainer.style.display = 'none';

    try {

        // Crear FormData para enviar la imagen
        const formData = new FormData();
        formData.append('image', file);

        // Enviar la imagen al backend
        const response = await fetch('http://localhost:5000/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            alert('Error al analizar la imagen: ' + data.error);
            loading.style.display = 'none';
            previewContainer.style.display = 'block';
            return;
        }

        // Actualizar la imagen de vista previa con la imagen anotada (con bounding boxes)
        imagePreview.src = 'data:image/jpeg;base64,' + data.image_base64;
        
        // Agregar clase para estilo especial de imagen analizada
        imagePreview.classList.add('analyzed');

        // Guardar los resultados para el reporte
        window.analysisResults = data;

        // Ocultar botón de analizar (ya está analizado)
        document.getElementById('analyzeBtn').style.display = 'none';

        // Mostrar título de imagen analizada
        document.getElementById('imageTitle').style.display = 'block';

        // Mostrar la imagen con bounding boxes
        previewContainer.style.display = 'block';

        // Scroll suave a la imagen analizada
        previewContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });

        // Mostrar resumen de detecciones después de un momento
        setTimeout(() => {
            showDetectionsSummary(data.detections);
        }, 500);

        loading.style.display = 'none';
        showResults(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Error al conectar con el servidor. Asegúrate de que el servidor está corriendo.');
        loading.style.display = 'none';
        previewContainer.style.display = 'block';
    }
}

// Show results (solo con resultados reales de YOLO)
function showResults(data) {
    resultsContainer.style.display = 'block';
    resultsContainer.scrollIntoView({ behavior: 'smooth' });

    // Validar que tengamos datos del análisis
    if (!data) {
        console.error('No hay datos de análisis disponibles');
        return;
    }

    // Procesar resultados reales de YOLO
    const detections = data.detections || [];
    const numDetections = detections.length;

    let scenario;
    if (numDetections === 0) {
        // Sin detecciones - Análisis completado pero sin hallazgos
        scenario = {
            status: 'Sin Detecciones',
            statusClass: 'normal',
            confidence: 95,
            findings: [
                { area: 'Análisis Completo', status: 'No se detectaron las 14 patologías analizadas', icon: 'normal' },
                { area: 'YOLOv11', status: 'Modelo ejecutado correctamente', icon: 'normal' },
                { area: 'Imagen Procesada', status: 'Análisis finalizado sin hallazgos', icon: 'normal' },
                { area: 'Recomendación', status: 'Verificar calidad de imagen si sospecha patología', icon: 'normal' }
            ],
            recommendations: [
                'El sistema no detectó ninguna de las 14 enfermedades que puede identificar.',
                'Esto NO garantiza ausencia total de patologías, solo que no se detectaron estas específicas.',
                'Si tiene síntomas o sospecha de alguna condición, consulte con un médico.',
                'Los resultados del análisis son solo de apoyo y no reemplazan el criterio médico profesional.',
                'Considere analizar con una imagen de mejor calidad si los resultados no son los esperados.'
            ]
        };
    } else {
        // Con detecciones
        const avgConfidence = Math.round(
            detections.reduce((sum, det) => sum + det.confidence, 0) / numDetections * 100
        );

        const findings = [];
        const recommendations = [
            `Se detectaron ${numDetections} hallazgo(s) en la radiografía mediante análisis con visión artificial.`,
            'Es FUNDAMENTAL que un profesional médico evalúe estos resultados.',
            'Consulte con un radiólogo certificado lo antes posible para confirmación diagnóstica.',
            'NO utilice estos resultados como diagnóstico definitivo.'
        ];

        // Agrupar detecciones por clase
        const detectionsByClass = {};
        detections.forEach(det => {
            const className_es = det.class_es || det.class;
            if (!detectionsByClass[className_es]) {
                detectionsByClass[className_es] = {
                    class_en: det.class,
                    class_es: className_es,
                    detections: []
                };
            }
            detectionsByClass[className_es].detections.push(det);
        });

        // Crear hallazgos basados en las detecciones (usar nombres en español)
        let findingIndex = 0;
        for (const [className_es, classData] of Object.entries(detectionsByClass)) {
            const count = classData.detections.length;
            const avgConf = Math.round(
                classData.detections.reduce((sum, d) => sum + d.confidence, 0) / count * 100
            );
            
            findings.push({
                area: className_es,
                status: `${count} detección(es) - Confianza: ${avgConf}%`,
                icon: avgConf >= 75 ? 'danger' : (avgConf >= 50 ? 'warning' : 'normal')
            });

            // Agregar recomendación específica por enfermedad
            const confText = avgConf >= 75 ? 'alta' : (avgConf >= 50 ? 'media' : 'baja');
            recommendations.push(`• ${className_es}: Detectada ${count} vez(ces) con confianza ${confText} (${avgConf}%). Requiere evaluación médica.`);
            findingIndex++;
        }

        // Completar con hallazgos normales si hay menos de 4
        while (findings.length < 4) {
            findings.push({
                area: 'Otras áreas',
                status: 'Sin anomalías adicionales',
                icon: 'normal'
            });
        }

        scenario = {
            status: 'Detecciones Encontradas',
            statusClass: numDetections > 2 ? 'danger' : 'warning',
            confidence: avgConfidence,
            findings: findings.slice(0, 4),
            recommendations: recommendations
        };
    }

    updateResultsUI(scenario);
}

function updateResultsUI(scenario) {
    // Actualizar estado general
    const statusBadge = document.getElementById('statusBadge');
    statusBadge.textContent = scenario.status;
    statusBadge.className = `status-badge ${scenario.statusClass}`;

    // Actualizar barra de confianza
    const confidenceBar = document.getElementById('confidenceBar');
    const confidenceValue = document.getElementById('confidenceValue');
    confidenceBar.style.width = scenario.confidence + '%';
    confidenceValue.textContent = scenario.confidence + '%';

    // Actualizar hallazgos
    scenario.findings.forEach((finding, index) => {
        const card = document.getElementById(`finding${index + 1}`);
        const icon = card.querySelector('.finding-icon');
        const title = card.querySelector('h4');
        const status = card.querySelector('.finding-status');

        icon.className = `finding-icon ${finding.icon}`;
        icon.innerHTML = finding.icon === 'normal' ? '<i class="fas fa-check"></i>' : 
                        finding.icon === 'warning' ? '<i class="fas fa-exclamation-triangle"></i>' : 
                        '<i class="fas fa-times"></i>';
        
        title.textContent = finding.area;
        status.textContent = finding.status;
        
        card.className = `finding-card ${finding.icon}`;
    });

    // Actualizar recomendaciones
    const recommendationsList = document.getElementById('recommendationsList');
    recommendationsList.innerHTML = '';
    scenario.recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        recommendationsList.appendChild(li);
    });
}

// Download report
async function downloadReport() {
    // Crear un reporte con los resultados reales
    if (!window.analysisResults || !window.analysisResults.detections) {
        alert('No hay resultados de análisis para generar el reporte');
        return;
    }

    let detailsSection = '';
    let summarySection = '';
    let diseaseInfoSection = '';
    
    const detections = window.analysisResults.detections;
    
    // Resumen de enfermedades
    summarySection = '\n' + '='.repeat(80) + '\nRESUMEN DE ENFERMEDADES DETECTADAS\n' + '='.repeat(80) + '\n\n';
    
    if (detections.length === 0) {
        summarySection += 'No se detectaron enfermedades en la radiografía.\n\n';
    } else {
        // Agrupar por enfermedad
        const diseaseCount = {};
        detections.forEach(det => {
            const key = det.class_es || det.class;
            if (!diseaseCount[key]) {
                diseaseCount[key] = {
                    name_es: det.class_es || det.class,
                    name_en: det.class,
                    count: 0,
                    confidences: []
                };
            }
            diseaseCount[key].count++;
            diseaseCount[key].confidences.push(det.confidence);
        });

        // Crear resumen
        Object.values(diseaseCount).forEach((disease, i) => {
            const avgConf = disease.confidences.reduce((a, b) => a + b, 0) / disease.confidences.length;
            const maxConf = Math.max(...disease.confidences);
            
            summarySection += `${i + 1}. ${disease.name_es} (${disease.name_en})\n`;
            summarySection += `   Número de detecciones: ${disease.count}\n`;
            summarySection += `   Confianza máxima: ${(maxConf * 100).toFixed(2)}%\n`;
            summarySection += `   Confianza promedio: ${(avgConf * 100).toFixed(2)}%\n\n`;
        });

        // Obtener información detallada del Excel para cada enfermedad
        diseaseInfoSection = '\n' + '='.repeat(80) + '\nINFORMACIÓN DETALLADA DE ENFERMEDADES\n' + '='.repeat(80) + '\n\n';
        
        const uniqueDiseases = Object.values(diseaseCount);
        for (const disease of uniqueDiseases) {
            try {
                const response = await fetch(`http://localhost:5000/disease_info/${disease.name_en}`);
                const data = await response.json();
                
                if (data.success) {
                    diseaseInfoSection += `\n${'─'.repeat(80)}\n`;
                    diseaseInfoSection += `ENFERMEDAD: ${disease.name_es} (${disease.name_en})\n`;
                    diseaseInfoSection += `${'─'.repeat(80)}\n\n`;
                    diseaseInfoSection += `DESCRIPCIÓN RADIOLÓGICA (Qué se ve):\n${data.descripcion}\n\n`;
                    diseaseInfoSection += `PRINCIPALES CAUSAS:\n${data.causas}\n\n`;
                    diseaseInfoSection += `MEDIDAS Y SOLUCIONES:\n${data.medidas}\n\n`;
                } else {
                    diseaseInfoSection += `\n${disease.name_es}: No se encontró información adicional.\n\n`;
                }
            } catch (error) {
                console.error(`Error obteniendo info de ${disease.name_en}:`, error);
                diseaseInfoSection += `\n${disease.name_es}: Error al obtener información adicional.\n\n`;
            }
        }
    }
    
    // Detalle de cada detección
    detailsSection = '\n' + '='.repeat(80) + '\nDETALLE DE DETECCIONES INDIVIDUALES\n' + '='.repeat(80) + '\n\n';
    detections.forEach((det, i) => {
        detailsSection += `Detección #${i + 1}:\n`;
        detailsSection += `  Enfermedad (ES): ${det.class_es || det.class}\n`;
        detailsSection += `  Enfermedad (EN): ${det.class}\n`;
        detailsSection += `  Confianza: ${(det.confidence * 100).toFixed(2)}%\n`;
        detailsSection += `  Ubicación (x1,y1,x2,y2): [${det.bbox.map(n => n.toFixed(0)).join(', ')}]\n\n`;
    });

    const reportContent = `
${'='.repeat(80)}
REPORTE DE ANÁLISIS DE RADIOGRAFÍA - LabVision
${'='.repeat(80)}

Fecha: ${new Date().toLocaleDateString('es-ES')}
Hora: ${new Date().toLocaleTimeString('es-ES')}

RESULTADO DEL ANÁLISIS:
${document.getElementById('statusBadge').textContent}

NIVEL DE CONFIANZA GENERAL:
${document.getElementById('confidenceValue').textContent}
${summarySection}${diseaseInfoSection}${detailsSection}
${'='.repeat(80)}
HALLAZGOS EN ANÁLISIS GENERAL
${'='.repeat(80)}

${Array.from(document.querySelectorAll('.finding-card')).map((card, i) => 
    `${i + 1}. ${card.querySelector('h4').textContent}: ${card.querySelector('.finding-status').textContent}`
).join('\n')}

${'='.repeat(80)}
RECOMENDACIONES
${'='.repeat(80)}

${Array.from(document.querySelectorAll('#recommendationsList li')).map((li, i) => 
    `${i + 1}. ${li.textContent}`
).join('\n')}

${'='.repeat(80)}
INFORMACIÓN ADICIONAL
${'='.repeat(80)}

Imagen analizada guardada en: ${window.analysisResults ? window.analysisResults.image_path : 'N/A'}

${'='.repeat(80)}
AVISO IMPORTANTE
${'='.repeat(80)}

Este reporte es generado automáticamente por LabVision mediante YOLOv11.
Los resultados son de apoyo diagnóstico y deben ser validados por un profesional médico.
NO utilice este reporte como diagnóstico final sin supervisión médica.

Generado por: LabVision - Sistema de Análisis de Radiografías
Fecha de generación: ${new Date().toLocaleString('es-ES')}
    `;

    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `reporte_radiografia_${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);

    // Mostrar mensaje de éxito
    alert('✓ Reporte descargado exitosamente');
}

// Reset analysis
function resetAnalysis() {
    clearImage();
    document.getElementById('detectionsSummary').style.display = 'none';
    document.getElementById('detectionsList').innerHTML = '';
    window.analysisResults = null;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Form submission
function handleSubmit(e) {
    e.preventDefault();
    alert('¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.');
    e.target.reset();
}

// Smooth scroll for all navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Add animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.service-card, .stat-card, .finding-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});
