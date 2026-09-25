"""
Parche para el bug conocido de la libreria `ember` con versiones
nuevas de scikit-learn (ver https://github.com/elastic/ember/issues/103
y la solucion propuesta en https://github.com/elastic/ember/pull/108).

Correr esta celda en Colab DESPUES de instalar `ember` y ANTES de
llamar a ember.create_vectorized_features(). No hace falta reinstalar
nada; simplemente corrige el archivo ya instalado en el entorno.
"""
import ember
import os

features_path = os.path.join(os.path.dirname(ember.__file__), "features.py")

with open(features_path, "r") as f:
    contenido = f.read()

linea_rota = 'entry_name_hashed = FeatureHasher(50, input_type="string").transform([raw_obj[\'entry\']]).toarray()[0]'
linea_corregida = 'entry_name_hashed = FeatureHasher(50, input_type="string").transform([[raw_obj[\'entry\']]]).toarray()[0]'

if linea_rota in contenido:
    contenido = contenido.replace(linea_rota, linea_corregida)
    with open(features_path, "w") as f:
        f.write(contenido)
    print(f"Parche aplicado correctamente en: {features_path}")
elif linea_corregida in contenido:
    print("El archivo ya tenia el parche aplicado, no se hizo nada.")
else:
    print("ADVERTENCIA: no se encontro la linea esperada. "
          "Puede que la version instalada de ember sea distinta. "
          f"Revisar manualmente el archivo: {features_path}")
    print("Buscar la linea que usa FeatureHasher sobre raw_obj['entry']")
    print("y envolver raw_obj['entry'] en una lista adicional: [[raw_obj['entry']]]")
