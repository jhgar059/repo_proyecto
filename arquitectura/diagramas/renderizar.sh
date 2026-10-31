#!/usr/bin/env bash
# Regenera los PNG de los diagramas a partir de sus fuentes.
# Requiere Graphviz (dot), Mermaid CLI (mmdc) y Python con matplotlib.
set -euo pipefail
cd "$(dirname "$0")"
for f in *.dot; do dot -Tpng -Gdpi=300 "$f" -o "${f%.dot}.png"; done
mmdc -i 09_secuencia.mmd -o 09_secuencia.png -c config_seq.json -b white -s 3
python3 wireframe_pantalla_analisis.py 12_wireframe.png
python3 wireframe_estados.py 13_estados_ui.png
