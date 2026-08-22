"""
Descarga y vectorizacion del dataset EMBER2018 real.

IMPORTANTE: este script NO se puede correr dentro de este chat/sandbox
porque (1) el host ember.elastic.co esta bloqueado por la politica de
red de este entorno, y (2) el archivo pesa varios GB, mas de lo que
conviene procesar aqui.

Instrucciones: subir y correr este script en Google Colab (el entorno
que ya esta definido en el anteproyecto, seccion 6.2 - Instrumentos).
Requiere ~10 GB libres de disco y puede tardar 20-40 min en descargar
segun la velocidad de conexion de Colab.

*** MUY IMPORTANTE SOBRE EL ORDEN DE EJECUCION ***
Este script debe correr en un runtime "limpio" (recien iniciado, sin
haber hecho antes `import ember` en esa misma sesion). La razon:
Python carga el modulo `ember` EN MEMORIA la primera vez que se
importa; si se parcha el archivo .py en disco DESPUES de haber hecho
`import ember`, la copia en memoria sigue siendo la vieja, y como
`ember.create_vectorized_features()` usa multiprocessing, los procesos
hijos heredan esa copia vieja -> el error de FeatureHasher reaparece
aunque el archivo en disco ya este corregido.
Si ya corrieron `import ember` antes en esta sesion de Colab: vayan a
Entorno de ejecucion > Reiniciar entorno de ejecucion, y corran este
script desde cero (el dataset ya descargado en /content/data no se
pierde al reiniciar el runtime, asi que no toca descargar de nuevo).
"""

import os
import subprocess

DATA_DIR = "/content/data/ember2018"  # ruta tipica en Colab
archive_path = "/content/data/ember2018.tar.bz2"
os.makedirs(DATA_DIR, exist_ok=True)

# --- 1) Instalar el paquete oficial ember ---
# En Colab, ejecutar primero en una celda (antes que todo lo demas):
#   !pip install git+https://github.com/elastic/ember.git
#   !pip install lightgbm lief

# --- 2) Descargar el archivo comprimido oficial (solo si no existe ya) ---
url = "https://ember.elastic.co/ember_dataset_2018_2.tar.bz2"

if not os.path.exists(archive_path):
    print("Descargando EMBER2018 (esto puede tardar, el archivo pesa varios GB)...")
    subprocess.run(["curl", "-L", url, "-o", archive_path], check=True)
else:
    print("El archivo comprimido ya existe en disco, no se vuelve a descargar.")

if not os.listdir(DATA_DIR):
    print("Descomprimiendo...")
    subprocess.run(["tar", "-xjf", archive_path, "-C", "/content/data"], check=True)
else:
    print("Los datos ya estan descomprimidos, no se repite el paso.")

# --- 3) Parche de compatibilidad ANTES de importar ember ---
# Bug conocido de la libreria `ember` con versiones nuevas de
# scikit-learn (repositorio archivado, sin mantenimiento). Ver:
#   https://github.com/elastic/ember/issues/103
#   https://github.com/elastic/ember/pull/108
# Se usa la ruta reportada en el traceback para no tener que hacer
# `import ember` antes de parchar (eso es justo lo que causa el
# problema de cacheo descrito arriba).
features_path = "/usr/local/lib/python3.12/dist-packages/ember/features.py"

with open(features_path, "r") as f:
    contenido = f.read()

linea_rota = 'entry_name_hashed = FeatureHasher(50, input_type="string").transform([raw_obj[\'entry\']]).toarray()[0]'
linea_corregida = 'entry_name_hashed = FeatureHasher(50, input_type="string").transform([[raw_obj[\'entry\']]]).toarray()[0]'

if linea_rota in contenido:
    contenido = contenido.replace(linea_rota, linea_corregida)
    with open(features_path, "w") as f:
        f.write(contenido)
    print(f"Parche del bug #103 aplicado en: {features_path}")
