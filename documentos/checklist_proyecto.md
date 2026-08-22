# Checklist completo — Trabajo de Grado
## Sistema inteligente basado en ML para detección de malware

*Estado al cierre de la semana 3 (16 semanas totales)*

---

## FASE 1 — Análisis y selección de características (Semanas 1–4)

- [x] Revisar datasets públicos disponibles (EMBER, CIC-MalMem-2022, VirusShare)
- [x] Definir y justificar el dataset principal (EMBER) y el complementario (CIC-MalMem-2022)
- [x] Diseñar el flujo de limpieza y preprocesamiento (nulos, columnas constantes, estandarización)
- [x] Construir el pipeline de selección de características (Extra Trees Classifier + análisis de correlación)
- [x] Validar el pipeline con un dataset piloto (prueba metodológica, datos sintéticos)
- [ ] **Descargar EMBER y CIC-MalMem-2022 reales**
- [ ] Ejecutar la limpieza y el balanceo de clases sobre los datos reales
- [ ] Ejecutar la selección de características (Extra Trees + correlación) sobre EMBER real
- [ ] Calcular los KPI definitivos de Fase 1 (% reducción real, % varianza/desempeño conservado, tiempo de extracción)
- [ ] **Hito 1: dataset limpio, balanceado y optimizado, listo para entrenamiento**

## FASE 2 — Construcción y evaluación del modelo (Semanas 5–8)

- [ ] Entrenar modelo Random Forest
- [ ] Entrenar modelo XGBoost
- [ ] Entrenar modelo de red neuronal densa (Dense Neural Network)
- [ ] Aplicar validación cruzada y ajuste de hiperparámetros a los tres modelos
- [ ] Calcular y comparar métricas: precisión, recall, F1-score, AUC-ROC, tasa de falsos positivos
- [ ] Priorizar minimización de falsos negativos (archivo malicioso clasificado como benigno)
- [ ] Seleccionar el modelo final según desempeño global
- [ ] **Hito 2: modelo seleccionado (meta: F1 ≥ 0.95, FPR ≤ 5%, AUC-ROC ≥ 0.98)**

## FASE 3 — Integración de explicabilidad XAI (Semanas 9–12)

- [ ] Implementar SHAP sobre el modelo seleccionado
- [ ] Implementar LIME sobre el modelo seleccionado
- [ ] Comparar SHAP vs. LIME y elegir la técnica definitiva
- [ ] Diseñar la traducción de valores SHAP/LIME a explicaciones en lenguaje natural comprensible
- [ ] Generar visualizaciones de importancia de características por predicción
- [ ] Verificar que el 100% de las predicciones generen explicación asociada
- [ ] **Hito 3: XAI integrada y verificada**

## FASE 4 — Despliegue y validación en interfaz interactiva (Semanas 13–16)

- [ ] Construir la interfaz web con Streamlit o Gradio
- [ ] Implementar la carga de archivos y la conexión con el modelo + módulo XAI
- [ ] Pruebas funcionales (malware conocido vs. archivos benignos)
- [ ] Pruebas de rendimiento (meta: respuesta ≤ 10 s por archivo, latencia interfaz ≤ 2 s)
- [ ] Evaluación de usabilidad con escala SUS y usuarios reales (meta: SUS ≥ 70)
- [ ] Ajustes finales según resultados de las pruebas
- [ ] **Hito 4: sistema desplegado y validado**

## Entregables finales del proyecto

- [ ] Dataset procesado, documentado y reproducible (real, no piloto)
- [ ] Modelo entrenado y evaluado, con scripts de validación cruzada
- [ ] Módulo de explicabilidad con visualizaciones de importancia de características
- [ ] Interfaz interactiva funcional con instrucciones de despliegue
- [ ] Repositorio público en GitHub o GitLab con control de versiones y README
- [ ] Documento final de trabajo de grado (resultados, análisis y conclusiones — capítulos que aún no existen en el anteproyecto actual)
- [ ] Sustentación / presentación final ante el jurado

## Avances administrativos / de gestión

- [x] Anteproyecto completo (contexto, objetivos, marcos de referencia, estado del arte, metodología, cronograma, presupuesto)
- [x] Informe de avance semana 3 entregado al director
- [ ] Informes de avance de las semanas siguientes (según lo pida el director)
- [ ] Crear el repositorio en GitHub/GitLab (aún no se ha hecho)

---

### Resumen rápido
**Hecho:** justificación y comparación de datasets, diseño y validación metodológica del pipeline de selección de características (sobre datos piloto), primer informe de avance.
**Pendiente inmediato (semana 4):** conseguir y procesar los datasets reales (EMBER, CIC-MalMem-2022) para cerrar formalmente la Fase 1.
**Pendiente grueso:** Fases 2, 3 y 4 completas (entrenamiento de modelos, XAI, interfaz, pruebas), repositorio de código, y la redacción del documento final de trabajo de grado con resultados y conclusiones.
