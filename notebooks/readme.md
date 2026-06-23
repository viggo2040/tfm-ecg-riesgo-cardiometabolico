# Notebooks del TFM

Esta carpeta contiene los notebooks desarrollados para reproducir los procesos técnicos asociados al Trabajo Fin de Máster:

**Evaluación del valor incremental de parámetros ECG en riesgo cardiometabólico**

El repositorio documenta una arquitectura experimental de Inteligencia Artificial clínica multimodal orientada a construir una cohorte analítica reproducible, integrar información clínica estructurada, antecedentes médicos procesados mediante PLN/NLP y parámetros electrocardiográficos extraídos desde reportes ECG en formato PDF, y evaluar su aporte dentro de modelos predictivos de riesgo cardiometabólico.

## Objetivo de la carpeta

El objetivo de esta carpeta es centralizar los cuadernos ejecutables que respaldan la trazabilidad técnica del TFM.

Los notebooks permiten reproducir, documentar y auditar las principales transformaciones realizadas sobre los datos, desde la base clínica original hasta los datasets preparados para modelado predictivo, evaluación incremental del aporte ECG e interpretabilidad mediante SHAP.

El flujo está diseñado para mantener separación entre:

- datos clínicos originales;
- artefactos privados de trazabilidad;
- bases clínicas anonimizadas;
- dataset ECG estructurado;
- cohorte multimodal integrada;
- datasets experimentales por escenario;
- métricas, modelos e interpretabilidad.

## Orden recomendado de ejecución

| Orden | Notebook | Propósito | Entrada principal | Salida principal |
| ----: | -------- | --------- | ----------------- | ---------------- |
| 1 | `01_proceso_pln1_anonimizacion_normalizacion.ipynb` | Anonimización, normalización clínica, PLN/NLP, generación de identificadores internos y trazabilidad privada | `Base de Datos Original.xlsx` | `Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx` + `crosswalk_paciente_ecg.xlsx` |
| 2 | `02_proceso_pln2_subsets_baterias.ipynb` | Cálculo de completitud y segmentación estructural en pseudo-baterías clínicas | `Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx` | `Base_Ordenada_Subsets_TFM.xlsx` |
| 3 | `03_extraccion_ecg_pdf.ipynb` | Extracción estructurada de parámetros ECG desde reportes PDF | Carpeta de reportes ECG PDF | `ecg_dataset.xlsx` |
| 4 | `04_integracion_ecg.ipynb` | Integración determinística de parámetros ECG con la cohorte clínica | `Base_Ordenada_Subsets_TFM.xlsx` + `crosswalk_paciente_ecg.xlsx` + `ecg_dataset.xlsx` | `Dataset_Multimodal_Integrado_TFM.xlsx` |
| 5 | `05_construccion_endpoint.ipynb` | Construcción del endpoint experimental y generación de datasets por escenario | Dataset multimodal integrado | Datasets E1, E2, E3 y E4 + `RIESGO_CARDIOMETABOLICO` |
| 6 | `06_modelado_predictivo.ipynb` | Entrenamiento y evaluación base de modelos supervisados por escenario | Datasets experimentales E1–E4 | Métricas por modelo y escenario |
| 7 | `07_evaluacion_incremental_ecg.ipynb` | Comparación incremental entre escenarios clínicos, NLP, ECG y multimodal completo | Métricas consolidadas | Tablas comparativas de diferencias e impacto incremental |
| 8 | `08_interpretabilidad_shap.ipynb` | Interpretabilidad de modelos mediante SHAP | Modelos entrenados y datasets finales | Gráficos y tablas SHAP |

## Arquitectura general del pipeline

