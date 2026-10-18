"""traduccion_amigable.py - Capa de traducción de las explicaciones SHAP a lenguaje sencillo.

La genera la Fase 3 del notebook (fase3/traduccion_amigable.py) y app_malware.py la incluye
tal cual, para que la aplicación siga siendo un módulo autocontenido.

Idea: SHAP entrega, por archivo, un número por característica (cuánto empujó la decisión hacia
"malicioso" o hacia "benigno"). Esta capa convierte cada uno de esos números en:
  - un nombre corto en español (para la tabla y la gráfica),
  - una observación sobre el archivo concreto, escrita a partir del valor real de la
    característica ("no tiene firma digital", "es una biblioteca (DLL)"),
  - el efecto en palabras ("esto hizo desconfiar mucho al sistema"),
  - y el término del glosario que ayuda a entenderla.
Las frases describen lo que el extractor midió en el archivo y la dirección que SHAP calculó; no
afirman nada que no esté en los datos. Para características fuera de las 15 seleccionadas en la
corrida 1 hay una traducción genérica por grupo, de modo que la capa sigue funcionando si en una
nueva iteración cambia el conjunto de características.
"""
import datetime as _dt

GLOSARIO = {
    "firma digital": ("Sello electrónico que el fabricante pone a su programa y que Windows puede comprobar. Mucho software "
                      "legítimo lo trae; un programa sin firma no es necesariamente peligroso, pero da menos garantías."),
    "biblioteca (DLL)": ("Archivo con funciones que otros programas usan; no se abre solo. Un programa (.exe) sí se ejecuta "
                         "directamente."),
    "entropía": ("Medida de qué tan 'desordenados' están los datos. Es alta cuando el contenido está comprimido o cifrado, "
                 "algo que el malware usa para esconder su código, aunque algunos programas legítimos también lo hacen."),
    "encabezado": ("La 'ficha técnica' que todo programa de Windows lleva al inicio del archivo: dice qué tipo de archivo es, "
                   "cómo está organizado y qué protecciones usa."),
    "protecciones del sistema (ASLR/DEP)": ("Opciones que los programas activan al compilarse para que Windows los proteja mejor "
                                            "contra ataques. Los programas hechos con herramientas modernas suelen tenerlas."),
    "sección": ("Cada una de las partes en que se divide un programa (código, datos, recursos). Cada parte tiene permisos: "
                "leerse, escribirse o ejecutarse."),
    "datos añadidos (overlay)": ("Información pegada al final del archivo, después de las partes normales del programa. Algunos "
                                  "instaladores la usan; el malware también la usa para esconder contenido."),
    "exportaciones": "Funciones que un archivo ofrece a otros programas. Es típico de las bibliotecas (DLL).",
    "reubicaciones": ("Tabla que permite a Windows cargar el programa en distintas posiciones de la memoria; los programas "
                      "modernos suelen incluirla."),
}

GRUPOS_CORTOS = {
    "general": "Información general", "histogram": "Distribución de bytes", "byteentropy": "Contenido comprimido o cifrado",
    "strings": "Textos dentro del archivo", "header": "Encabezado del archivo", "section": "Partes del archivo",
    "imports": "Funciones del sistema que usa", "exports": "Funciones que ofrece", "datadirectories": "Estructura interna",
    "richheader": "Herramientas con que se compiló", "authenticode": "Firma digital", "pefilewarnings": "Anomalías de formato",
}
TERMINO_POR_GRUPO = {
    "byteentropy": "entropía", "header": "encabezado", "section": "sección", "exports": "exportaciones",
    "datadirectories": "reubicaciones", "authenticode": "firma digital", "pefilewarnings": "encabezado",
}


def _fecha(ts):
    try:
        return _dt.datetime.utcfromtimestamp(float(ts)).strftime("%d/%m/%Y")
    except (OverflowError, OSError, ValueError):
        return "fecha no válida"


def _si(x):
    return float(x) >= 0.5


