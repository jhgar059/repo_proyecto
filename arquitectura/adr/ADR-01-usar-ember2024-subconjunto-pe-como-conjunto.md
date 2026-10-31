---
status: accepted
date: 2026-10-31
decision-makers: Jhon Alexander Parra Olarte, Jhon David González García
---

# ADR-01. Usar EMBER2024 (subconjunto PE) como conjunto de datos

## Contexto y planteamiento del problema

Se necesitaba un conjunto público, reciente y documentado de ejecutables PE que permitiera evaluar con archivos posteriores al entrenamiento.

## Factores de decisión

* Actualidad
* Partición temporal
* Malware evasivo
* Extractor abierto
* Viabilidad en Colab

## Opciones consideradas

* EMBER2018
* BODMAS
* SOREL-20M
* CIC-MalMem-2022
* Conjunto de Kaggle
* EMBER2024

## Resultado de la decisión

Opción elegida: EMBER2024, el único que cumple todos los factores (Tabla 40 del documento).

### Consecuencias

* Buena, porque prueba temporal, desafío y el mismo extractor en la interfaz.
* Mala, porque 46 GB de archivos crudos obligan a muestrear el 23,5 % del entrenamiento; el extractor es más lento.

### Confirmación

Compuerta KPI-1; composición del conjunto (Tabla 42 del documento).

## Más información

* Estado: Aceptada (septiembre de 2026; reemplazó a EMBER2018).
* ASR que traza: ASR-03.
* En el documento: Tabla 20 (resumen) y Tabla F.1 del Anexo F.
* La fecha del encabezado es la del registro escrito de la decisión; el mes en que se tomó está en el estado.