```text
Base de Datos Original.xlsx
        ↓
01_proceso_pln1_anonimizacion_normalizacion.ipynb
        ↓
Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx
crosswalk_paciente_ecg.xlsx
        ↓
02_proceso_pln2_subsets_baterias.ipynb
        ↓
Base_Ordenada_Subsets_TFM.xlsx
        ↓
03_extraccion_ecg_pdf.ipynb
        ↓
ecg_dataset.xlsx
        ↓
04_integracion_ecg.ipynb
        ↓
Dataset_Multimodal_Integrado_TFM.xlsx
        ↓
05_construccion_endpoint.ipynb
        ↓
Datasets experimentales E1, E2, E3 y E4
        ↓
06_modelado_predictivo.ipynb
        ↓
Métricas por modelo y escenario
        ↓
07_evaluacion_incremental_ecg.ipynb
        ↓
Comparación incremental de modalidades
        ↓
08_interpretabilidad_shap.ipynb
        ↓
Interpretabilidad global y local mediante SHAP
```

## Identificadores y trazabilidad

El pipeline utiliza identificadores internos para preservar trazabilidad analítica sin exponer identificadores directos de pacientes.

### Identificadores principales

```text
PACIENTE_ID
REGISTRO_ID
clave_matching
```

`PACIENTE_ID` representa el identificador anónimo del paciente dentro de la cohorte clínica.

`REGISTRO_ID` representa el identificador único del registro clínico o evento analítico. Permite distinguir múltiples registros asociados a un mismo paciente cuando corresponda.

`clave_matching` representa una clave operacional utilizada para asociar reportes ECG PDF con registros clínicos mediante una estructura normalizada basada en nombre de paciente y fecha. Esta clave se mantiene como parte de los artefactos privados de trazabilidad y no debe publicarse en repositorios abiertos.

### Archivo privado de correspondencia

El archivo:

```text
crosswalk_paciente_ecg.xlsx
```

permite relacionar la cohorte clínica anonimizada con el dataset ECG estructurado.

Estructura mínima:

```text
PACIENTE_ID
REGISTRO_ID
clave_matching
```

Estructura recomendada:

```text
PACIENTE_ID
REGISTRO_ID
nombre_paciente_norm
fecha_atencion_norm
clave_matching
clave_hash_privada
estado_validacion
metodo_match
observaciones
```

Este archivo es un artefacto privado de trazabilidad y no sera subido a GitHub si contiene nombres normalizados, fechas exactas, hashes derivados de identificadores o cualquier información potencialmente reidentificable.

## Proceso 1: Anonimización, normalización clínica y PLN/NLP

Notebook asociado:

```text
01_proceso_pln1_anonimizacion_normalizacion.ipynb
```

Entrada principal:

```text
Base de Datos Original.xlsx
```

Salidas principales:

```text
Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx
crosswalk_paciente_ecg.xlsx
Auditoria_Privada_Trazabilidad_TFM.xlsx
Diccionario_Normalizacion_Antecedentes.csv
Log_Transformacion_Cohorte_TFM.txt
```

### Objetivo metodológico

Este proceso transforma la base clínica original en una cohorte anonimizada, estructurada y analíticamente consistente. Además, genera los identificadores internos necesarios para mantener trazabilidad entre fuentes clínicas, antecedentes textuales y reportes ECG.

El proceso permite:

- proteger la privacidad de los pacientes mediante anonimización;
- eliminar identificadores directos de la base analítica;
- generar `PACIENTE_ID` y `REGISTRO_ID`;
- construir una tabla privada de correspondencia para integración ECG;
- normalizar variables clínicas numéricas;
- procesar antecedentes médicos registrados como texto libre;
- generar variables binarias derivadas mediante reglas PLN/NLP;
- construir indicadores clínicos cardiometabólicos;
- documentar transformaciones mediante diccionarios, logs y artefactos de auditoría.

### Transformaciones principales

1. Lectura de la base clínica original.
2. Limpieza y estandarización de nombres de columnas.
3. Normalización de identificadores internos.
4. Generación de `PACIENTE_ID` y `REGISTRO_ID`.
5. Construcción de `nombre_paciente_norm`, `fecha_atencion_norm` y `clave_matching`.
6. Generación de `crosswalk_paciente_ecg.xlsx` como artefacto privado de trazabilidad.
7. Eliminación de identificadores directos desde la base analítica.
8. Normalización de variables clínicas numéricas.
9. Codificación binaria de variables clínicas como tabaquismo y diabetes.
10. Limpieza textual de antecedentes médicos.
11. Detección de conceptos clínicos mediante reglas PLN/NLP.
12. Detección básica de negaciones clínicas.
13. Generación de variables `ANT_*`.
14. Generación de flags cardiometabólicos `FLAG_*`.
15. Exportación de base clínica anonimizada, diccionarios y logs.

