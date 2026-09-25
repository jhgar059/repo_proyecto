"""
Interfaz interactiva - Deteccion de malware con Machine Learning.

Esqueleto de la Fase 4. Por ahora usa un modelo y explicaciones de
EJEMPLO (placeholders) para poder disenar y probar el flujo completo
de la interfaz sin depender de que Fase 2 y Fase 3 esten terminadas.

Para conectar el modelo real cuando este listo, buscar los bloques
marcados con "# TODO: conectar modelo real" y reemplazar la logica
de ejemplo por la carga real del modelo (.joblib / .keras) y del
modulo de explicabilidad (SHAP o LIME).

Correr con: streamlit run streamlit_app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(
    page_title="Detector de Malware",
    page_icon="🛡️",
    layout="centered",
)

# --------------------------------------------------------------
# Encabezado
# --------------------------------------------------------------
st.title("🛡️ Detector de Malware con Machine Learning")
st.caption(
    "Trabajo de grado — Universidad Católica de Colombia. "
    "Analiza un archivo antes de abrirlo y entiende por qué se "
    "considera seguro o peligroso."
)

st.divider()

# --------------------------------------------------------------
# Carga de archivo
# --------------------------------------------------------------
archivo = st.file_uploader(
    "Sube un archivo ejecutable (.exe o .dll) para analizar",
    type=["exe", "dll"],
    help="El archivo se analiza de forma estática, sin ejecutarlo en ningún momento.",
)

analizar = st.button("Analizar archivo", type="primary", disabled=archivo is None)

# --------------------------------------------------------------
# TODO: conectar modelo real
# --------------------------------------------------------------
def extraer_caracteristicas(archivo_bytes):
    """
    Placeholder. Debe reemplazarse por la extraccion real de las
    caracteristicas seleccionadas en Fase 1 (usando LIEF, igual que
    hace la libreria `ember`), devolviendo un DataFrame de una fila
    con las mismas columnas usadas para entrenar el modelo.
    """
    columnas_ejemplo = [f"f{i}" for i in range(10)]  # ajustar a las reales
    valores_ejemplo = np.random.rand(1, 10)
    return pd.DataFrame(valores_ejemplo, columns=columnas_ejemplo)


def predecir(features_df):
    """
    Placeholder. Debe reemplazarse por:
        modelo = joblib.load("modelo_random_forest.joblib")  # o el elegido
        proba = modelo.predict_proba(features_df)[0][1]
    """
    proba_malicioso = float(np.random.rand())
    return proba_malicioso


def explicar_prediccion(features_df, proba_malicioso):
    """
    Placeholder. Debe reemplazarse por la integracion real de SHAP
    o LIME (Fase 3), devolviendo una lista de (caracteristica,
    contribucion, explicacion_en_texto).
    """
    ejemplo = [
        ("Entropía de sección .text", 0.34, "Nivel de entropía inusualmente alto, típico de código empaquetado o cifrado."),
        ("Funciones importadas sospechosas", 0.21, "El archivo importa funciones asociadas a manipulación de memoria de otros procesos."),
        ("Tamaño de la sección de recursos", -0.12, "Tamaño dentro de rangos normales, reduce ligeramente la sospecha."),
    ]
    return ejemplo


# --------------------------------------------------------------
# Flujo principal
# --------------------------------------------------------------
if analizar and archivo is not None:
    with st.spinner("Analizando archivo..."):
        t0 = time.time()
        features_df = extraer_caracteristicas(archivo.read())
        proba_malicioso = predecir(features_df)
        explicacion = explicar_prediccion(features_df, proba_malicioso)
        tiempo_transcurrido = time.time() - t0

    es_malicioso = proba_malicioso >= 0.5

    st.divider()

    if es_malicioso:
        st.error(f"⚠️ Archivo clasificado como **MALICIOSO** ({proba_malicioso:.1%} de confianza)")
    else:
        st.success(f"✅ Archivo clasificado como **SEGURO** ({(1-proba_malicioso):.1%} de confianza)")

    st.caption(f"Tiempo de análisis: {tiempo_transcurrido:.2f} segundos")

    st.subheader("¿Por qué se clasificó así?")
    st.write("Estos son los factores que más influyeron en el resultado:")

    for nombre, contribucion, texto in explicacion:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{nombre}**")
            st.caption(texto)
        with col2:
            color = "🔴" if contribucion > 0 else "🟢"
            st.write(f"{color} {contribucion:+.2f}")

    with st.expander("Ver detalles técnicos"):
        st.dataframe(features_df.T.rename(columns={0: "Valor"}))

elif archivo is None:
    st.info("Sube un archivo para comenzar el análisis.")

st.divider()
st.caption(
    "⚠️ Nota: esta es una herramienta de demostración académica, no un "
    "antivirus de producción. No reemplaza herramientas de seguridad "
    "profesionales."
)
