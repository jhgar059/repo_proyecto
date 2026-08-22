"""
Fase 1 - Seleccion de caracteristicas
Extra Trees Classifier (importancia por impureza de Gini) +
analisis de correlacion para eliminar redundancia.
"""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42
TOP_K = 10  # meta del proyecto: reducir a las ~10 caracteristicas mas influyentes

df = pd.read_csv("/home/claude/work/dataset_piloto.csv")
X = df.drop(columns=["label"])
y = df["label"]
n_original = X.shape[1]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=RANDOM_STATE, stratify=y
)

scaler = StandardScaler()
X_train_s = pd.DataFrame(scaler.fit_transform(X_train), columns=X.columns)

# --- 1) Importancia con Extra Trees Classifier ---
etc = ExtraTreesClassifier(
    n_estimators=400, random_state=RANDOM_STATE, n_jobs=-1, criterion="gini"
)
etc.fit(X_train_s, y_train)
importances = pd.Series(etc.feature_importances_, index=X.columns).sort_values(ascending=False)

# --- 2) Analisis de correlacion sobre el top preliminar (top 30) ---
top_preliminar = importances.head(30).index.tolist()
corr_matrix = X_train_s[top_preliminar].corr().abs()

# eliminar una de cada par con correlacion > 0.9, conservando la de mayor importancia
to_drop = set()
cols_ordenadas = importances.head(30).index.tolist()  # ya ordenadas por importancia desc
for i, col_i in enumerate(cols_ordenadas):
    if col_i in to_drop:
        continue
    for col_j in cols_ordenadas[i + 1:]:
        if col_j in to_drop:
            continue
        if corr_matrix.loc[col_i, col_j] > 0.90:
            to_drop.add(col_j)  # col_j tiene menor importancia (viene despues)

seleccion_final = [c for c in cols_ordenadas if c not in to_drop][:TOP_K]

# --- 3) Desempeno conservado: se compara un clasificador entrenado con
# TODAS las caracteristicas contra uno entrenado solo con las 10
# seleccionadas, para verificar que la reduccion no sacrifica poder
# discriminativo (medido en F1-score sobre el set de prueba).
from sklearn.metrics import f1_score

X_test_s = pd.DataFrame(scaler.transform(X_test), columns=X.columns)

clf_full = ExtraTreesClassifier(n_estimators=300, random_state=RANDOM_STATE, n_jobs=-1)
clf_full.fit(X_train_s, y_train)
f1_full = f1_score(y_test, clf_full.predict(X_test_s))

clf_reducido = ExtraTreesClassifier(n_estimators=300, random_state=RANDOM_STATE, n_jobs=-1)
clf_reducido.fit(X_train_s[seleccion_final], y_train)
f1_reducido = f1_score(y_test, clf_reducido.predict(X_test_s[seleccion_final]))

pct_f1_conservado = 100 * f1_reducido / f1_full
pct_reduccion = 100 * (1 - len(seleccion_final) / n_original)

# --- 4) Guardar dataset reducido ---
df_reducido = df[seleccion_final + ["label"]]
df_reducido.to_csv("/home/claude/work/dataset_reducido_top10.csv", index=False)

# --- 5) Graficos ---
plt.figure(figsize=(8, 5))
importances.head(15).sort_values().plot(kind="barh", color="#2E5EAA")
plt.title("Top 15 caracteristicas por importancia (Extra Trees Classifier)")
plt.xlabel("Importancia (impureza de Gini)")
plt.tight_layout()
plt.savefig("/home/claude/work/fig_importancia_features.png", dpi=150)
plt.close()

plt.figure(figsize=(7, 6))
sub_corr = X_train_s[seleccion_final].corr()
im = plt.imshow(sub_corr, cmap="RdBu_r", vmin=-1, vmax=1)
plt.colorbar(im, fraction=0.046, pad=0.04)
plt.xticks(range(len(seleccion_final)), seleccion_final, rotation=90, fontsize=7)
plt.yticks(range(len(seleccion_final)), seleccion_final, fontsize=7)
plt.title("Correlacion entre las 10 caracteristicas seleccionadas")
plt.tight_layout()
plt.savefig("/home/claude/work/fig_correlacion_top10.png", dpi=150)
plt.close()

resumen = {
    "n_caracteristicas_originales": int(n_original),
    "n_caracteristicas_seleccionadas": len(seleccion_final),
    "porcentaje_reduccion_dimensionalidad": round(pct_reduccion, 1),
    "f1_con_todas_las_caracteristicas": round(f1_full, 4),
    "f1_con_10_caracteristicas": round(f1_reducido, 4),
    "porcentaje_desempeno_f1_conservado": round(pct_f1_conservado, 1),
    "caracteristicas_seleccionadas": seleccion_final,
    "caracteristicas_eliminadas_por_redundancia": len(to_drop),
}

with open("/home/claude/work/resumen_seleccion.json", "w") as f:
    json.dump(resumen, f, indent=2, ensure_ascii=False)

print(json.dumps(resumen, indent=2, ensure_ascii=False))