### Variables generadas mediante PLN/NLP

```text
ANT_HTA
ANT_DIABETES
ANT_DISLIPIDEMIA
ANT_TABAQUISMO
ANT_OBESIDAD
ANT_INFARTO
ANT_ACV
ANT_CARDIOPATIA
ANT_ARRITMIA
ANT_ENF_RENAL
ANT_EPOC
ANT_CANCER
ANT_HIPOTIROIDISMO
ANT_SALUD_MENTAL
ANT_ALCOHOL
ANT_ASMA
```

Estas variables permiten incorporar información clínica previamente no estructurada dentro de los modelos experimentales.

### Indicadores cardiometabólicos generados

```text
FLAG_PA_SISTOLICA_ALTA
FLAG_PA_DIASTOLICA_ALTA
FLAG_GLICEMIA_ALTA
FLAG_LDL_ALTO
FLAG_TRIGLICERIDOS_ALTOS
FLAG_OBESIDAD_IMC
FLAG_HDL_BAJO
```

Estos indicadores se utilizan posteriormente para la construcción del endpoint operacional:

```text
RIESGO_CARDIOMETABOLICO
```

## Proceso 2: Segmentación estructural y pseudo-baterías clínicas

Notebook asociado:

```text
02_proceso_pln2_subsets_baterias.ipynb
```

Entrada principal:

```text
Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx
```

Salida principal:

```text
Base_Ordenada_Subsets_TFM.xlsx
```

### Objetivo metodológico

Este proceso caracteriza la heterogeneidad estructural de la cohorte clínica y construye subconjuntos basados en patrones de disponibilidad de información.

La cohorte presenta diferencias reales en disponibilidad de variables clínicas, antecedentes procesados y exámenes complementarios. En lugar de eliminar todos los registros incompletos, el pipeline representa explícitamente la disponibilidad diferencial de información mediante pseudo-baterías clínicas.

Este proceso permite:

- preservar registros clínicos útiles;
- evitar una reducción excesiva del tamaño muestral;
- representar patrones de completitud;
- identificar configuraciones estructurales de disponibilidad;
- preparar evaluaciones de estabilidad entre subconjuntos;
- mantener `PACIENTE_ID` y `REGISTRO_ID` durante todo el flujo.

### Cálculo de completitud

Se calcula:

```text
TOTAL_RESULTADOS
PORCENTAJE_COMPLETITUD
```

`TOTAL_RESULTADOS` corresponde al conteo de campos disponibles por registro dentro de un conjunto definido de variables clínicas, normalizadas y derivadas.

`PORCENTAJE_COMPLETITUD` expresa el porcentaje de disponibilidad relativa del registro respecto al total de variables evaluadas.

### Segmentación estructural

Se construye una matriz binaria de presencia/ausencia de variables clínicas y derivadas. Esta matriz no representa similitud clínica entre pacientes; representa similitud estructural en disponibilidad de datos.

Sobre esta matriz se aplica clustering estructural, con semilla fija para reproducibilidad.

Subconjuntos generados:

```text
BATERIA_A
BATERIA_B
BATERIA_C
BATERIA_D
```

Las hojas esperadas del archivo final son:

```text
BASE_COMPLETA
BATERIA_A
BATERIA_B
BATERIA_C
BATERIA_D
```

## Proceso 3: Extracción estructurada de datos ECG desde PDF

Notebook asociado:

```text
03_extraccion_ecg_pdf.ipynb
```

Entrada principal:

```text
Carpeta de reportes ECG PDF
```

Salidas principales:

```text
ecg_dataset.xlsx
ecg_dataset.csv
ecg_resumen.txt
```

### Objetivo metodológico

Este proceso extrae parámetros electrocardiográficos desde reportes ECG en formato PDF y los transforma en un dataset tabular compatible con la cohorte clínica.

El proceso permite:

