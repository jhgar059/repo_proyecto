"""Wireframe (mockup de baja fidelidad) de la pantalla de análisis de la interfaz web.

Documenta la estructura de la versión final: no es una captura ni muestra datos reales; los textos entre corchetes
son marcadores. Fuente editable del diagrama. Uso: python3 wireframe_pantalla_analisis.py salida.png
"""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

GRIS_BORDE, GRIS_FONDO, GRIS_TEXTO = "#555555", "#F2F2F2", "#333333"
plt.rcParams["font.family"] = "Liberation Sans"

fig = plt.figure(figsize=(6.6, 9.0))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 100); ax.set_ylim(-7, 130); ax.axis("off")


def caja(x, y, w, h, texto="", fondo="white", borde=GRIS_BORDE, tam=8.5, negrita=False, alinear="left", punteado=False, redondo=True):
    estilo = "round,pad=0.4,rounding_size=1.2" if redondo else "square,pad=0.2"
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=estilo, linewidth=1.1, edgecolor=borde, facecolor=fondo,
                                linestyle=(0, (4, 3)) if punteado else "solid"))
    if texto:
        tx = x + 1.5 if alinear == "left" else x + w / 2
        ax.text(tx, y + h / 2, texto, ha=alinear if alinear != "center" else "center", va="center", fontsize=tam,
                color=GRIS_TEXTO, fontweight="bold" if negrita else "normal", wrap=True)


def llamada(n, x, y):
    ax.add_patch(plt.Circle((x, y), 1.9, color="#1168BD"))
    ax.text(x, y, str(n), ha="center", va="center", fontsize=8, color="white", fontweight="bold")


# Marco del navegador
caja(2, 2, 96, 126, fondo="white", borde="#333333", redondo=False)
caja(2, 123.5, 96, 4.5, "  ●  ●  ●     [enlace de la aplicación]", fondo=GRIS_FONDO, tam=7.5, redondo=False)
# Encabezado
ax.text(6, 117.5, "¿Es seguro este archivo?", fontsize=14, fontweight="bold", color=GRIS_TEXTO)
ax.text(6, 112.8, "Suba un programa o biblioteca de Windows. El sistema le dirá si parece peligroso o seguro,\n"
                  "qué hacer y por qué, en palabras sencillas. El archivo no se abre ni se ejecuta.",
        fontsize=7.5, color=GRIS_TEXTO, va="center")
llamada(1, 94, 117.5)
# Pestañas
caja(6, 102, 30, 4.5, "Analizar un archivo", fondo="#DCEBFA", tam=8, negrita=True, alinear="center")
caja(38, 102, 40, 4.5, "Probar con ejemplos de EMBER2024", tam=8, alinear="center")
llamada(2, 82, 104.2)
# Zona de carga y botón
caja(6, 88, 88, 10, "Arrastre aquí el archivo o haga clic para buscarlo\n(.exe, .dll, .sys, .ocx, .scr, .cpl, .drv; máx. 5 MB)",
     fondo=GRIS_FONDO, tam=8, alinear="center", punteado=True)
caja(6, 81, 88, 4.5, "Analizar", fondo="#438DD5", borde="#2E6295", tam=9, negrita=True, alinear="center")
ax.texts[-1].set_color("white")
llamada(3, 96.5, 93)
# Resultado
caja(6, 66, 88, 11.5, "", fondo="#FFF4CC", borde="#B38F00")
ax.text(8, 74.2, "[VEREDICTO]  ·  Riesgo: [NIVEL]  ·  Probabilidad de malware: [xx %]", fontsize=8.5, fontweight="bold", color=GRIS_TEXTO)
ax.text(8, 69.3, "Qué hacer: [recomendación según el nivel de riesgo]", fontsize=8, color=GRIS_TEXTO)
llamada(4, 96.5, 71.8)
# Por qué
ax.text(6, 61.5, "¿Por qué lo dice el sistema?", fontsize=9.5, fontweight="bold", color=GRIS_TEXTO)
for i in range(5):
    ax.text(8, 57.3 - 3.6 * i, f"•  [Frase {i + 1}: qué se encontró en el archivo y si aumentó o redujo la sospecha (mucho / un poco / ligeramente)]",
            fontsize=6.9, color=GRIS_TEXTO)
llamada(5, 96.5, 52)
# Gráfica sin ejes
caja(6, 21.5, 52, 17, "", fondo="white")
ax.text(8, 36.7, "Señales que más pesaron (sin ejes numéricos)", fontsize=7.5, color=GRIS_TEXTO)
for i, (ancho, color) in enumerate([(38, "#555555"), (31, "#555555"), (22, "#BBBBBB"), (15, "#555555"), (11, "#BBBBBB")]):
    ax.add_patch(Rectangle((8, 33.6 - 2.1 * i), ancho, 1.4, color=color))
ax.text(8, 23.2, "oscuro: aumentó la sospecha · claro: la redujo", fontsize=6.5, color=GRIS_TEXTO)
# Glosario
caja(61, 21.5, 33, 17, "", fondo=GRIS_FONDO)
ax.text(63, 36.2, "Glosario", fontsize=8, fontweight="bold", color=GRIS_TEXTO)
for i in range(3):
    ax.text(63, 31.5 - 3.6 * i, f"[término {i + 1}]: [definición breve]", fontsize=6.8, color=GRIS_TEXTO)
llamada(6, 96.5, 30)
# Panel plegable
caja(6, 11.5, 88, 5, "►  Detalles técnicos (nombres de las características, valores y aportes SHAP)", tam=7.8)
llamada(7, 96.5, 14)
ax.text(6, 5.5, "Trabajo de grado – Universidad Católica de Colombia, 2026. Uso académico: no sustituye un antivirus.", fontsize=6.5, color=GRIS_TEXTO)

# Leyenda de las llamadas
leyenda = ("Leyenda: 1 encabezado y propósito · 2 pestañas (HU-001, HU-004) · 3 carga con tipos admitidos y límite (HU-001)\n"
           "4 resultado y qué hacer (HU-001) · 5 explicación en frases (HU-002) · 6 gráfica y glosario (HU-002) · "
           "7 detalles técnicos (HU-003) · [ ] marcador")
fig.text(0.5, 0.004, leyenda, ha="center", va="bottom", fontsize=6.6, color=GRIS_TEXTO, wrap=True)
fig.savefig(sys.argv[1], dpi=300, facecolor="white")
print("guardado", sys.argv[1])
