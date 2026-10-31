# Arquitectura del sistema

Fuentes editables de los diagramas y registros de decisiones de arquitectura (ADR) del capítulo «Ingeniería de
requisitos y arquitectura del sistema» del documento del trabajo de grado. Los diagramas están escritos como código
(Graphviz, Mermaid y matplotlib) para que se puedan revisar y versionar igual que el resto del proyecto.

## Diagramas (`diagramas/`)

| Imagen | Contenido | En el documento | Fuente editable |
|---|---|---|---|
| 01_casos_de_uso.png | Casos de uso del sistema | Figura 2 | 01_casos_de_uso.dot (Graphviz) |
| 02_utility_tree.png | Utility Tree de los ASR de calidad | Figura 3 | 02_utility_tree.dot (Graphviz) |
| 03_modelo_dominio.png | Modelo de dominio | Figura 4 | 03_modelo_dominio.dot (Graphviz) |
| 04_c4_contexto.png | C4 nivel 1: contexto | Figura 5 | 04_c4_contexto.dot (Graphviz) |
| 05_c4_contenedores.png | C4 nivel 2: contenedores | Figura 6 | 05_c4_contenedores.dot (Graphviz) |
| 06_c4_componentes.png | C4 nivel 3: componentes | Figura 7 | 06_c4_componentes.dot (Graphviz) |
| 07_clases.png | Clases del módulo app_malware.py | Figura 8 | 07_clases.dot (Graphviz) |
| 08_despliegue.png | Despliegue | Figura 9 | 08_despliegue.dot (Graphviz) |
| 09_secuencia.png | Secuencia del escenario ASR-01 | Figura 10 | 09_secuencia.mmd (Mermaid) |
| 10_estados.png | Máquina de estados del análisis | Figura 11 | 10_estados.dot (Graphviz) |
| 11_navegacion.png | Mapa de navegación | Figura 13 | 11_navegacion.dot (Graphviz) |
| 12_wireframe.png | Wireframe de la pantalla de análisis | Figura 14 | wireframe_pantalla_analisis.py (matplotlib) |
| 13_estados_ui.png | Wireframe de los estados vacío y de error | Figura 15 | wireframe_estados.py (matplotlib) |
| 14_modelo_datos.png | Modelo de datos persistidos | Figura 12 | 14_modelo_datos.dot (Graphviz) |

Para regenerar todas las imágenes: `bash diagramas/renderizar.sh` (requiere Graphviz, Mermaid CLI y matplotlib).

## Decisiones de arquitectura (`adr/`)

Cada decisión sigue el formato MADR 4.0 (contexto, factores, opciones, decisión, consecuencias y confirmación) y
remite a los ASR que traza. El resumen está en la Tabla 20 del documento y el detalle en el Anexo F.

| ADR | Decisión | Estado | ASR |
|---|---|---|---|
| [ADR-01](adr/ADR-01-usar-ember2024-subconjunto-pe-como-conjunto.md) | Usar EMBER2024 (subconjunto PE) como conjunto de datos | Aceptada (septiembre de 2026; reemplazó a EMBER2018) | ASR-03 |
| [ADR-02](adr/ADR-02-seleccionar-k-15-caracteristicas.md) | Seleccionar K = 15 características | Aceptada (septiembre de 2026); revisión propuesta con K = 50 | ASR-01 |
| [ADR-03](adr/ADR-03-usar-random-forest-como-modelo.md) | Usar Random Forest como modelo | Aceptada (septiembre de 2026) | ASR-01 |
| [ADR-04](adr/ADR-04-shap-como-explicacion-principal-y-lime.md) | SHAP como explicación principal y LIME como contraste | Aceptada (septiembre de 2026) | ASR-04 |
| [ADR-05](adr/ADR-05-construir-la-interfaz-web-con-gradio.md) | Construir la interfaz web con Gradio | Aceptada (septiembre de 2026) | ASR-05, ASR-06 |
| [ADR-06](adr/ADR-06-usar-google-colab-google-drive-y.md) | Usar Google Colab, Google Drive y GitHub como infraestructura | Aceptada (agosto de 2026) | ASR-03 |
| [ADR-07](adr/ADR-07-limitar-a-5-mb-el-tamano.md) | Limitar a 5 MB el tamaño de los archivos en la interfaz | Aceptada (octubre de 2026) | ASR-01, ASR-07 |
| [ADR-08](adr/ADR-08-fijar-la-version-del-extractor-y.md) | Fijar la versión del extractor y registrar un contrato de artefactos | Aceptada (octubre de 2026) | ASR-03 |
| [ADR-09](adr/ADR-09-tuberia-por-lotes-fuera-de-linea.md) | Tubería por lotes fuera de línea y aplicación monolítica en línea | Aceptada (septiembre de 2026) | ASR-01, ASR-07 |

Una decisión nueva se propone como un archivo ADR en esta carpeta, se aprueba por acuerdo de los dos autores y, si
cambia el alcance, se consulta con la docente; el historial de Git es el registro.
