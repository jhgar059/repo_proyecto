# Manifiesto de evidencias — Trabajo de grado: detección de malware con ML y XAI (EMBER2024)

Generado: 2026-09-22 23:29:29 · Entorno: Google Colab · Carpeta base: `/content/drive/MyDrive/trabajo_grado_malware/ember2024`

Archivos presentes: **90** · pendientes: **4** · omitidos del zip por tamaño: **0**

Resumen de la corrida: {"K_seleccionado": 15, "pct_reduccion": 99.42, "modelo_seleccionado": "Random Forest", "f1_prueba_temporal": 0.9251361573513851, "fpr": 0.07414981106912648, "recall_challenge": 0.5729252259654889, "n_train": 548997, "n_test": 539940, "n_challenge": 4868}

Cómo abrir los `.parquet`: `import pandas as pd; df = pd.read_parquet('archivo.parquet')` (o `pip install pyarrow`). Las columnas `f###` son posiciones del vector EMBER2024; su nombre legible está en `01_dataset/diccionario_caracteristicas.csv` y, para las seleccionadas, en `02_seleccion_caracteristicas/caracteristicas_seleccionadas.csv`.

## 00_resumen

| Archivo | Estado | Tamaño (MB) | Descripción |
|---|---|---|---|
| `cuadro_cumplimiento_metas.csv` | presente | 0.000 | Cuadro de cumplimiento de las metas del anteproyecto. |
| `registro_memoria.csv` | presente | 0.002 | Registro del uso de RAM del proceso en cada punto de control (evidencia de que la corrida cabe en Colab). |
| `resultados_para_documento.json` | presente | 0.020 | Consolidado de los resúmenes de todas las fases + configuración usada. |

## 01_dataset

| Archivo | Estado | Tamaño (MB) | Descripción |
|---|---|---|---|
| `diccionario_caracteristicas.csv` | presente | 0.107 | Diccionario completo: nombre legible y grupo de cada una de las 2.568 posiciones del vector. |
| `diccionario_grupos.csv` | presente | 0.001 | Diccionario de datos por grupo: los 12 grupos del vector EMBER2024, n.º de variables y descripción. |
| `distribucion_por_semana.csv` | presente | 0.016 | Número de archivos por semana y clase en cada split (cobertura temporal del muestreo). |
| `resumen_datos.csv` | presente | 0.000 | Composición del dataset construido: archivos por split (train/test/challenge), tipo PE y clase, con rango de semanas. |
| `resumen_datos.json` | presente | 0.001 | Igual que el CSV, con totales, fracciones de muestreo y número de características. |

## 02_seleccion_caracteristicas

| Archivo | Estado | Tamaño (MB) | Descripción |
|---|---|---|---|
| `caracteristicas_seleccionadas.csv` | presente | 0.001 | Tabla de las K características seleccionadas: posición, columna, nombre legible, grupo, importancia y puesto en el ranking. |
| `challenge_reducido.parquet` | presente | 0.403 | BASE DE DATOS REDUCIDA del conjunto de desafío (malware evasivo): mismas columnas. |
| `challenge_reducido_muestra_5000filas.csv` | presente | 0.832 | Primeras 4868 filas de challenge_reducido.parquet en CSV (para abrir en Excel); el parquet tiene 4,868 filas. |
| `columnas_constantes.csv` | presente | 0.002 | Variables eliminadas por ser constantes en la muestra. |
| `correlacion_seleccionadas.csv` | presente | 0.002 | Matriz de correlación de Pearson entre las K características seleccionadas. |
| `curva_k_vs_f1.csv` | presente | 0.000 | Curva K vs. F1: F1, % de reducción y % del F1 de referencia conservado para cada K probado. |
| `fase1_resumen.json` | presente | 0.003 | KPIs de la Fase 1: tamaño de la muestra, limpieza, F1 de referencia, K elegido, % de reducción, cumplimiento de metas. |
| `grupos_en_seleccion.csv` | presente | 0.000 | Cuántas características aporta cada grupo del vector al subconjunto seleccionado. |
| `importancia_extratrees_completa.csv` | presente | 0.158 | Ranking completo de importancia (Extra Trees, Gini) de todas las variables limpias, con nombre y grupo. |
| `muestra_seleccion_sha256.csv.gz` | presente | 5.498 | SHA-256, clase y partición (entrenamiento/validación) de cada archivo de la muestra usada para seleccionar características. |
| `ranking_caracteristicas.json` | presente | 0.007 | Ranking del top preliminar, candidatos tras el filtro de correlación y F1 de referencia. |
| `redundantes_descartadas.csv` | presente | 0.002 | Variables descartadas por redundancia (|r| > umbral): con cuál estaban correlacionadas y el valor de |r|. |
| `seleccion_final.json` | presente | 0.001 | Regla aplicada y lista de las K columnas seleccionadas (con nombres y grupos). |
| `test_reducido.parquet` | presente | 42.038 | BASE DE DATOS REDUCIDA de prueba temporal (semanas 53-64): mismas columnas. |
| `test_reducido_muestra_5000filas.csv` | presente | 0.816 | Primeras 5000 filas de test_reducido.parquet en CSV (para abrir en Excel); el parquet tiene 539,940 filas. |
| `train_reducido.parquet` | presente | 43.428 | BASE DE DATOS REDUCIDA de entrenamiento: K características seleccionadas + metadatos (sha256, label, tipo, fecha, semana, familia, comportamiento). |
| `train_reducido_muestra_5000filas.csv` | presente | 0.820 | Primeras 5000 filas de train_reducido.parquet en CSV (para abrir en Excel); el parquet tiene 548,997 filas. |