- leer reportes ECG PDF de forma recursiva;
- extraer texto embebido desde los documentos;
- recuperar parámetros ECG estructurados;
- normalizar valores numéricos con coma decimal;
- construir `clave_matching` compatible con el crosswalk privado;
- identificar duplicados del mismo paciente en el mismo día;
- generar un dataset ECG auditable y reutilizable.

### Variables ECG extraídas

```text
ECG_HR
ECG_PR
ECG_QRS
ECG_QTC
ECG_AXIS
QT
QRS_AXIS
RV5
SV1
RV1
SV5
ECG_ANALYSIS
ECG_DIAGNOSIS
```

### Variables auxiliares generadas

```text
ECG_ID
archivo_origen
ruta_relativa
año
mes
fecha_examen
fecha
paciente_id_pdf
sexo
edad
nombre_paciente
nombre_paciente_norm
clave_matching
clave_hash_ecg
num_ecg_mismo_paciente_fecha
duplicado_mismo_dia
rank_ecg_mismo_paciente_fecha
estado_match_ecg
pdf_valido
parametros_extraidos
observaciones_extraccion
```

### Parámetros core ECG

Los parámetros principales evaluados durante control de calidad son:

```text
ECG_HR
ECG_PR
ECG_QRS
ECG_QTC
ECG_AXIS
```

El identificador extraído desde el PDF no se utiliza como identificador clínico real. La integración con la cohorte clínica se realiza posteriormente mediante `crosswalk_paciente_ecg.xlsx`.

## Proceso 4: Integración ECG con cohorte clínica

Notebook asociado:

```text
04_integracion_ecg.ipynb
```

Entradas principales:

```text
Base_Ordenada_Subsets_TFM.xlsx
crosswalk_paciente_ecg.xlsx
ecg_dataset.xlsx
```

Salidas principales:

```text
Dataset_Multimodal_Integrado_TFM.xlsx
Auditoria_Integracion_ECG_TFM.xlsx
Reporte_Integracion_ECG_TFM.txt
```

### Objetivo metodológico

Este proceso vincula la cohorte clínica segmentada con los parámetros ECG extraídos desde PDF mediante una integración determinística basada en identificadores internos y tabla privada de correspondencia.

La integración utiliza la siguiente relación:

```text
Base clínica: PACIENTE_ID / REGISTRO_ID
Crosswalk: PACIENTE_ID / REGISTRO_ID + clave_matching
Dataset ECG: clave_matching
```

### Resultado esperado

El resultado es una cohorte multimodal integrada con:

```text
PACIENTE_ID
REGISTRO_ID
variables clínicas estructuradas
variables derivadas mediante NLP
variables de completitud
SUBSET_BATERIA
ECG_HR
ECG_PR
ECG_QRS
ECG_QTC
ECG_AXIS
QT
RV5
SV1
RV1
SV5
flag_ecg_disponible
```

Las columnas con información sensible o potencialmente reidentificable se excluyen de la salida analítica destinada a modelado.

## Proceso 5: Construcción del endpoint experimental

Notebook asociado:

```text
05_construccion_endpoint.ipynb
```

Entrada principal:

```text
Dataset_Multimodal_Integrado_TFM.xlsx
```

Salidas principales:

```text
Dataset_E1_Clinico.xlsx
Dataset_E2_Clinico_NLP.xlsx
Dataset_E3_Clinico_ECG.xlsx
Dataset_E4_Clinico_NLP_ECG.xlsx
```

### Objetivo metodológico

Este proceso construye la variable objetivo operacional del estudio:

```text
RIESGO_CARDIOMETABOLICO
```

El endpoint representa una aproximación operacional al riesgo cardiometabólico compuesto, construida a partir de la acumulación de factores de riesgo disponibles en la cohorte.

La variable no corresponde a un evento cardiovascular observado ni a una escala clínica validada externamente. Su finalidad es experimental y permite comparar escenarios predictivos bajo una definición reproducible.

### Escenarios experimentales generados

```text
E1. Clínico
E2. Clínico + NLP
E3. Clínico + ECG
E4. Clínico + NLP + ECG
```

