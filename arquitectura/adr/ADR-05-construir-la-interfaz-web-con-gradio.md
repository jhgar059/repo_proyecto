---
status: accepted
date: 2026-10-31
decision-makers: Jhon Alexander Parra Olarte, Jhon David González García
---

# ADR-05. Construir la interfaz web con Gradio

## Contexto y planteamiento del problema

Publicar una interfaz con carga de archivos para pruebas con usuarios.

## Factores de decisión

* Rapidez de desarrollo
* Carga de archivos
* Enlace compartible
* Costo cero

## Opciones consideradas

* Streamlit (prototipo de agosto de 2026)
* Framework web propio
* Gradio

## Resultado de la decisión

Opción elegida: Gradio.

### Consecuencias

* Buena, porque interfaz en un solo módulo y enlace público inmediato.
* Mala, porque caché y enlace público con los riesgos T-01 y T-05; personalización limitada.

### Confirmación

PF-09; prueba SUS.

## Más información

* Estado: Aceptada (septiembre de 2026).
* ASR que traza: ASR-05, ASR-06.
* En el documento: Tabla 20 (resumen) y Tabla F.5 del Anexo F.
* La fecha del encabezado es la del registro escrito de la decisión; el mes en que se tomó está en el estado.