## 03_modelos

| Archivo | Estado | Tamaño (MB) | Descripción |
|---|---|---|---|
| `busqueda_hiperparametros_random_forest.csv` | presente | 0.000 | Búsqueda aleatoria de hiperparámetros de Random Forest: combinaciones probadas, F1 medio/desv. en validación cruzada y tiempo. |
| `busqueda_hiperparametros_xgboost.csv` | presente | 0.001 | Búsqueda aleatoria de hiperparámetros de XGBoost: combinaciones probadas, F1 medio/desv. en validación cruzada y tiempo. |
| `curvas_precision_recall.csv` | presente | 0.434 | Puntos (recall, precisión) de la curva precisión-recall de cada modelo. |
| `curvas_roc.csv` | presente | 0.613 | Puntos (FPR, TPR, umbral) de la curva ROC de cada modelo. |
| `dnn.keras` | presente | 0.176 | Red neuronal densa entrenada (Keras). |
| `dnn_info.json` | presente | 0.000 | Red neuronal: arquitectura, épocas efectivas, tiempo de entrenamiento y tamaño. |
| `fase2_comparacion_modelos.csv` | presente | 0.000 | Tabla comparativa de modelos (métricas principales sobre la prueba temporal y el desafío). |
| `fase2_comparacion_modelos_completa.csv` | presente | 0.001 | Tabla comparativa con TODAS las métricas escalares (incluye conteos de la matriz de confusión, PR-AUC, latencias, tamaño del modelo). |
| `fase2_resumen.json` | presente | 0.006 | Resumen completo de la Fase 2: métricas de cada modelo, hiperparámetros, modelo seleccionado, criterio y cumplimiento de metas. |
| `historia_entrenamiento_dnn.csv` | presente | 0.003 | Historia de entrenamiento de la red neuronal por época (pérdida, AUC y accuracy en entrenamiento y validación). |
| `matrices_confusion.csv` | presente | 0.000 | MATRIZ DE CONFUSIÓN (validación sobre la prueba temporal) de cada modelo: TN, FP, FN, TP, FPR, FNR y accuracy. |
| `metricas_por_semana.csv` | presente | 0.002 | F1, recall y FPR por semana del conjunto de prueba (deriva temporal), con el número de archivos por semana. |
| `metricas_por_tipo.csv` | presente | 0.001 | Métricas por tipo de archivo (Win32, Win64, .NET) para cada modelo, con el número de archivos de cada grupo. |
| `metricas_vs_umbral.csv` | presente | 0.002 | Precision, recall, F1, FPR, FNR y recall en el desafío para umbrales de decisión de 0,1 a 0,9. |
| `modelo_seleccionado.json` | presente | 0.000 | Modelo seleccionado, criterio de selección, umbral y columnas usadas. |
| `predicciones_challenge.csv` | presente | 0.480 | Predicción por archivo del conjunto de desafío: sha256, tipo y probabilidad de malware de cada modelo. |
| `predicciones_test.parquet` | presente | 37.203 | Predicción por archivo de la prueba temporal: sha256, tipo, semana, clase real y probabilidad de malware de cada modelo. |
| `random_forest.joblib` | presente | 138.027 | Modelo Random Forest entrenado (joblib comprimido). |
| `random_forest_info.json` | presente | 0.000 | Random Forest: mejores hiperparámetros, F1 de validación cruzada, tiempo de entrenamiento, tamaño y n.º de nodos. |
| `reportes_clasificacion.csv` | presente | 0.001 | Reporte de clasificación por clase (precision, recall, F1, soporte) y promedios macro/ponderado de cada modelo. |
| `scaler.joblib` | presente | 0.001 | StandardScaler ajustado con el entrenamiento (necesario para reproducir las predicciones). |
| `xgboost.joblib` | presente | 0.559 | Modelo XGBoost entrenado (joblib comprimido). |
| `xgboost_info.json` | presente | 0.000 | XGBoost: mejores hiperparámetros, F1 de validación cruzada, tiempo de entrenamiento y tamaño. |