Estos escenarios permiten evaluar de forma incremental el aporte de cada modalidad de información.

## Proceso 6: Modelado predictivo

Notebook asociado:

```text
06_modelado_predictivo.ipynb
```

Entrada principal:

```text
Datasets experimentales E1, E2, E3 y E4
```

Salidas principales:

```text
Metricas_Modelado_Predictivo_TFM.xlsx
Modelos entrenados
Predicciones por escenario
```

### Objetivo metodológico

Este proceso entrena y evalúa modelos supervisados sobre los escenarios experimentales definidos.

Modelos considerados:

```text
Logistic Regression
Random Forest
XGBoost
LightGBM
```

Métricas consideradas:

```text
Accuracy
Precision
Recall
F1-Score
ROC-AUC
AUPRC
```

Todos los modelos deben entrenarse bajo condiciones homogéneas para preservar comparabilidad entre escenarios.

## Proceso 7: Evaluación incremental de parámetros ECG

Notebook asociado:

```text
07_evaluacion_incremental_ecg.ipynb
```

Entrada principal:

```text
Metricas_Modelado_Predictivo_TFM.xlsx
```

Salidas principales:

```text
Comparacion_Incremental_ECG_TFM.xlsx
Tablas_Incrementales_TFM.xlsx
Reporte_Evaluacion_Incremental_TFM.txt
```

### Objetivo metodológico

Este proceso consolida las métricas obtenidas y evalúa el aporte incremental de las modalidades NLP y ECG.

Comparaciones principales:

```text
E1 Clínico → E2 Clínico + NLP
E1 Clínico → E3 Clínico + ECG
E2 Clínico + NLP → E4 Clínico + NLP + ECG
E1 Clínico → E4 Clínico + NLP + ECG
```

Diferencias evaluadas:

```text
ΔROC-AUC
ΔAUPRC
ΔF1
ΔRecall
ΔPrecision
```

El objetivo central es determinar si la incorporación de parámetros ECG estructurados mejora el desempeño predictivo respecto a los escenarios sin ECG.

## Proceso 8: Interpretabilidad mediante SHAP

Notebook asociado:

```text
08_interpretabilidad_shap.ipynb
```

Entrada principal:

```text
Modelos entrenados
Datasets experimentales finales
```

Salidas principales:

```text
Resultados_SHAP_TFM.xlsx
Graficos_SHAP/
Reporte_Interpretabilidad_SHAP_TFM.txt
```

### Objetivo metodológico

Este proceso interpreta los modelos entrenados mediante SHAP, con énfasis en la contribución relativa de variables clínicas, NLP y ECG.

El análisis debe permitir:

- identificar variables con mayor importancia global;
- analizar contribuciones locales de predicción;
- determinar si las variables ECG participan entre los predictores relevantes;
- comparar importancia relativa entre modalidades;
- apoyar la interpretación del aporte incremental observado en las métricas.

Variables ECG de interés:

```text
ECG_HR
ECG_PR
ECG_QRS
ECG_QTC
ECG_AXIS
```

## Escenarios experimentales del TFM

La evaluación experimental se organiza en cuatro escenarios:

| Escenario | Variables clínicas | NLP | ECG | Finalidad |
| --------- | ------------------ | --- | --- | --------- |
| E1. Clínico | Sí | No | No | Línea base clínica |
| E2. Clínico + NLP | Sí | Sí | No | Evaluar aporte de antecedentes procesados |
| E3. Clínico + ECG | Sí | No | Sí | Evaluar aporte incremental ECG |
| E4. Clínico + NLP + ECG | Sí | Sí | Sí | Evaluar configuración multimodal completa |

La comparación principal del TFM corresponde a:

```text
E1 Clínico vs E3 Clínico + ECG
```

La comparación complementaria para evaluar el aporte ECG dentro del escenario enriquecido es:

```text
E2 Clínico + NLP vs E4 Clínico + NLP + ECG
```

## Relación con el TFM

Los notebooks respaldan principalmente los siguientes capítulos:

