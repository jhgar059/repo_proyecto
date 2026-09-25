"""
Ejecuta en tu computador la interfaz Gradio del proyecto (la misma que describe el documento) con los
artefactos reales de la corrida 1, tomados de evidencias_proyecto.zip.

Uso (en una consola, dentro de la carpeta donde está el zip):
    pip install -r requisitos_interfaz.txt
    python ejecutar_interfaz_local.py evidencias_proyecto.zip

Qué hace:
  1. Extrae del zip solo lo que la app necesita y lo acomoda en app_local/ con la estructura que espera
     (modelos/, datos/, fase4/): modelo seleccionado, scaler, configuración XAI, app_malware.py y ejemplos.
  2. Reconstruye datos/diccionario_caracteristicas.json a partir del CSV del diccionario.
  3. Lanza la aplicación en http://127.0.0.1:7860 y abre el navegador.
Para detenerla: Ctrl+C en la consola.
"""
import os
import sys
import json
import zipfile
import importlib.util

ZIP = sys.argv[1] if len(sys.argv) > 1 else "evidencias_proyecto.zip"
BASE = os.path.abspath("app_local")

MAPA = {   # ruta dentro del zip -> ruta relativa que espera app_malware.py
    "03_modelos/random_forest.joblib": "modelos/random_forest.joblib",
    "03_modelos/xgboost.joblib": "modelos/xgboost.joblib",
    "03_modelos/dnn.keras": "modelos/dnn.keras",
    "03_modelos/scaler.joblib": "modelos/scaler.joblib",
    "03_modelos/modelo_seleccionado.json": "modelos/modelo_seleccionado.json",
    "04_explicabilidad/xai_config.joblib": "modelos/xai_config.joblib",
    "05_interfaz_y_pruebas/app_malware.py": "fase4/app_malware.py",
    "05_interfaz_y_pruebas/ejemplos_demo.parquet": "fase4/ejemplos_demo.parquet",
    "01_dataset/diccionario_caracteristicas.csv": "datos/diccionario_caracteristicas.csv",
}

if not os.path.exists(ZIP):
    sys.exit(f"No encuentro {ZIP}. Cópialo a esta carpeta (está en Drive/trabajo_grado_malware/ember2024/ o en tus descargas).")

with zipfile.ZipFile(ZIP) as z:
    nombres = set(z.namelist())
    for origen, destino in MAPA.items():
        if origen in nombres:
            ruta = os.path.join(BASE, destino)
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            with z.open(origen) as f_in, open(ruta, "wb") as f_out:
                f_out.write(f_in.read())
            print("extraído:", destino)
        elif not destino.endswith((".keras", "xgboost.joblib")):
            print("AVISO: no está en el zip:", origen)

sel = json.load(open(os.path.join(BASE, "modelos", "modelo_seleccionado.json"), encoding="utf-8"))
archivo_modelo = {"Random Forest": "random_forest.joblib", "XGBoost": "xgboost.joblib", "Red Neuronal Densa": "dnn.keras"}[sel["modelo"]]
if not os.path.exists(os.path.join(BASE, "modelos", archivo_modelo)):
    sys.exit(f"El modelo seleccionado ({sel['modelo']}) no venía en el zip por su tamaño: copia Drive/.../modelos/{archivo_modelo} "
             f"a app_local/modelos/ y vuelve a ejecutar.")

# Diccionario en el formato JSON que usa la app ({"nombres": [...], "grupos": [...]}) a partir del CSV
import pandas as pd
dic = pd.read_csv(os.path.join(BASE, "datos", "diccionario_caracteristicas.csv")).sort_values("indice")
json.dump({"nombres": dic["nombre"].tolist(), "grupos": dic["grupo"].tolist()},
          open(os.path.join(BASE, "datos", "diccionario_caracteristicas.json"), "w", encoding="utf-8"), ensure_ascii=False)

# Lanzar la app (misma clase AnalizadorMalware e interfaz construir_interfaz del notebook)
spec = importlib.util.spec_from_file_location("app_malware", os.path.join(BASE, "fase4", "app_malware.py"))
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)
print(f"Cargando el modelo {sel['modelo']} y el explicador SHAP (puede tardar un minuto)...")
analizador = app.AnalizadorMalware(BASE)
ejemplos = pd.read_parquet(os.path.join(BASE, "fase4", "ejemplos_demo.parquet"))
demo = app.construir_interfaz(analizador, ejemplos)
print("Interfaz lista: http://127.0.0.1:7860  (Ctrl+C para detener)")
demo.launch(server_name="127.0.0.1", server_port=7860, share=False, inbrowser=True)
