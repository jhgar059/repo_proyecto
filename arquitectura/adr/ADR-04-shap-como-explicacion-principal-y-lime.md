---
status: accepted
date: 2026-10-31
decision-makers: Jhon Alexander Parra Olarte, Jhon David González García
---

# ADR-04. SHAP como explicación principal y LIME como contraste

## Contexto y planteamiento del problema

Cada predicción de la interfaz debe venir con una explicación rápida y fiel.

## Factores de decisión

* Fidelidad
* Tiempo
* Estabilidad

## Opciones consideradas

* SHAP TreeExplainer exacto o aproximado
* LIME
* Ambos

## Resultado de la decisión

Opción elegida: SHAP aproximado en la interfaz; LIME solo para medir el acuerdo.

### Consecuencias

* Buena, porque 0,6 ms y aditividad exacta.
* Mala, porque lIME varía entre ejecuciones (acuerdo de 0,677).

### Confirmación

Tabla 51 del documento.

## Más información

* Estado: Aceptada (septiembre de 2026).
* ASR que traza: ASR-04.
* En el documento: Tabla 20 (resumen) y Tabla F.4 del Anexo F.
* La fecha del encabezado es la del registro escrito de la decisión; el mes en que se tomó está en el estado.
