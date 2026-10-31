---
status: accepted
date: 2026-10-31
decision-makers: Jhon Alexander Parra Olarte, Jhon David González García
---

# ADR-07. Limitar a 5 MB el tamaño de los archivos en la interfaz

## Contexto y planteamiento del problema

La interfaz aceptaba 50 MB, pero la meta de latencia (p95 < 10 s) solo se cumplió hasta 5 MB (11,40 s a 20 MB).

## Factores de decisión

* No admitir entradas con las que se sabe que se incumple la meta
* Robustez ante la variación de Colab

## Opciones consideradas

* Mantener 50 MB y reformular la meta
* 20 MB
* Medir 10 y 15 MB
* 5 MB

## Resultado de la decisión

Opción elegida: 5 MB, el mayor tamaño medido que cumple, con margen (3,48 s).

### Consecuencias

* Buena, porque la interfaz y el requisito son coherentes.
* Mala, porque los ejecutables mayores no se analizan; la versión de la prueba SUS aceptaba 50 MB.

### Confirmación

PF-05 y PF-07 en la corrida de verificación.

## Más información

* Estado: Aceptada (octubre de 2026).
* ASR que traza: ASR-01, ASR-07.
* En el documento: Tabla 20 (resumen) y Tabla F.7 del Anexo F.
* La fecha del encabezado es la del registro escrito de la decisión; el mes en que se tomó está en el estado.