elif linea_corregida in contenido:
    print("El parche ya estaba aplicado, no se hizo nada.")
else:
    print("ADVERTENCIA: no se encontro la linea esperada en features.py.")
    print("Revisar la ruta real del paquete (!pip show ember) y aplicar")
    print("el parche manualmente en esa ubicacion.")

# --- 4) Recien AHORA se importa ember, ya con el archivo parchado ---
# (si esto falla con el mismo ValueError, es señal de que `ember` ya
# se habia importado antes en esta sesion -> reiniciar el runtime)
import multiprocessing
multiprocessing.set_start_method("spawn", force=True)  # refuerzo extra:
# obliga a que los procesos hijos se creen desde cero y relean el
# archivo parchado del disco, en vez de heredar memoria del proceso
# padre (comportamiento por defecto en Linux/Colab: "fork").

import ember

print("Vectorizando caracteristicas (2381 columnas)...")
ember.create_vectorized_features(DATA_DIR)
ember.create_metadata(DATA_DIR)

# --- 5) Cargar en memoria para inspeccion inicial ---
X_train, y_train, X_test, y_test = ember.read_vectorized_features(DATA_DIR)
metadata = ember.read_metadata(DATA_DIR)

print(f"X_train shape: {X_train.shape}")   # esperado: (900000, 2381)
print(f"X_test shape:  {X_test.shape}")    # esperado: (200000, 2381)
print(f"Distribucion y_train -> benigno: {(y_train==0).sum()}, "
      f"malicioso: {(y_train==1).sum()}, sin_etiqueta: {(y_train==-1).sum()}")

# --- 6) Guardar como parquet SIN cargar todo en RAM de una vez ---
# ember ya guarda X_train, y_train, X_test, y_test como archivos
# memmap en disco (X_train.dat, y_train.dat, etc. dentro de DATA_DIR).
# Convertirlos con pd.DataFrame(X_train) hace una copia completa en
# RAM (para train+test, ~19 GB), lo cual excede la RAM de Colab
# gratuito (~12.7 GB) y hace que se caiga el entorno.
# En vez de eso, se escribe el parquet por bloques (chunks), sin que
# el arreglo completo exista nunca entero en RAM.
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np

CHUNK_SIZE = 50_000  # filas por bloque; bajar a 20_000 si aun asi falta RAM

def guardar_parquet_por_chunks(X, y, out_path, solo_etiquetados=False):
    writer = None
    n = X.shape[0]
    for start in range(0, n, CHUNK_SIZE):
        end = min(start + CHUNK_SIZE, n)
        X_chunk = np.asarray(X[start:end])  # copia SOLO este bloque, no todo
        y_chunk = np.asarray(y[start:end])

        if solo_etiquetados:
            mask = y_chunk != -1
            X_chunk = X_chunk[mask]
            y_chunk = y_chunk[mask]
            if len(y_chunk) == 0:
                continue

        tabla = pa.table(
            {**{f"f{i}": X_chunk[:, i] for i in range(X_chunk.shape[1])},
             "label": y_chunk}
        )
        if writer is None:
            writer = pq.ParquetWriter(out_path, tabla.schema)
        writer.write_table(tabla)
        print(f"  {out_path}: filas {start}-{end} de {n} guardadas")

    if writer is not None:
        writer.close()
    else:
        print(f"  {out_path}: no habia filas para guardar")

print("Guardando train (solo etiquetados) por bloques...")
guardar_parquet_por_chunks(
    X_train, y_train,
    "/content/data/ember_train_etiquetado.parquet",
    solo_etiquetados=True,
)

print("Guardando test por bloques...")
guardar_parquet_por_chunks(
    X_test, y_test,
    "/content/data/ember_test.parquet",
    solo_etiquetados=False,
)

print("Listo. Archivos guardados en /content/data/*.parquet")
print("Estos archivos son los que se deben descargar y llevar al repositorio")
print("del proyecto para continuar con limpieza y seleccion de caracteristicas.")