## 04_explicabilidad

| Archivo | Estado | Tamaño (MB) | Descripción |
|---|---|---|---|
| `acuerdo_shap_lime_por_instancia.csv` | presente | 0.014 | Acuerdo SHAP-LIME por archivo: los 5 factores de cada técnica, coincidencias, índice de Jaccard y tiempo de LIME. |
| `explicaciones_ejemplos.txt` | presente | 0.002 | Explicaciones en lenguaje natural de los ejemplos malicioso y benigno usados en las figuras. |
| `fase3_resumen.json` | presente | 0.004 | Indicadores de explicabilidad: cobertura, fidelidad de SHAP, acuerdo SHAP-LIME, tiempos, top-10 global y ejemplos explicados. |
| `lime_ejemplo_malicioso.html` | presente | 1.175 | Explicación LIME interactiva (HTML) del ejemplo malicioso. |
| `muestra_explicada.csv` | presente | 1.680 | Muestra explicada archivo por archivo: clase real, probabilidad, veredicto, nivel de riesgo y explicación en lenguaje natural. |
| `shap_importancia_global.csv` | presente | 0.001 | Importancia global SHAP (media de |SHAP| y SHAP medio) de cada característica seleccionada, con nombre y grupo. |
| `shap_importancia_por_grupo.csv` | presente | 0.000 | Aporte de cada grupo de características a las decisiones del modelo (suma de |SHAP| medio). |
| `shap_valores_muestra.parquet` | presente | 0.253 | Valores SHAP de cada archivo de la muestra explicada (una columna por característica) + sha256, clase y probabilidad. |
| `xai_config.joblib` | presente | 0.001 | Configuración de explicabilidad usada por la interfaz (plantillas por grupo, valor base, escala). |

## 05_interfaz_y_pruebas

| Archivo | Estado | Tamaño (MB) | Descripción |
|---|---|---|---|
| `app_malware.py` | presente | 0.012 | Código fuente de la aplicación (motor AnalizadorMalware + interfaz Gradio). |
| `archivos_de_prueba.csv` | presente | 0.000 | Identificación (tamaño y SHA-256) de los ejecutables sintéticos usados en las pruebas. |
| `cuestionario_SUS.txt` | presente | 0.001 | Cuestionario SUS aplicado a los participantes. |
| `ejemplo_resultado_analisis.json` | presente | 0.002 | Respuesta completa del motor de análisis para un ejemplo (veredicto, probabilidad, riesgo, factores y frases). |
| `ejemplos_demo.parquet` | presente | 0.011 | Archivos de ejemplo cargados en la interfaz (vectores reducidos, etiqueta real, tipo y sha256). |
| `fase4_pruebas.json` | presente | 0.003 | Resumen JSON de las pruebas funcionales y de rendimiento. |
| `fase4_sus.json` | presente | 0.000 | Resumen SUS: promedio, desviación, IC 95 %, calificación y cumplimiento de la meta (o estado pendiente). |
| `fig_interfaz_gradio.png` | PENDIENTE (aún no generado) |  | Captura de pantalla de la interfaz (la toma el usuario al lanzar la app). |
| `pruebas_funcionales.csv` | presente | 0.001 | Pruebas funcionales PF-01 a PF-09: descripción, resultado PASA/FALLA y detalle. |
| `pruebas_funcionales_detalle.json` | presente | 0.011 | Respuesta completa del analizador en cada prueba funcional. |
| `pruebas_rendimiento.csv` | presente | 0.000 | Latencia de extremo a extremo por tamaño de archivo: p50, p95, máximo, desglose extracción/predicción y cumplimiento de la meta. |
| `pruebas_rendimiento_detalle.csv` | presente | 0.003 | Todas las mediciones individuales de las pruebas de rendimiento (una fila por repetición). |
| `sus_puntajes_por_participante.csv` | PENDIENTE (aún no generado) |  | Puntaje SUS calculado por participante (solo existe cuando hay respuestas reales). |
| `sus_respuestas.csv` | presente | 0.000 | Respuestas SUS registradas (plantilla; se diligencia con participantes reales). |

