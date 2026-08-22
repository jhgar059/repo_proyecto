"""
Diagnostico: verificar que hay realmente en Google Drive antes de
correr el pipeline de seleccion de caracteristicas.

Correr esta celda SOLA primero, antes que cualquier otra cosa.
"""
import os

# 1) Asegurar que Drive este montado en ESTA sesion
from google.colab import drive
drive.mount("/content/drive")

BASE_DIR = "/content/drive/MyDrive/trabajo_grado_malware/ember2018"

# 2) Listar que hay realmente en esa carpeta
if not os.path.exists(BASE_DIR):
    print(f"La carpeta {BASE_DIR} NO EXISTE todavia.")
    print("Esto significa que el script de descarga/vectorizacion nunca")
    print("llego a crearla, o se guardo en otra ruta. Busquemos en Drive:")
    for root, dirs, files in os.walk("/content/drive/MyDrive"):
        if "ember" in root.lower():
            print(" ", root)
else:
    print(f"La carpeta {BASE_DIR} SI existe. Contenido:")
    for f in sorted(os.listdir(BASE_DIR)):
        ruta = os.path.join(BASE_DIR, f)
        tam_mb = os.path.getsize(ruta) / 1e6 if os.path.isfile(ruta) else None
        if tam_mb is not None:
            print(f"  {f}  ({tam_mb:.1f} MB)")
        else:
            print(f"  {f}/  (carpeta)")

    ember2018_dir = os.path.join(BASE_DIR, "ember2018")
    if os.path.exists(ember2018_dir):
        print(f"\nContenido de {ember2018_dir}:")
        for f in sorted(os.listdir(ember2018_dir)):
            print(" ", f)
