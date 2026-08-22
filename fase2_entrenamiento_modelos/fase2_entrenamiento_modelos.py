"""
Fase 2 - Construccion y evaluacion del modelo.

Entrena y compara Random Forest, XGBoost y una red neuronal densa
sobre el dataset real de EMBER ya reducido en la Fase 1, usando
validacion cruzada para el ajuste y el set de prueba INDEPENDIENTE
de EMBER (no visto durante seleccion de caracteristicas ni
entrenamiento) para la evaluacion final.

Correr en Google Colab, en la misma sesion/Drive donde ya estan los
archivos de la Fase 1.
"""
import os
import json
import time
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, accuracy_score,
)

BASE_DIR = "/content/drive/MyDrive/trabajo_grado_malware/ember2018"

# --- 0) Elegir que version del dataset reducido se usa ---
# Cambiar aqui segun cual dataset se quiera evaluar (TOP_K=10 o el
# TOP_K=20 que este probando tu compañero). Los dos deben quedar en
# Drive con nombres distintos para poder compararlos sin pisarse.
TRAIN_REDUCIDO = os.path.join(BASE_DIR, "ember_reducido_top10.parquet")  # o *_top20.parquet
RESUMEN_SELECCION = os.path.join(BASE_DIR, "resumen_seleccion_real.json")  # o el de top20

RANDOM_STATE = 42
N_FOLDS = 5

# --- 1) Cargar dataset reducido de entrenamiento (Fase 1) ---
print(f"Cargando: {TRAIN_REDUCIDO}")
df_train = pd.read_parquet(TRAIN_REDUCIDO)

with open(RESUMEN_SELECCION) as f:
    resumen_f1 = json.load(f)
columnas_seleccionadas = resumen_f1["caracteristicas_seleccionadas"]
print(f"Caracteristicas usadas ({len(columnas_seleccionadas)}): {columnas_seleccionadas}")

X_train_full = df_train[columnas_seleccionadas]
y_train_full = df_train["label"]

# --- 2) Cargar el set de prueba REAL e INDEPENDIENTE de EMBER ---
# ember_test.parquet tiene las 2381 columnas originales; se filtran
# solo las columnas seleccionadas en Fase 1, para evaluar en
# condiciones identicas y con datos que el pipeline nunca vio.
test_path = os.path.join(BASE_DIR, "ember_test.parquet")
print(f"Cargando set de prueba independiente: {test_path}")
df_test = pd.read_parquet(test_path, columns=columnas_seleccionadas + ["label"])
X_test = df_test[columnas_seleccionadas]
y_test = df_test["label"]

scaler = StandardScaler()
X_train_s = pd.DataFrame(scaler.fit_transform(X_train_full), columns=columnas_seleccionadas)
X_test_s = pd.DataFrame(scaler.transform(X_test), columns=columnas_seleccionadas)

print(f"Train: {X_train_s.shape}, Test (independiente): {X_test_s.shape}")

resultados = {}

# --- 3) Random Forest: RandomizedSearchCV + validacion cruzada ---
print("\n=== Random Forest ===")
t0 = time.time()
param_dist_rf = {
    "n_estimators": [200, 300, 400],
    "max_depth": [None, 10, 20, 30],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
}
cv = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=RANDOM_STATE)
rf_search = RandomizedSearchCV(
    RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1),
    param_distributions=param_dist_rf, n_iter=15, scoring="f1",
    cv=cv, random_state=RANDOM_STATE, n_jobs=-1, verbose=1,
)
rf_search.fit(X_train_s, y_train_full)
rf_best = rf_search.best_estimator_
tiempo_rf = time.time() - t0
print(f"Mejores hiperparametros RF: {rf_search.best_params_}")
print(f"F1 promedio en CV: {rf_search.best_score_:.4f}")

# --- 4) XGBoost: RandomizedSearchCV + validacion cruzada ---
print("\n=== XGBoost ===")
import xgboost as xgb
t0 = time.time()
param_dist_xgb = {
    "n_estimators": [200, 300, 400],
    "max_depth": [4, 6, 8, 10],
    "learning_rate": [0.01, 0.05, 0.1, 0.2],
    "subsample": [0.7, 0.85, 1.0],
    "colsample_bytree": [0.7, 0.85, 1.0],
}
xgb_search = RandomizedSearchCV(
    xgb.XGBClassifier(random_state=RANDOM_STATE, n_jobs=-1, eval_metric="logloss"),
    param_distributions=param_dist_xgb, n_iter=15, scoring="f1",
    cv=cv, random_state=RANDOM_STATE, n_jobs=-1, verbose=1,
)
xgb_search.fit(X_train_s, y_train_full)
xgb_best = xgb_search.best_estimator_
tiempo_xgb = time.time() - t0
print(f"Mejores hiperparametros XGBoost: {xgb_search.best_params_}")
print(f"F1 promedio en CV: {xgb_search.best_score_:.4f}")