## 06_figuras

| Archivo | Estado | Tamaño (MB) | Descripción |
|---|---|---|---|
| `fig_acuerdo_shap_lime.png` | presente | 0.057 | Distribución del índice de Jaccard entre los top-5 de SHAP y LIME. |
| `fig_busqueda_hiperparametros.png` | presente | 0.121 | F1 de validación cruzada de cada combinación probada en la búsqueda de hiperparámetros. |
| `fig_comparacion_modelos.png` | presente | 0.080 | Comparación de F1, recall, precisión, AUC-ROC y recall en el desafío de los tres modelos. |
| `fig_composicion_dataset.png` | presente | 0.086 | Composición del subconjunto PE de EMBER2024 por split, tipo y clase. |
| `fig_correlacion_seleccionadas.png` | presente | 0.132 | Mapa de calor de la correlación entre las K características seleccionadas. |
| `fig_curva_k_vs_f1.png` | presente | 0.103 | Curva K vs. % del F1 de referencia conservado, con la meta y el K seleccionado. |
| `fig_desempeno_por_tipo.png` | presente | 0.062 | F1 por tipo de archivo y recall por tipo en el conjunto de desafío. |
| `fig_dnn_historia.png` | presente | 0.117 | Pérdida y AUC por época de la red neuronal (entrenamiento vs. validación). |
| `fig_f1_por_semana.png` | presente | 0.141 | Deriva temporal: F1 por semana del conjunto de prueba. |
| `fig_importancia_topk.png` | presente | 0.214 | Importancia (Extra Trees) de las K características seleccionadas, coloreadas por grupo. |
| `fig_interfaz_gradio.png` | PENDIENTE (aún no generada) |  | Captura de pantalla de la interfaz Gradio. |
| `fig_latencia_por_tamano.png` | presente | 0.082 | Latencia de análisis por tamaño de archivo (desglose y p95 frente a la meta). |
| `fig_lime_ejemplo.png` | presente | 0.124 | Explicación LIME del mismo archivo malicioso (contraste con SHAP). |
| `fig_matrices_confusion.png` | presente | 0.116 | Matrices de confusión de los tres modelos sobre la prueba temporal. |
| `fig_pr_modelos.png` | presente | 0.090 | Curvas precisión-recall de los tres modelos. |
| `fig_roc_modelos.png` | presente | 0.172 | Curvas ROC (escala lineal y logarítmica) de los tres modelos. |
| `fig_shap_beeswarm.png` | presente | 0.295 | Resumen SHAP (beeswarm): dirección y magnitud del efecto de cada característica. |
| `fig_shap_global_barras.png` | presente | 0.199 | Importancia global SHAP (media de |SHAP|) del modelo seleccionado. |
| `fig_shap_local_benigno.png` | presente | 0.207 | Explicación local SHAP (waterfall) de un archivo benigno. |
| `fig_shap_local_malicioso.png` | presente | 0.208 | Explicación local SHAP (waterfall) de un archivo malicioso. |
| `fig_shap_por_grupo.png` | presente | 0.078 | Aporte de cada grupo de características a las decisiones (SHAP). |
| `fig_sus_resultados.png` | PENDIENTE (aún no generada) |  | Puntajes SUS por participante y promedio por ítem (con respuestas reales). |
| `fig_tiempos_modelos.png` | presente | 0.052 | Tiempo de entrenamiento y latencia de predicción por modelo. |

## Pendientes

- `05_interfaz_y_pruebas/fig_interfaz_gradio.png`: Captura de pantalla de la interfaz (la toma el usuario al lanzar la app).
- `05_interfaz_y_pruebas/sus_puntajes_por_participante.csv`: Puntaje SUS calculado por participante (solo existe cuando hay respuestas reales).
- `06_figuras/fig_interfaz_gradio.png`: Captura de pantalla de la interfaz Gradio.
- `06_figuras/fig_sus_resultados.png`: Puntajes SUS por participante y promedio por ítem (con respuestas reales).
