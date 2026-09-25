"""
Fase 1 (pasos finales) - Limpieza y seleccion de caracteristicas sobre
EMBER real (ya descargado y vectorizado en el paso anterior).

Correr en la MISMA sesion de Colab donde ya tienen montado Google
Drive y generado ember_train_etiquetado.parquet.
"""
import os
import time
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score

BASE_DIR = "/content/drive/MyDrive/trabajo_grado_malware/ember2018"
train_parquet = os.path.join(BASE_DIR, "ember_train_etiquetado.parquet")

RANDOM_STATE = 42
TOP_K = 10

# --- 1) Cargar datos reales ---
print("Cargando dataset real...")
df = pd.read_parquet(train_parquet)
print(f"Filas: {df.shape[0]}, columnas: {df.shape[1]-1} caracteristicas + label")

X = df.drop(columns=["label"])
y = df["label"]

# --- 2) Limpieza: nulos y columnas constantes ---
n_nulos = X.isnull().sum().sum()
print(f"Valores nulos encontrados: {n_nulos}")
if n_nulos > 0:
    X = X.fillna(0)

cols_constantes = X.columns[X.nunique() <= 1].tolist()
print(f"Columnas constantes encontradas: {len(cols_constantes)}")
if cols_constantes:
    X = X.drop(columns=cols_constantes)

n_original = X.shape[1]
print(f"Caracteristicas despues de limpieza: {n_original}")

# --- 3) Split train/test para validar el pipeline ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y
)

scaler = StandardScaler()
X_train_s = pd.DataFrame(scaler.fit_transform(X_train), columns=X.columns)
X_test_s = pd.DataFrame(scaler.transform(X_test), columns=X.columns)

# --- 4) Extra Trees Classifier: ranking de importancia ---
print("Entrenando Extra Trees Classifier sobre datos reales (puede tardar varios minutos)...")
t0 = time.time()
etc = ExtraTreesClassifier(n_estimators=400, random_state=RANDOM_STATE, n_jobs=-1, criterion="gini")
etc.fit(X_train_s, y_train)
tiempo_seleccion = time.time() - t0

importances = pd.Series(etc.feature_importances_, index=X.columns).sort_values(ascending=False)

# --- 5) Filtro de correlacion sobre el top 30 ---
top_preliminar = importances.head(30).index.tolist()
corr_matrix = X_train_s[top_preliminar].corr().abs()

to_drop = set()
for i, col_i in enumerate(top_preliminar):
    if col_i in to_drop:
        continue
    for col_j in top_preliminar[i + 1:]:
        if col_j in to_drop:
            continue
        if corr_matrix.loc[col_i, col_j] > 0.90:
            to_drop.add(col_j)

seleccion_final = [c for c in top_preliminar if c not in to_drop][:TOP_K]
print(f"Caracteristicas seleccionadas ({len(seleccion_final)}): {seleccion_final}")

# --- 6) Validacion: F1 con todas vs. con las seleccionadas ---
clf_full = ExtraTreesClassifier(n_estimators=300, random_state=RANDOM_STATE, n_jobs=-1)
clf_full.fit(X_train_s, y_train)
f1_full = f1_score(y_test, clf_full.predict(X_test_s))

clf_reducido = ExtraTreesClassifier(n_estimators=300, random_state=RANDOM_STATE, n_jobs=-1)
clf_reducido.fit(X_train_s[seleccion_final], y_train)
f1_reducido = f1_score(y_test, clf_reducido.predict(X_test_s[seleccion_final]))

pct_reduccion = 100 * (1 - len(seleccion_final) / n_original)
pct_f1_conservado = 100 * f1_reducido / f1_full

# --- 7) Resumen final (KPI de Fase 1) ---
resumen = {
    "n_caracteristicas_originales": int(n_original),
    "n_caracteristicas_seleccionadas": len(seleccion_final),
    "porcentaje_reduccion_dimensionalidad": round(pct_reduccion, 1),
    "f1_con_todas_las_caracteristicas": round(f1_full, 4),
    "f1_con_caracteristicas_seleccionadas": round(f1_reducido, 4),
    "porcentaje_desempeno_f1_conservado": round(pct_f1_conservado, 1),
    "tiempo_seleccion_segundos": round(tiempo_seleccion, 1),
    "caracteristicas_seleccionadas": seleccion_final,
}

import json
print(json.dumps(resumen, indent=2, ensure_ascii=False))

# --- 8) Guardar dataset reducido final + resumen en Drive ---
df_reducido = df[seleccion_final + ["label"]]
df_reducido.to_parquet(os.path.join(BASE_DIR, "ember_reducido_top10.parquet"), index=False)

with open(os.path.join(BASE_DIR, "resumen_seleccion_real.json"), "w") as f:
    json.dump(resumen, f, indent=2, ensure_ascii=False)

print("Listo. Dataset reducido y resumen guardados en Drive.")
print("Con esto se cierra el Objetivo Especifico 1 y el Hito 1 del cronograma.")