# Características seleccionadas en la corrida 1 (clave = nombre legible del diccionario de datos).
# "nombre": etiqueta corta para tabla y gráfica; "termino": entrada del glosario; "observacion": frase según el valor crudo.
CARACTERISTICAS = {
    "header.characteristics.DLL": {
        "nombre": "Tipo de archivo (programa o biblioteca)", "termino": "biblioteca (DLL)",
        "observacion": lambda x: ("Es una biblioteca (DLL): un archivo que otros programas usan y que no se abre solo."
                                  if _si(x) else "Es un programa ejecutable (.exe), no una biblioteca (DLL)."),
    },
    "authenticode.latest_signing_time": {
        "nombre": "Firma digital (fecha de la firma)", "termino": "firma digital",
        "observacion": lambda x: (f"Tiene firma digital con sello de fecha del {_fecha(x)}."
                                  if float(x) > 0 else "No tiene firma digital (o su firma no tiene sello de fecha)."),
    },
    "authenticode.chain_max_depth": {
        "nombre": "Firma digital (certificados que la respaldan)", "termino": "firma digital",
        "observacion": lambda x: (f"Su firma digital está respaldada por una cadena de {int(round(float(x)))} certificado(s)."
                                  if float(x) > 0 else "No tiene certificados de firma digital."),
    },
    "authenticode.empty_program_name": {
        "nombre": "Firma digital (nombre del programa)", "termino": "firma digital",
        "observacion": lambda x: ("Está firmado, pero la firma no indica el nombre del programa."
                                  if _si(x) else "Si tiene firma digital, esta indica el nombre del programa."),
    },
    "exports.has_exports": {
        "nombre": "Funciones que ofrece a otros programas", "termino": "exportaciones",
        "observacion": lambda x: ("Ofrece funciones a otros programas (tiene exportaciones), como suelen hacerlo las bibliotecas."
                                  if _si(x) else "No ofrece funciones a otros programas (no tiene exportaciones)."),
    },
    "pefilewarnings.w67_Suspicious flags set for section": {
        "nombre": "Una parte se puede modificar y ejecutar a la vez", "termino": "sección",
        "observacion": lambda x: ("Una de sus partes está marcada para poder modificarse y ejecutarse al mismo tiempo, algo poco "
                                  "habitual en programas normales y típico de código empaquetado."
                                  if _si(x) else "Ninguna de sus partes está marcada para modificarse y ejecutarse a la vez, como es normal."),
    },
    "pefilewarnings.w66_SizeOfHeaders is smaller than AddressOfE": {
        "nombre": "Punto de arranque en un lugar anómalo", "termino": "encabezado",
        "observacion": lambda x: ("El punto donde arranca el programa está dentro de la zona del encabezado: una estructura anómala "
                                  "que Windows 8 o posterior no ejecuta."
                                  if _si(x) else "El punto de arranque del programa está donde debe estar (fuera del encabezado)."),
    },
    "datadirectories.has_relocs": {
        "nombre": "Tabla de reubicaciones", "termino": "reubicaciones",
        "observacion": lambda x: ("Incluye tabla de reubicaciones: puede cargarse en distintas posiciones de memoria, como los programas modernos."
                                  if _si(x) else "No incluye tabla de reubicaciones."),
    },
    "header.dll_characteristics.DYNAMIC_BASE": {
        "nombre": "Protección ASLR (posición aleatoria en memoria)", "termino": "protecciones del sistema (ASLR/DEP)",
        "observacion": lambda x: ("Tiene activada la protección ASLR, habitual en programas compilados con herramientas modernas."
                                  if _si(x) else "No tiene activada la protección ASLR."),
    },
    "header.dll_characteristics.NX_COMPAT": {
        "nombre": "Protección DEP (no ejecutar datos)", "termino": "protecciones del sistema (ASLR/DEP)",
        "observacion": lambda x: ("Tiene activada la protección DEP, habitual en programas compilados con herramientas modernas."
                                  if _si(x) else "No tiene activada la protección DEP."),
    },
    "header.dll_characteristics.TERMINAL_SERVER_AWARE": {
        "nombre": "Compatibilidad con escritorio remoto", "termino": "encabezado",
        "observacion": lambda x: ("Declara compatibilidad con sesiones de escritorio remoto, una marca típica de programas compilados con herramientas modernas."
                                  if _si(x) else "No declara compatibilidad con sesiones de escritorio remoto."),
    },
    "header.characteristics.RELOCS_STRIPPED": {
        "nombre": "Información de reubicación eliminada", "termino": "reubicaciones",
        "observacion": lambda x: ("Se le quitó la información de reubicación: solo puede cargarse en una posición fija de memoria."
                                  if _si(x) else "Conserva la información de reubicación."),
    },
    "header.characteristics.LINE_NUMS_STRIPPED": {
        "nombre": "Marca antigua del compilador (números de línea)", "termino": "encabezado",
        "observacion": lambda x: ("Lleva la marca de 'números de línea eliminados', propia de compiladores antiguos."
                                  if _si(x) else "No lleva la marca de 'números de línea eliminados'."),
    },
    "section.overlay.entropy": {
        "nombre": "Datos añadidos al final del archivo", "termino": "datos añadidos (overlay)",
        "observacion": lambda x: ((f"Tiene datos añadidos al final del archivo, {'muy desordenados: parecen comprimidos o cifrados' if float(x) >= 7 else 'medianamente desordenados' if float(x) >= 5 else 'poco desordenados'} "
                                   f"(entropía {float(x):.1f} de 8).")
                                  if float(x) > 0 else "No tiene datos añadidos al final del archivo."),
    },
    "byteentropy.entropia15_byte15": {
        "nombre": "Contenido que parece comprimido o cifrado", "termino": "entropía",
        "observacion": lambda x: (f"Alrededor del {100 * float(x):.0f} % de su contenido se ve muy desordenado, como pasa con datos comprimidos o cifrados."
                                  if float(x) > 0.005 else "Casi nada de su contenido se ve comprimido o cifrado."),
    },
}


