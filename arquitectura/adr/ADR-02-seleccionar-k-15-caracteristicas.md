---
status: accepted
date: 2026-10-31
decision-makers: Jhon Alexander Parra Olarte, Jhon David González García
---

# ADR-02. Seleccionar K = 15 características

## Contexto y planteamiento del problema

El vector tiene 2.568 características y se buscaba un sistema liviano y explicable con una regla de selección fijada de antemano.

## Factores de decisión

* F1 conservado ≥ 95 %
* Reducción ≥ 90 %
* Explicaciones con pocos factores

## Opciones consideradas

* K entre 5 y 150 (Tabla 45 del documento)
* Vector completo. Se intentó una corrida con K = 150, que se abandonó por el tiempo de cómputo en Colab

## Resultado de la decisión

Opción elegida: K = 15, el menor K que conserva el 95 % del F1 de referencia.

### Consecuencias

* Buena, porque reducción del 99,42 % y explicaciones de pocos factores.
* Mala, porque f1 de 0,925 y FPR de 7,4 % en la prueba temporal; no reduce la extracción.

### Confirmación

Curva K vs. F1 (Tabla 45 del documento); compuerta KPI-2.

## Más información

* Estado: Aceptada (septiembre de 2026); revisión propuesta con K = 50.
* ASR que traza: ASR-01.
* En el documento: Tabla 20 (resumen) y Tabla F.2 del Anexo F.
* La fecha del encabezado es la del registro escrito de la decisión; el mes en que se tomó está en el estado.
