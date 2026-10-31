---
status: accepted
date: 2026-10-31
decision-makers: Jhon Alexander Parra Olarte, Jhon David González García
---

# ADR-03. Usar Random Forest como modelo

## Contexto y planteamiento del problema

Elegir el clasificador con la regla de la Fase 2.

## Factores de decisión

* FPR ≤ 5 % (prioridad), recall, F1 y latencia

## Opciones consideradas

* Random Forest
* XGBoost
* Red neuronal densa

## Resultado de la decisión

Opción elegida: Random Forest por el criterio subsidiario (mayor F1), porque ningún modelo cumplió la meta de FPR.

### Consecuencias

* Buena, porque mejor F1, menor FPR y mejor recall en el desafío.
* Mala, porque 138 MB y 46,5 minutos de entrenamiento.

### Confirmación

Tablas 49 y 50 del documento.

## Más información

* Estado: Aceptada (septiembre de 2026).
* ASR que traza: ASR-01.
* En el documento: Tabla 20 (resumen) y Tabla F.3 del Anexo F.
* La fecha del encabezado es la del registro escrito de la decisión; el mes en que se tomó está en el estado.
