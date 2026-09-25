# Sistema inteligente de detección de malware con Machine Learning y explicabilidad (XAI)

Trabajo de grado — Universidad Católica de Colombia, Facultad de Ingeniería, Programa de Ingeniería de Sistemas y Computación (2026).

**Autores:** Jhon Alexander Parra Olarte · Jhon David González García
**Docente:** Stefany Tatiana Ospina
**Director:** Jorge Ignacio Blanco, Magíster en Telecomunicaciones

## Descripción

Sistema que clasifica archivos ejecutables de Windows (PE: Win32, Win64 y .NET) como **maliciosos o benignos**
mediante **análisis estático** (el archivo nunca se ejecuta) y explica cada decisión con **SHAP** (y LIME como
técnica de contraste) en lenguaje comprensible para usuarios sin formación en ciberseguridad. Se construyó sobre
**EMBER2024** (Joyce et al., KDD 2025), el benchmark público más reciente para esta tarea, usando su extractor
oficial `thrember` (2.568 características estáticas), y se despliega en una aplicación web construida con Gradio.

## Resultados principales (corrida 1, septiembre de 2026)

| Indicador | Resultado |
|---|---|
| Datos (archivos únicos por SHA-256) | 548.997 de entrenamiento · 539.940 de prueba temporal · 4.868 de desafío (malware evasivo) |
| Selección de características | **15 de 2.568** (reducción del 99,42 %) conservando el 95,45 % del F1 de referencia |
| Modelo seleccionado | **Random Forest** (250 árboles) — F1 0,9251 · recall 0,9245 · precision 0,9258 · AUC-ROC 0,978 · FPR 7,41 % |
| Comparación | XGBoost F1 0,9222 · red neuronal densa F1 0,9085 |
| Malware evasivo (conjunto de desafío) | recall 57,3 % · AUC-ROC 0,907 · PR-AUC 0,295 |
| Explicabilidad | cobertura 100 % · fidelidad SHAP exacta · acuerdo SHAP-LIME (Jaccard top-5) 0,677 · 1,3 ms por explicación |
| Interfaz y pruebas | 9/9 pruebas funcionales · latencia p95: 1,5 s (1 MB), 6,1 s (5 MB), 21 s (20 MB) |
| Metas del anteproyecto | cumplidas: reducción ≥ 90 %, F1 conservado ≥ 95 %, cobertura 100 %; **no cumplidas:** F1 ≥ 0,95 (0,925), FPR ≤ 5 % (7,4 %), latencia < 10 s para 20 MB; SUS pendiente |

El cuadro completo está en `cuadro_cumplimiento_metas.csv` y todos los resúmenes en `resultados_para_documento.json`.

## Estructura del repositorio

```
├── TrabajoGrado_EMBER2024.ipynb        Notebook maestro (Google Colab): fases 1 a 4 + exportación de evidencias
├── datos/                              Composición del dataset construido y diccionario de las 2.568 características
├── fase1_seleccion_caracteristicas/    Ranking, curva K vs. F1, características seleccionadas, correlación
├── fase2_entrenamiento_modelos/        Búsqueda de hiperparámetros, comparación, matrices de confusión, curvas ROC/PR,
│                                       métricas por umbral/tipo/semana, predicciones sobre el desafío
├── fase3_explicabilidad/               Importancias SHAP, muestra explicada, acuerdo SHAP-LIME, ejemplos
├── fase4_interfaz/                     app_malware.py (motor + interfaz Gradio), pruebas funcionales y de rendimiento,
│                                       prueba exploratoria con archivos externos, cuestionario SUS,
│                                       ejecutar_interfaz_local.py + requisitos_interfaz.txt
├── figuras/                            Todas las figuras del documento (incluidas las capturas de la interfaz)
├── evidencias/                         Manifiesto e índice del paquete completo de evidencias (evidencias_proyecto.zip)
├── documentos/                         Documento de trabajo de grado y entregables anteriores
├── legacy_ember2018/                   Primera versión del proyecto (EMBER2018 y esqueleto Streamlit); solo trazabilidad
├── cuadro_cumplimiento_metas.csv · resultados_para_documento.json · registro_memoria.csv
└── README.md
```

