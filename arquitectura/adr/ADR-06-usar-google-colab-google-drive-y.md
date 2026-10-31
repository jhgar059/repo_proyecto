---
status: accepted
date: 2026-10-31
decision-makers: Jhon Alexander Parra Olarte, Jhon David González García
---

# ADR-06. Usar Google Colab, Google Drive y GitHub como infraestructura

## Contexto y planteamiento del problema

No hay presupuesto ni servidores y procesar EMBER2024 requiere memoria.

## Factores de decisión

* Costo cero
* Reproducibilidad
* Capacidad suficiente

## Opciones consideradas

* Computadores de los autores
* Servidor o nube de pago
* Colab gratuito con Drive y GitHub

## Resultado de la decisión

Opción elegida: Colab gratuito con Drive para persistir y GitHub para versionar.

### Consecuencias

* Buena, porque gratis y reproducible.
* Mala, porque sesiones temporales, recursos limitados (muestreo) y sin URL estable.

### Confirmación

Ejecución completa del notebook con puntos de control.

## Más información

* Estado: Aceptada (agosto de 2026).
* ASR que traza: ASR-03.
* En el documento: Tabla 20 (resumen) y Tabla F.6 del Anexo F.
* La fecha del encabezado es la del registro escrito de la decisión; el mes en que se tomó está en el estado.
