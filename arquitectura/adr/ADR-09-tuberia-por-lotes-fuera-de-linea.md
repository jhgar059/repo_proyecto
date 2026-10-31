---
status: accepted
date: 2026-10-31
decision-makers: Jhon Alexander Parra Olarte, Jhon David González García
---

# ADR-09. Tubería por lotes fuera de línea y aplicación monolítica en línea

## Contexto y planteamiento del problema

El entrenamiento corre por fases en Colab y el análisis en línea debe responder rápido y desplegarse sin infraestructura propia.

## Factores de decisión

* Simplicidad
* Costo cero
* Latencia
* Aislamiento

## Opciones consideradas

* Aplicación monolítica en un proceso
* Servicios separados (interfaz, API y trabajador aislado con cola)

## Resultado de la decisión

Opción elegida: Aplicación monolítica con el motor dentro del mismo proceso que Gradio.

### Consecuencias

* Buena, porque simple, sin costo y sin saltos de red.
* Mala, porque la extracción no está aislada (T-03, T-04) y no escala.

### Confirmación

Pruebas de rendimiento y matriz de amenazas.

## Más información

* Estado: Aceptada (septiembre de 2026).
* ASR que traza: ASR-01, ASR-07.
* En el documento: Tabla 20 (resumen) y Tabla F.9 del Anexo F.
* La fecha del encabezado es la del registro escrito de la decisión; el mes en que se tomó está en el estado.