Los datasets vectorizados (parquet, varios GB) y los modelos serializados (`.joblib`, `.keras`) no se versionan
(ver `.gitignore`); quedan en Google Drive y en el paquete `evidencias_proyecto.zip` que genera la celda de
exportación del notebook (el Random Forest comprimido pesa 138 MB).

## Cómo reproducir el proyecto (Google Colab)

1. Abrir `TrabajoGrado_EMBER2024.ipynb` en Google Colab y ejecutar las celdas **en orden**, empezando por la celda 0
   (monta Google Drive e instala `thrember`, el extractor oficial de EMBER2024, con `signify==0.7.1`).
2. Fase 1a descarga desde Hugging Face (`joyce8/EMBER2024`) los zip de Win32, Win64 y .NET, los lee en *streaming*
   y vectoriza por bloques (1,5–2,5 h). Fase 1b selecciona las características (≈ 25 min), Fase 2 entrena y compara
   los modelos (≈ 1 h), Fase 3 calcula las explicaciones (≈ 10 min) y Fase 4 construye la interfaz y ejecuta las
   pruebas (≈ 5 min).
3. Cada celda deja marcas de finalización en Drive: si la sesión se cae, basta con volver a correr desde la celda 0.
4. La celda de exportación genera `entregables_documento.zip` (figuras y tablas) y `evidencias_proyecto.zip`
   (paquete completo con un manifiesto que describe cada archivo).

Semilla fija (42) en todas las operaciones aleatorias; el notebook está diseñado para no superar ~4 GB de RAM.

## Cómo ejecutar la interfaz en un computador

```
cd fase4_interfaz
pip install -r requisitos_interfaz.txt
python ejecutar_interfaz_local.py ruta/a/evidencias_proyecto.zip
```

El script extrae del paquete de evidencias el modelo, el escalador, la configuración de explicabilidad y los
ejemplos, y abre la aplicación en http://127.0.0.1:7860. Requiere Python 3.10 a 3.12.

## Prueba exploratoria con archivos externos

Cuatro archivos PE benignos ajenos a EMBER2024 analizados a ciegas en un computador personal
(`fase4_interfaz/prueba_exploratoria_archivos_externos.csv`): la biblioteca `pythoncom311.dll` fue clasificada
como benigna (6,3 %) y los tres ejecutables sin firma (`Pythonwin.exe`, `pythonservice.exe` y un PE sintético
mínimo) como maliciosos (73,4 %, 73,4 % y 67,3 %). Los dos ejecutables reales comparten los valores de las 15
características seleccionadas, lo que ilustra el costo de la reducción de dimensionalidad y dónde se concentra la
tasa de falsos positivos del modelo: ejecutables sin firma Authenticode.

## Estado del proyecto

| Fase | Estado |
|---|---|
| Fase 1 — Conjunto de datos y selección de características (OE1) | ✅ Completa |
| Fase 2 — Entrenamiento, comparación y selección del modelo (OE2) | ✅ Completa (metas F1/FPR no alcanzadas; análisis en el documento) |
| Fase 3 — Integración de XAI (SHAP/LIME) (OE3) | ✅ Completa |
| Fase 4 — Interfaz, pruebas funcionales y de rendimiento (OE3) | ✅ Completa |
| Prueba de usabilidad SUS con usuarios | ⬜ Pendiente (plantilla y cuestionario en `fase4_interfaz/`) |

## Licencia

Proyecto académico — Universidad Católica de Colombia, 2026. EMBER2024 y `thrember` se distribuyen bajo licencia
Apache 2.0 (FutureComputing4AI).
