"""
Fase 1 - Generacion de dataset piloto para validar el pipeline de
seleccion de caracteristicas antes de aplicarlo sobre el volumen
completo de EMBER / CIC-MalMem-2022.

Se simulan grupos de caracteristicas analogos a los que describe la
literatura de EMBER (Anderson & Roth, 2018): informacion de cabecera
PE, secciones, tabla de importaciones/exportaciones, histograma de
bytes/entropia y caracteristicas generales del archivo. Se incluyen
variables redundantes (altamente correlacionadas) y variables de
ruido para poder demostrar que Extra Trees + analisis de correlacion
efectivamente descartan lo que no aporta.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 6000  # muestras piloto

def make_group(prefix, n_features, n_informative, noise_std=1.0):
    """Crea un grupo de variables donde algunas son informativas
    (separan clases) y otras son ruido puro."""
    cols = {}
    signal = rng.normal(0, 1, N)
    for i in range(n_features):
        if i < n_informative:
            # variable informativa + ruido
            cols[f"{prefix}_{i}"] = signal * rng.uniform(0.6, 1.4) + rng.normal(0, noise_std, N)
        else:
            cols[f"{prefix}_{i}"] = rng.normal(0, 1, N)
    return cols, signal

data = {}
signals = []

# Grupos analogos a EMBER: header, section, imports, exports,
# byte_entropy_histogram, general, strings
grupos = [
    ("header",   15, 4),
    ("section",  20, 5),
    ("imports",  25, 6),
    ("exports",  10, 2),
    ("entropy",  30, 8),
    ("general",  10, 3),
    ("strings",  15, 4),
]

for prefix, n_feat, n_info in grupos:
    cols, sig = make_group(prefix, n_feat, n_info)
    data.update(cols)
    signals.append(sig)

df = pd.DataFrame(data)

# Variables redundantes: copias casi identicas de columnas ya
# informativas (para que el analisis de correlacion tenga algo que
# eliminar), simulando metadatos duplicados del PE header.
for i in range(12):
    src = rng.choice(df.columns)
    df[f"dup_{i}_{src}"] = df[src] + rng.normal(0, 0.05, N)

# Variable objetivo: combinacion de las senales de los grupos mas
# relevantes (header, section, imports, entropy) + ruido, pasada por
# un umbral -> clasificacion binaria malicioso(1) / benigno(0)
combined_signal = (
    1.3 * signals[0] + 1.1 * signals[1] + 1.4 * signals[2] + 1.6 * signals[4]
    + rng.normal(0, 1.5, N)
)
threshold = np.quantile(combined_signal, 0.62)  # ~38% malicioso, similar a EMBER
df["label"] = (combined_signal > threshold).astype(int)

out_path = "/home/claude/work/dataset_piloto.csv"
df.to_csv(out_path, index=False)

print(f"Dataset piloto generado: {df.shape[0]} muestras x {df.shape[1]-1} caracteristicas")
print(f"Distribucion de clases -> benigno: {(df['label']==0).sum()} | malicioso: {(df['label']==1).sum()}")
print(f"Guardado en: {out_path}")