```text
Capítulo 4: Construcción de la cohorte experimental multimodal.
Capítulo 5: Desarrollo experimental y modelado predictivo.
Capítulo 6: Notebooks, código fuente y datos analizados.
Capítulo 7: Conclusiones.
Capítulo 8: Limitaciones y prospectiva.
```

La arquitectura implementada mantiene coherencia con el diseño metodológico del TFM, cuyo objetivo central es evaluar el valor incremental de parámetros electrocardiográficos estructurados derivados de reportes ECG digitales dentro de modelos predictivos de riesgo cardiometabólico.

## Estructura sugerida del repositorio

```text
notebooks/
  01_proceso_pln1_anonimizacion_normalizacion.ipynb
  02_proceso_pln2_subsets_baterias.ipynb
  03_extraccion_ecg_pdf.ipynb
  04_integracion_ecg.ipynb
  05_construccion_endpoint.ipynb
  06_modelado_predictivo.ipynb
  07_evaluacion_incremental_ecg.ipynb
  08_interpretabilidad_shap.ipynb

src/
  extract_ecg.py
  utils_normalizacion.py
  utils_trazabilidad.py
  utils_metricas.py

docs/
  diccionario_variables.md
  metodologia_pipeline.md
  estructura_datasets.md

outputs/
  logs/
  reportes_anonimizados/
  metricas/
  figuras/
```

## Consideraciones de privacidad

La base original, los archivos intermedios con trazabilidad privada, los datasets clínicos reales y los PDFs ECG originales no deben publicarse en repositorios públicos.

No son publicados en GitHub:

```text
Base de Datos Original.xlsx
Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx
Base_Ordenada_Subsets_TFM.xlsx
Dataset_Multimodal_Integrado_TFM.xlsx
crosswalk_paciente_ecg.xlsx
Auditoria_Privada_Trazabilidad_TFM.xlsx
Auditoria_Integracion_ECG_TFM.xlsx
ecg_dataset.xlsx
ecg_dataset.csv
PDFs ECG originales
archivos con nombres de pacientes
rutas relativas con identificadores
RUT
fechas de nacimiento
nombres normalizados
clave_matching
clave_hash_privada
información clínica reidentificable
```

Para disponibilización pública se incluyen únicamente:

```text
notebooks sin datos reales
scripts
funciones utilitarias
diccionarios anonimizados
logs sintéticos o anonimizados
estructura de carpetas
archivos de ejemplo sintéticos
documentación metodológica
README.md
```

## Reproducibilidad

La reproducibilidad se garantiza mediante:

- notebooks ejecutables en orden secuencial;
- separación entre datos originales, artefactos privados y salidas analíticas;
- identificadores internos `PACIENTE_ID` y `REGISTRO_ID`;
- tabla privada de trazabilidad `crosswalk_paciente_ecg.xlsx`;
- claves operacionales de matching para integración ECG;
- logs de transformación;
- diccionarios de variables;
- semillas fijas en clustering y modelado;
- exportación de métricas consolidadas;
- documentación de entradas y salidas;
- control de completitud;
- trazabilidad de escenarios experimentales;
- separación explícita entre modelado, evaluación incremental e interpretabilidad.

Cada notebook debe ejecutarse siguiendo el orden definido en la tabla inicial.

## Dependencias principales

Las dependencias pueden variar según el entorno local, pero el pipeline utiliza principalmente:

```text
pandas
numpy
openpyxl
xlsxwriter
scikit-learn
pypdfium2
matplotlib
xgboost
lightgbm
shap
joblib
```

Cada notebook contiene celdas de instalación o validación de dependencias requeridas para facilitar ejecución reproducible.

## Advertencia sobre uso clínico

Este repositorio tiene finalidad académica y experimental.

Los notebooks, pipelines, datasets derivados y resultados asociados no constituyen una herramienta clínica validada, no deben utilizarse para diagnóstico, tratamiento, estratificación clínica real ni toma de decisiones médicas.

Cualquier uso aplicado en contextos sanitarios reales requeriría validación externa, revisión clínica especializada, evaluación prospectiva, análisis regulatorio y control formal de seguridad, sesgo, privacidad e interoperabilidad.