# --- 5) Red neuronal densa (Dense Neural Network) ---
print("\n=== Dense Neural Network ===")
import tensorflow as tf
from tensorflow import keras

t0 = time.time()
tf.random.set_seed(RANDOM_STATE)

def construir_dnn(n_features):
    modelo = keras.Sequential([
        keras.layers.Input(shape=(n_features,)),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(32, activation="relu"),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(16, activation="relu"),
        keras.layers.Dense(1, activation="sigmoid"),
    ])
    modelo.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss="binary_crossentropy",
        metrics=[keras.metrics.AUC(name="auc"), "accuracy"],
    )
    return modelo

dnn = construir_dnn(X_train_s.shape[1])
early_stop = keras.callbacks.EarlyStopping(
    monitor="val_auc", mode="max", patience=8, restore_best_weights=True
)
historia = dnn.fit(
    X_train_s, y_train_full,
    validation_split=0.2,
    epochs=100, batch_size=1024,
    callbacks=[early_stop], verbose=1,
)
tiempo_dnn = time.time() - t0

# --- 6) Evaluacion final de los 3 modelos sobre el set de prueba INDEPENDIENTE ---
def evaluar(nombre, y_true, y_pred, y_proba, tiempo_entrenamiento, tiempo_inferencia_ms):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    fpr = fp / (fp + tn)
    return {
        "modelo": nombre,
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "precision": round(precision_score(y_true, y_pred), 4),
        "recall": round(recall_score(y_true, y_pred), 4),
        "f1_score": round(f1_score(y_true, y_pred), 4),
        "auc_roc": round(roc_auc_score(y_true, y_proba), 4),
        "fpr": round(fpr, 4),
        "tiempo_entrenamiento_s": round(tiempo_entrenamiento, 1),
        "tiempo_inferencia_ms_por_archivo": round(tiempo_inferencia_ms, 3),
    }

resultados_finales = []

# Random Forest
t0 = time.time()
y_pred_rf = rf_best.predict(X_test_s)
y_proba_rf = rf_best.predict_proba(X_test_s)[:, 1]
ms_rf = 1000 * (time.time() - t0) / len(X_test_s)
resultados_finales.append(evaluar("Random Forest", y_test, y_pred_rf, y_proba_rf, tiempo_rf, ms_rf))

# XGBoost
t0 = time.time()
y_pred_xgb = xgb_best.predict(X_test_s)
y_proba_xgb = xgb_best.predict_proba(X_test_s)[:, 1]
ms_xgb = 1000 * (time.time() - t0) / len(X_test_s)
resultados_finales.append(evaluar("XGBoost", y_test, y_pred_xgb, y_proba_xgb, tiempo_xgb, ms_xgb))

# DNN
t0 = time.time()
y_proba_dnn = dnn.predict(X_test_s, batch_size=4096).ravel()
ms_dnn = 1000 * (time.time() - t0) / len(X_test_s)
y_pred_dnn = (y_proba_dnn >= 0.5).astype(int)
resultados_finales.append(evaluar("Dense Neural Network", y_test, y_pred_dnn, y_proba_dnn, tiempo_dnn, ms_dnn))

df_resultados = pd.DataFrame(resultados_finales)
print("\n=== COMPARACION FINAL (set de prueba independiente) ===")
print(df_resultados.to_string(index=False))

# --- 7) Seleccionar el mejor modelo priorizando minimizar falsos negativos ---
# (recall alto = pocos maliciosos clasificados como benignos), tal
# como indica la metodologia del anteproyecto (seccion 6.1, Fase 2).
mejor = df_resultados.sort_values(by=["recall", "f1_score"], ascending=False).iloc[0]
print(f"\nModelo con mejor recall (menos falsos negativos): {mejor['modelo']}")

# --- 8) Guardar resultados y modelos en Drive ---
df_resultados.to_csv(os.path.join(BASE_DIR, "fase2_comparacion_modelos.csv"), index=False)

import joblib
joblib.dump(rf_best, os.path.join(BASE_DIR, "modelo_random_forest.joblib"))
joblib.dump(xgb_best, os.path.join(BASE_DIR, "modelo_xgboost.joblib"))
dnn.save(os.path.join(BASE_DIR, "modelo_dnn.keras"))

with open(os.path.join(BASE_DIR, "fase2_mejores_hiperparametros.json"), "w") as f:
    json.dump({
        "random_forest": rf_search.best_params_,
        "xgboost": xgb_search.best_params_,
        "modelo_recomendado": mejor["modelo"],
    }, f, indent=2, ensure_ascii=False)

print("\nListo. Resultados y modelos guardados en Drive:")
print("  fase2_comparacion_modelos.csv")
print("  fase2_mejores_hiperparametros.json")
print("  modelo_random_forest.joblib / modelo_xgboost.joblib / modelo_dnn.keras")