def describir_caracteristica(nombre_legible, grupo, valor):
    """Devuelve (nombre_corto, observacion, termino) para cualquier característica, conocida o no."""
    ficha = CARACTERISTICAS.get(nombre_legible)
    if ficha is not None:
        return ficha["nombre"], ficha["observacion"](valor), ficha["termino"]
    detalle = nombre_legible.split(".", 1)[-1] if "." in nombre_legible else nombre_legible
    nombre_corto = f"{GRUPOS_CORTOS.get(grupo, grupo)}: {detalle[:28]}"
    observacion = f"El dato '{detalle}' (grupo: {GRUPOS_CORTOS.get(grupo, grupo).lower()}) tiene el valor {float(valor):g}."
    return nombre_corto, observacion, TERMINO_POR_GRUPO.get(grupo)


def _peso(contribucion, maximo):
    """Peso relativo del factor frente al mayor del mismo archivo, en palabras (no depende de la escala de SHAP)."""
    r = abs(contribucion) / maximo if maximo > 0 else 0.0
    return "mucho" if r >= 0.66 else "un poco" if r >= 0.33 else "ligeramente"


def traducir(columnas, nombres, grupos, valores_crudos, contribuciones, top_n=5):
    """Convierte el vector SHAP de UN archivo en factores explicados en lenguaje sencillo.

    columnas / nombres / grupos: listas paralelas (p. ej. 'f739', 'header.characteristics.DLL', 'header');
    valores_crudos: valores de las características sin escalar; contribuciones: valores SHAP del archivo.
    Devuelve una lista de diccionarios ordenada por |SHAP| (máximo top_n)."""
    orden = [int(i) for i in sorted(range(len(contribuciones)), key=lambda i: -abs(contribuciones[i])) if abs(contribuciones[i]) > 1e-6][:top_n]
    maximo = max((abs(contribuciones[i]) for i in orden), default=0.0)
    factores = []
    for i in orden:
        nombre_corto, observacion, termino = describir_caracteristica(nombres[i], grupos[i], valores_crudos[i])
        hacia_malware = contribuciones[i] > 0
        peso = _peso(contribuciones[i], maximo)
        efecto_corto = "hace desconfiar" if hacia_malware else "hace confiar"
        explicacion = f"{observacion} Para el sistema, esto {'aumentó' if hacia_malware else 'redujo'} la sospecha {peso}."
        factores.append({
            "caracteristica": columnas[i], "nombre": nombres[i], "grupo": grupos[i],
            "valor": float(valores_crudos[i]), "aporte_shap": round(float(contribuciones[i]), 4),
            "efecto": "aumenta la sospecha" if hacia_malware else "reduce la sospecha",   # compatibilidad con la versión anterior
            "nombre_amigable": nombre_corto, "observacion": observacion, "efecto_corto": efecto_corto,
            "peso": peso, "termino": termino, "explicacion": explicacion,
        })
    return factores


def glosario_para(factores):
    """Entradas del glosario que corresponden a los factores mostrados (sin repetir, en orden de aparición)."""
    vistos, salida = set(), []
    for f in factores:
        t = f.get("termino")
        if t and t in GLOSARIO and t not in vistos:
            vistos.add(t)
            salida.append((t, GLOSARIO[t]))
    return salida


def frases(factores):
    """Solo las frases, para registros de texto (muestra explicada, ejemplos del documento)."""
    if not factores:
        return ["Ninguna característica individual domina la decisión: el sistema combinó pequeñas señales de muchas variables."]
    return [f["explicacion"] for f in factores]
