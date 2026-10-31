---
status: accepted
date: 2026-10-31
decision-makers: Jhon Alexander Parra Olarte, Jhon David González García
---

# ADR-08. Fijar la versión del extractor y registrar un contrato de artefactos

## Contexto y planteamiento del problema

El modelo depende de que el vector se calcule igual que en el entrenamiento, y thrember se instalaba sin versión fija.

## Factores de decisión

* Corrección
* Detectar cambios
* Reproducibilidad

## Opciones consideradas

* Instalar siempre la última versión
* Fijar la versión y registrar huellas
* Además verificar en ejecución

## Resultado de la decisión

Opción elegida: Fijar el commit 0ef753e y registrar el contrato en cada exportación; la verificación al iniciar queda como deuda (DT-03).

### Consecuencias

* Buena, porque los cambios quedan visibles en el contrato.
* Mala, porque actualizar thrember exige reentrenar.

### Confirmación

contrato_artefactos.json; FF-06.

## Más información

* Estado: Aceptada (octubre de 2026).
* ASR que traza: ASR-03.
* En el documento: Tabla 20 (resumen) y Tabla F.8 del Anexo F.
* La fecha del encabezado es la del registro escrito de la decisión; el mes en que se tomó está en el estado.
