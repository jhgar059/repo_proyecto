<<<<<<< HEAD
# Sistema inteligente de detección de malware basado en Machine Learning

Trabajo de grado — Universidad Católica de Colombia, Facultad de Ingeniería, Programa de Ingeniería de Sistemas y Computación.

**Autores:** Jhon Alexander Parra Olarte, Jhon David González García
**Director:** Jorge Ignacio Blanco, Magíster en Telecomunicaciones

## Descripción

Sistema que utiliza Machine Learning para detectar malware en archivos ejecutables (PE de Windows) mediante análisis estático, integrando inteligencia artificial explicable (SHAP/LIME) para que cualquier usuario, con o sin conocimientos de ciberseguridad, entienda por qué un archivo se clasifica como seguro o malicioso.

## Estructura del repositorio

```
├── fase1_seleccion_caracteristicas/
│   ├── 01_generar_dataset_piloto.py
│   ├── 02_seleccion_caracteristicas.py
│   ├── descargar_ember_colab.py
│   ├── seleccion_caracteristicas_real.py
│   ├── parche_ember_bug103.py
│   ├── diagnostico_drive.py
│   ├── resumen_seleccion_real.json
│   └── Ficha_Tecnica_EMBER.docx
│
├── fase2_entrenamiento_modelos/
│   ├── fase2_entrenamiento_modelos.py
│   ├── fase2_comparacion_modelos.csv
│   └── fase2_mejores_hiperparametros.json
│
├── fase3_explicabilidad/
│   └── (pendiente)
│
├── fase4_interfaz/
│   ├── streamlit_app.py
│   └── requirements.txt
│
├── documentos/
│   ├── Trabajo-de-Grado.docx
│   ├── Entregable_OE1.docx
│   └── avances_semanales/
│
└── README.md
```

## Datasets utilizados

- **EMBER2018** (principal): 1.000.000 de archivos PE, 2.381 características estáticas.
  Fuente: Anderson, H. & Roth, P. (2018). arXiv:1804.04637.
- **CIC-MalMem-2022** (complementario): características de memoria volátil.

Los datasets no se incluyen en este repositorio por su tamaño (varios GB). Ver `fase1_seleccion_caracteristicas/descargar_ember_colab.py` para reproducir la descarga.

## Cómo reproducir el proyecto

1. **Fase 1** (Google Colab): correr `descargar_ember_colab.py`, luego `seleccion_caracteristicas_real.py`.
2. **Fase 2** (Google Colab): correr `fase2_entrenamiento_modelos.py` sobre el dataset reducido de Fase 1.
3. **Fase 3**: (pendiente de documentar tras completar Fase 2).
4. **Fase 4**: `streamlit run fase4_interfaz/streamlit_app.py`.

## Estado del proyecto

| Fase | Estado |
|---|---|
| Fase 1 — Selección de características | ✅ Completa |
| Fase 2 — Entrenamiento y comparación de modelos | 🔄 En progreso |
| Fase 3 — Integración de XAI (SHAP/LIME) | ⬜ Pendiente |
| Fase 4 — Interfaz interactiva y validación | ⬜ Pendiente |

## Licencia

Proyecto académico — Universidad Católica de Colombia, 2026.
=======
# repo_proyecto
trabajo de grado
>>>>>>> 086c69f5c82162acefcee95823d6d85a8e779753
