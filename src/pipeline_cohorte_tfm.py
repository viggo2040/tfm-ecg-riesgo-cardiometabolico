"""
Pipeline reproducible para construir la cohorte experimental anonimizada del TFM.

Entrada:
    Base de Datos Original.xlsx

Salida:
    Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx
    Diccionario_Normalizacion_Antecedentes.csv
    Log_Transformacion_Cohorte_TFM.txt
"""

from pathlib import Path
import re
import unicodedata
import numpy as np
import pandas as pd


INPUT_PATH = Path("Base de Datos Original.xlsx")
OUTPUT_XLSX = Path("Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx")
DICT_CSV = Path("Diccionario_Normalizacion_Antecedentes.csv")
LOG_TXT = Path("Log_Transformacion_Cohorte_TFM.txt")


def strip_accents(value):
    if pd.isna(value):
        return ""
    return "".join(
        char for char in unicodedata.normalize("NFD", str(value))
        if unicodedata.category(char) != "Mn"
    )


def clean_text(value):
    value = strip_accents(value).lower()
    value = re.sub(r"[\n\r\t]", " ", value)
    value = re.sub(r"[/,+;|(){}\[\]:=._-]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def extract_number(value):
    if pd.isna(value):
        return np.nan
    match = re.search(r"[-+]?\d+([.,]\d+)?", strip_accents(str(value)))
    return float(match.group(0).replace(",", ".")) if match else np.nan


def normalize_yes_no(value):
    text = clean_text(value)
    if text in ["si", "sí", "s", "yes", "y", "positivo", "presente"] or re.search(r"\bsi\b", text):
        return 1
    if text in ["no", "n", "negativo", "ausente"] or re.search(r"\bno\b", text):
        return 0
    return np.nan


CATEGORIES = {
    "ANT_HTA": [r"\bhta\b", r"hipertension", r"hipertenso", r"hipertensa", r"presion alta"],
    "ANT_DIABETES": [r"\bdm\b", r"\bdm2\b", r"diabetes", r"diabetico", r"diabetica"],
    "ANT_DISLIPIDEMIA": [r"\bdlp\b", r"dislipidemia", r"hiperlipidemia", r"colesterol", r"hipercolesterolemia"],
    "ANT_TABAQUISMO": [r"tabaquismo", r"fumador", r"fumadora", r"tabaco", r"cigarr"],
    "ANT_OBESIDAD": [r"obesidad", r"obeso", r"obesa"],
    "ANT_INFARTO": [r"\biam\b", r"infarto", r"miocardio"],
    "ANT_ACV": [r"\bacv\b", r"accidente cerebrovascular", r"ictus", r"\bave\b"],
    "ANT_CARDIOPATIA": [r"cardiopatia", r"coronaria", r"cardiaca", r"cardiaco", r"angina"],
    "ANT_ARRITMIA": [r"arritmia", r"fibrilacion", r"\bfa\b"],
    "ANT_ENF_RENAL": [r"\birc\b", r"renal", r"rinon", r"riñon", r"nefropatia"],
    "ANT_EPOC": [r"\bepoc\b", r"enfermedad pulmonar obstructiva"],
    "ANT_CANCER": [r"cancer", r"tumor", r"neoplasia"],
    "ANT_HIPOTIROIDISMO": [r"hipotiroidismo", r"hipotiroid"],
    "ANT_SALUD_MENTAL": [r"depresion", r"ansiedad", r"psiquiatr", r"bipolar", r"trastorno"],
    "ANT_ALCOHOL": [r"alcohol", r"bebedor", r"bebedora"],
    "ANT_ASMA": [r"\basma\b", r"asmatico", r"asmatica"],
}

NEGATION_TERMS = [
    "no", "niega", "sin", "descarta", "no refiere",
    "sin antecedentes", "no presenta", "no registra", "negativo"
]


def detect_category(text, patterns):
    text = clean_text(text)
    if not text:
        return 0

    for pattern in patterns:
        for match in re.finditer(pattern, text):
            context = text[max(0, match.start() - 35):match.start()]
            negated = any(re.search(rf"\b{re.escape(term)}\b", context) for term in NEGATION_TERMS)
            if not negated:
                return 1
    return 0


def build_cohort(input_path=INPUT_PATH):
    df = pd.read_excel(input_path, sheet_name=0)
    df.columns = [str(column).strip() for column in df.columns]

    out = pd.DataFrame({
        "PACIENTE_ID": [f"PAC_{index:06d}" for index in range(1, len(df) + 1)]
    })

    direct_identifiers = [column for column in ["Nombre", "Rut", "FechaNacimiento"] if column in df.columns]

    if "UltimaFechaAtencion" in df.columns:
        dates = pd.to_datetime(df["UltimaFechaAtencion"], errors="coerce")
        out["UltimaAtencion_Anio"] = dates.dt.year
        out["UltimaAtencion_Mes"] = dates.dt.month
        out["DiasDesdePrimeraAtencion"] = (dates - dates.min()).dt.days

    exclude = set(direct_identifiers + ["AntecedentesMedicos", "UltimaFechaAtencion"])
    for column in df.columns:
        if column not in exclude:
            out[column] = df[column]

    numeric_columns = {
        "Peso": "Peso_kg",
        "Altura": "Altura_m",
        "IMC": "IMC_num",
        "PA_Sistolica": "PA_Sistolica_mmHg",
        "PA_Diastolica": "PA_Diastolica_mmHg",
        "Glicemia": "Glicemia_mg_dl",
        "ColesterolTotal": "ColesterolTotal_mg_dl",
        "HDL": "HDL_mg_dl",
        "LDL": "LDL_mg_dl",
        "Trigliceridos": "Trigliceridos_mg_dl",
        "Hemoglobina": "Hemoglobina_gr_pct",
        "Creatinina": "Creatinina_mg_dl",
    }

    for source, target in numeric_columns.items():
        if source in df.columns:
            out[target] = df[source].map(extract_number)

    if "Tabaquismo" in df.columns:
        out["Tabaquismo_bin"] = df["Tabaquismo"].map(normalize_yes_no)

    if "Diabetes" in df.columns:
        out["Diabetes_bin"] = df["Diabetes"].map(normalize_yes_no)

    raw_antecedents = (
        df["AntecedentesMedicos"].fillna("").astype(str)
        if "AntecedentesMedicos" in df.columns
        else pd.Series([""] * len(df))
    )

    normalized_labels = []
    category_arrays = {category: np.zeros(len(df), dtype=int) for category in CATEGORIES}

    for index, text in enumerate(raw_antecedents):
        detected_labels = []
        for category, patterns in CATEGORIES.items():
            value = detect_category(text, patterns)
            category_arrays[category][index] = value
            if value:
                detected_labels.append(category.replace("ANT_", "").lower())
        normalized_labels.append(", ".join(detected_labels))

    for category, values in category_arrays.items():
        out[category] = values

    out["AntecedentesMedicos_Normalizado"] = normalized_labels
    out["AntecedentesMedicos_TextoOriginal_Presente"] = raw_antecedents.map(
        lambda value: 1 if clean_text(value) else 0
    )

    def ge(column, threshold):
        return np.where(pd.to_numeric(out[column], errors="coerce") >= threshold, 1, 0)

    if "PA_Sistolica_mmHg" in out:
        out["FLAG_PA_SISTOLICA_ALTA"] = ge("PA_Sistolica_mmHg", 140)
    if "PA_Diastolica_mmHg" in out:
        out["FLAG_PA_DIASTOLICA_ALTA"] = ge("PA_Diastolica_mmHg", 90)
    if "Glicemia_mg_dl" in out:
        out["FLAG_GLICEMIA_ALTA"] = ge("Glicemia_mg_dl", 126)
    if "LDL_mg_dl" in out:
        out["FLAG_LDL_ALTO"] = ge("LDL_mg_dl", 130)
    if "Trigliceridos_mg_dl" in out:
        out["FLAG_TRIGLICERIDOS_ALTOS"] = ge("Trigliceridos_mg_dl", 150)
    if "IMC_num" in out:
        out["FLAG_OBESIDAD_IMC"] = ge("IMC_num", 30)

    if "HDL_mg_dl" in out and "Sexo" in out:
        female = out["Sexo"].astype(str).str.lower().str.contains("femen", na=False)
        out["FLAG_HDL_BAJO"] = np.where(
            (female & (out["HDL_mg_dl"] < 50)) |
            (~female & (out["HDL_mg_dl"] < 40)),
            1,
            0
        )

    return df, out, direct_identifiers


def export_outputs(df, out, direct_identifiers):
    clinical_binary_cols = [column for column in out.columns if column.startswith("ANT_")]
    flag_cols = [column for column in out.columns if column.startswith("FLAG_")]

    summary = pd.DataFrame([
        ["Filas originales", len(df)],
        ["Columnas originales", df.shape[1]],
        ["Filas finales", len(out)],
        ["Columnas finales", out.shape[1]],
        ["Identificadores directos eliminados", ", ".join(direct_identifiers)],
        ["Variables de antecedentes generadas", len(clinical_binary_cols)],
        ["Flags cardiometabólicos generados", len(flag_cols)],
        ["Texto original AntecedentesMedicos conservado", "No"],
    ], columns=["Metrica", "Valor"])

    anonymization = pd.DataFrame([
        ["Nombre", "Eliminado", "Identificador directo"],
        ["Rut", "Eliminado", "Identificador nacional directo"],
        ["FechaNacimiento", "Eliminado", "Cuasi-identificador; se conserva Edad"],
        ["UltimaFechaAtencion", "Generalizado", "Año, mes y días relativos"],
        ["AntecedentesMedicos", "Derivado y no conservado", "Texto clínico libre sensible"],
        ["PACIENTE_ID", "Creado", "Identificador secuencial no derivado de datos personales"],
    ], columns=["Campo original", "Tratamiento", "Justificacion"])

    dictionary = pd.DataFrame([{
        "Variable": category,
        "Descripcion": category.replace("ANT_", "").replace("_", " ").lower(),
        "Patrones": " | ".join(patterns),
        "Tipo": "Binaria derivada de AntecedentesMedicos",
    } for category, patterns in CATEGORIES.items()])

    counts = pd.DataFrame([{
        "Variable": column,
        "Positivos": int(pd.to_numeric(out[column], errors="coerce").fillna(0).sum()),
        "Pct": round(float(pd.to_numeric(out[column], errors="coerce").fillna(0).mean() * 100), 2),
    } for column in clinical_binary_cols + flag_cols])

    completeness = pd.DataFrame([{
        "Variable": column,
        "Nulos": int(out[column].isna().sum()),
        "Pct_Nulos": round(float(out[column].isna().mean() * 100), 2),
    } for column in out.columns])

    sheets = {
        "Cohorte_Anonimizada": out,
        "Resumen_Validacion": summary,
        "Anonimizacion": anonymization,
        "Diccionario_Clinico": dictionary,
        "Conteos_Variables": counts,
        "Completitud": completeness,
    }

    with pd.ExcelWriter(OUTPUT_XLSX, engine="xlsxwriter") as writer:
        for sheet_name, data in sheets.items():
            data.to_excel(writer, sheet_name=sheet_name, index=False)

    dictionary.to_csv(DICT_CSV, index=False, encoding="utf-8-sig")

    LOG_TXT.write_text(
        "\n".join([
            "LOG DE TRANSFORMACION - COHORTE TFM",
            f"Filas originales: {len(df)}",
            f"Columnas originales: {df.shape[1]}",
            f"Filas finales: {len(out)}",
            f"Columnas finales: {out.shape[1]}",
            f"Identificadores directos eliminados: {', '.join(direct_identifiers)}",
            "Texto original AntecedentesMedicos conservado: No",
            f"Filas preservadas: {len(df) == len(out)}",
            f"Identificadores directos presentes en salida: {[c for c in direct_identifiers + ['AntecedentesMedicos'] if c in out.columns]}",
        ]),
        encoding="utf-8"
    )


def main():
    df, out, direct_identifiers = build_cohort(INPUT_PATH)
    export_outputs(df, out, direct_identifiers)


if __name__ == "__main__":
    main()
