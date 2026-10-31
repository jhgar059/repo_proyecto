"""Wireframe de los estados vacío y de error de la pantalla de análisis (mockup de baja fidelidad).

Los mensajes son los que devuelve app_malware.py. Fuente editable. Uso: python3 wireframe_estados.py salida.png
"""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

GRIS_BORDE, GRIS_FONDO, GRIS_TEXTO = "#555555", "#F2F2F2", "#333333"
plt.rcParams["font.family"] = "Liberation Sans"
fig = plt.figure(figsize=(6.6, 3.7))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 56); ax.axis("off")


def caja(x, y, w, h, fondo="white", borde=GRIS_BORDE, punteado=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2", linewidth=1.1,
                                edgecolor=borde, facecolor=fondo, linestyle=(0, (4, 3)) if punteado else "solid"))


paneles = [
    (2, "a) Estado vacío (HU-001)", "Se pulsa «Analizar» sin seleccionar un archivo",
     "Seleccione un archivo para analizar.", GRIS_FONDO, GRIS_BORDE),
    (51, "b) Estado de error (HU-001)", "Se carga un .exe que en realidad no es un ejecutable",
     "El contenido del archivo no corresponde a un ejecutable\nde Windows (no tiene la firma PE), aunque su extensión\n"
     "lo sugiera. El sistema solo analiza programas y\nbibliotecas de Windows (.exe, .dll y formatos similares)…", "#F8D7DA", "#A94442"),
]
for x, titulo, accion, mensaje, fondo, borde in paneles:
    caja(x, 4, 47, 46, fondo="white", borde="#333333")
    ax.text(x + 1.5, 46.5, titulo, fontsize=9, fontweight="bold", color=GRIS_TEXTO)
    ax.text(x + 1.5, 42.5, accion, fontsize=7.2, color=GRIS_TEXTO, style="italic")
    caja(x + 2, 32, 43, 6.5, fondo=GRIS_FONDO, punteado=True)
    ax.text(x + 23.5, 35.2, "[zona de carga: .exe, .dll…; máx. 5 MB]", fontsize=7, ha="center", va="center", color=GRIS_TEXTO)
    caja(x + 2, 26, 43, 3.5, fondo="#438DD5", borde="#2E6295")
    ax.text(x + 23.5, 27.7, "Analizar", fontsize=8, ha="center", va="center", color="white", fontweight="bold")
    caja(x + 2, 7, 43, 15.5, fondo=fondo, borde=borde)
    ax.text(x + 3.5, 14.8, mensaje, fontsize=7, va="center", color=GRIS_TEXTO)
fig.text(0.5, 0.01, "Leyenda: recuadro punteado = zona de carga; recuadro inferior = área de resultado con el mensaje que muestra la aplicación; "
         "[ ] marcador", ha="center", fontsize=6.5, color=GRIS_TEXTO)
fig.savefig(sys.argv[1], dpi=300, facecolor="white")
print("guardado", sys.argv[1])
