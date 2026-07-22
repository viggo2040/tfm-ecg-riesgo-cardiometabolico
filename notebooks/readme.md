# Notebooks del TFM

## Evaluación del valor incremental de parámetros ECG en riesgo cardiometabólico

Esta carpeta contiene los notebooks ejecutables que respaldan el desarrollo técnico del Trabajo Fin de Máster. El repositorio documenta un pipeline experimental de Inteligencia Artificial clínica multimodal orientado a:

- seudonimizar y normalizar una cohorte clínica retrospectiva;
- procesar antecedentes médicos mediante PLN/NLP;
- caracterizar la completitud estructural mediante pseudo-baterías;
- extraer parámetros electrocardiográficos desde reportes ECG en PDF;
- integrar información clínica, textual y electrocardiográfica;
- construir un endpoint operacional de riesgo cardiometabólico;
- entrenar y evaluar modelos predictivos en cuatro escenarios experimentales;
- cuantificar el aporte incremental de ECG;
- analizar estabilidad por subconjuntos estructurales;
- interpretar los modelos mediante SHAP.

> **Alcance:** este repositorio tiene finalidad académica y experimental. No constituye una herramienta clínica validada ni debe emplearse para diagnóstico, tratamiento o toma de decisiones médicas.

---

## 1. Estado verificado del pipeline

Los ocho notebooks fueron revisados en su versión actual.

| Notebook | Estado de ejecución almacenado | Errores almacenados | Observación principal |
|---|---:|---:|---|
| `01_proceso_pln1_anonimizacion_normalizacion.ipynb` | Parcialmente ejecutado | 0 | Validaciones finales ejecutadas; cobertura de `clave_matching` de 99,84 % |
| `02_proceso_pln2_subsets_baterias.ipynb` | Parcialmente ejecutado | 0 | Segmentación en cuatro pseudo-baterías validada |
| `03_extraccion_ecg_pdf.ipynb` | Parcialmente ejecutado | 0 | Mantiene rutas locales absolutas que deben parametrizarse para reproducción externa |
| `04_integracion_ecg.ipynb` | Parcialmente ejecutado | 0 | Integración determinística validada; cobertura ECG integrada de 1,27 % |
| `05_construccion_endpoint.ipynb` | Parcialmente ejecutado | 0 | Endpoint y cuatro escenarios generados correctamente |
| `06_modelado_predictivo.ipynb` | Ejecutado | 0 | Genera métricas globales, métricas por batería, predicciones y modelos |
| `07_evaluacion_incremental_ecg.ipynb` | Ejecutado | 0 | Evaluación global y por `SUBSET_BATERIA` completada |
| `08_interpretabilidad_shap.ipynb` | Ejecutado | 0 | SHAP completado mediante fallback agnóstico cuando `TreeExplainer` no fue compatible |

La ausencia de errores almacenados indica que las ejecuciones registradas finalizaron correctamente. Los notebooks 01–05 contienen algunas celdas sin contador de ejecución, por lo que una reproducción desde cero debe realizarse mediante **Restart Kernel and Run All** en el orden indicado en este documento.

La versión actual del pipeline y del TFM utiliza una división holdout estratificada 80/20 con semilla 42. No se implementó validación cruzada. El ranking de modelos es descriptivo y se construye con las métricas del conjunto de prueba.

---

## 2. Orden obligatorio de ejecución

| Orden | Notebook | Entrada principal | Salida principal |
|---:|---|---|---|
| 1 | `01_proceso_pln1_anonimizacion_normalizacion.ipynb` | `Base de Datos Original.xlsx` | `Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx` y artefactos privados de trazabilidad |
| 2 | `02_proceso_pln2_subsets_baterias.ipynb` | `Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx` | `Base_Ordenada_Subsets_TFM.xlsx` |
| 3 | `03_extraccion_ecg_pdf.ipynb` | Carpeta de reportes ECG PDF | `ecg_dataset.xlsx`, `ecg_dataset.csv` y `ecg_resumen.txt` |
| 4 | `04_integracion_ecg.ipynb` | Base segmentada, crosswalk privado y dataset ECG | `Dataset_Multimodal_Integrado_TFM.xlsx` |
| 5 | `05_construccion_endpoint.ipynb` | `Dataset_Multimodal_Integrado_TFM.xlsx` | `Dataset_Endpoint_TFM.xlsx` y datasets E1–E4 |
| 6 | `06_modelado_predictivo.ipynb` | Datasets E1–E4 | Métricas, predicciones, variables y modelos entrenados |
| 7 | `07_evaluacion_incremental_ecg.ipynb` | Métricas globales y por batería | Comparaciones incrementales, ranking y figuras |
| 8 | `08_interpretabilidad_shap.ipynb` | Modelos entrenados, datasets y metadatos | Resultados SHAP, gráficos y reporte técnico |

---

## 3. Arquitectura general

```text
Base de Datos Original.xlsx
        ↓
01_proceso_pln1_anonimizacion_normalizacion.ipynb
        ↓
Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx
crosswalk_paciente_ecg.xlsx
Auditoria_Privada_Trazabilidad_TFM.xlsx
        ↓
02_proceso_pln2_subsets_baterias.ipynb
        ↓
Base_Ordenada_Subsets_TFM.xlsx
        ↓
03_extraccion_ecg_pdf.ipynb
        ↓
ecg_dataset.xlsx
ecg_dataset.csv
ecg_resumen.txt
        ↓
04_integracion_ecg.ipynb
        ↓
Dataset_Multimodal_Integrado_TFM.xlsx
Auditoria_Integracion_ECG_TFM.xlsx
Reporte_Integracion_ECG_TFM.txt
        ↓
05_construccion_endpoint.ipynb
        ↓
Dataset_Endpoint_TFM.xlsx
Dataset_E1_Clinico_TFM.xlsx
Dataset_E2_Clinico_NLP_TFM.xlsx
Dataset_E3_Clinico_ECG_TFM.xlsx
Dataset_E4_Clinico_NLP_ECG_TFM.xlsx
        ↓
06_modelado_predictivo.ipynb
        ↓
Metricas_Modelado_TFM.xlsx
Metricas_Modelado_Subsets_TFM.xlsx
Predicciones_Modelos_TFM.xlsx
Variables_Modelado_TFM.xlsx
Reporte_Modelado_Predictivo_TFM.txt
modelos_entrenados/
        ↓
07_evaluacion_incremental_ecg.ipynb
        ↓
Comparacion_Incremental_ECG_TFM.xlsx
Ranking_Modelos_Escenarios_TFM.xlsx
Resumen_Evaluacion_Incremental_TFM.txt
figuras_evaluacion_incremental/
        ↓
08_interpretabilidad_shap.ipynb
        ↓
Resultados_SHAP_TFM.xlsx
Reporte_Interpretabilidad_SHAP_TFM.txt
Graficos_SHAP/
```

---

## 4. Identificadores y trazabilidad

### 4.1. Identificadores internos

| Columna | Función | Uso como predictor |
|---|---|---:|
| `PACIENTE_ID` | Identificador interno seudonimizado del paciente | No |
| `REGISTRO_ID` | Identificador único del registro analítico | No |
| `clave_matching` | Clave operacional para integración clínica–ECG | No |

`PACIENTE_ID` y `REGISTRO_ID` se preservan para trazabilidad. `clave_matching` pertenece a los artefactos privados y no debe exponerse en repositorios públicos.

### 4.2. Trazabilidad estructural

| Columna | Descripción | Uso como predictor |
|---|---|---:|
| `SUBSET_EXAMENES` | Denominación original del subconjunto estructural | No |
| `SUBSET_BATERIA` | Nombre estándar transversal de pseudo-batería | No |
| `BATERIA_CLUSTER` | Identificador numérico del cluster estructural | No |

La columna estándar para análisis posteriores es `SUBSET_BATERIA`. Las pseudo-baterías representan patrones de disponibilidad de información; no representan fenotipos clínicos ni grupos diagnósticos.

---

## 5. Notebook 01: seudonimización, normalización clínica y PLN/NLP

**Archivo:** `01_proceso_pln1_anonimizacion_normalizacion.ipynb`

### Entrada

```text
Base de Datos Original.xlsx
```

### Salidas

```text
Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx
crosswalk_paciente_ecg.xlsx
Auditoria_Privada_Trazabilidad_TFM.xlsx
Diccionario_Normalizacion_Antecedentes.csv
Log_Transformacion_Cohorte_TFM.txt
```

### Funciones principales

1. Limpieza y estandarización de nombres de columnas.
2. Generación de `PACIENTE_ID` y `REGISTRO_ID`.
3. Construcción de `nombre_paciente_norm`, `fecha_atencion_norm` y `clave_matching`.
4. Generación del crosswalk privado para integración ECG.
5. Eliminación de identificadores directos desde la base analítica.
6. Normalización de variables clínicas numéricas.
7. Codificación binaria de tabaquismo y diabetes.
8. Procesamiento de antecedentes médicos mediante reglas PLN/NLP.
9. Detección básica de negaciones.
10. Generación de variables `ANT_*` e indicadores `FLAG_*`.
11. Exportación de la cohorte seudonimizada, diccionario, auditoría y log.

### Variables NLP generadas

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

### Indicadores cardiometabólicos

```text
FLAG_PA_SISTOLICA_ALTA
FLAG_PA_DIASTOLICA_ALTA
FLAG_GLICEMIA_ALTA
FLAG_LDL_ALTO
FLAG_TRIGLICERIDOS_ALTOS
FLAG_OBESIDAD_IMC
FLAG_HDL_BAJO
```

### Resultado verificado

```text
Registros: 3.779
Registros con clave_matching: 3.773
Cobertura clave_matching: 99,84 %
Duplicados detectados en clave_matching durante la validación final: 0
```

---

## 6. Notebook 02: completitud y pseudo-baterías

**Archivo:** `02_proceso_pln2_subsets_baterias.ipynb`

### Entrada

```text
Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx
```

### Salidas

```text
Base_Ordenada_Subsets_TFM.xlsx
Reporte_Subsets_Baterias_TFM.txt
```

### Hojas principales de la salida Excel

```text
BASE_COMPLETA
BATERIA_A
BATERIA_B
BATERIA_C
BATERIA_D
RESUMEN_BATERIAS
METADATA
COLUMNAS_USADAS
```

### Proceso

1. Selección de columnas para completitud.
2. Cálculo de `TOTAL_RESULTADOS`.
3. Cálculo de `PORCENTAJE_COMPLETITUD`.
4. Construcción de matriz binaria de disponibilidad.
5. Clustering estructural mediante K-Means con semilla fija.
6. Generación de cuatro pseudo-baterías.
7. Preservación de identificadores y columnas estructurales.

### Distribución verificada

| Pseudo-batería | Registros | Completitud promedio |
|---|---:|---:|
| `BATERIA_A` | 936 | 98,91 % |
| `BATERIA_B` | 1.192 | 83,88 % |
| `BATERIA_C` | 837 | 80,50 % |
| `BATERIA_D` | 814 | 61,24 % |
| **Total** | **3.779** | — |

---

## 7. Notebook 03: extracción de parámetros ECG desde PDF

**Archivo:** `03_extraccion_ecg_pdf.ipynb`

### Entrada

```text
Carpeta de reportes ECG PDF
```

### Salidas

```text
ecg_dataset.xlsx
ecg_dataset.csv
ecg_resumen.txt
```

### Hojas del archivo `ecg_dataset.xlsx`

```text
ECG_DATASET
RESUMEN
DUPLICADOS
```

### Variables ECG principales

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

La ejecución documentada conservó simultáneamente `ECG_AXIS` y `QRS_AXIS`, aunque `QRS_AXIS` corresponde a una copia del eje representado por `ECG_AXIS`. Esta duplicación se mantiene para conservar la trazabilidad de los resultados aprobados y se declara como una limitación de la configuración experimental actual. Deberá eliminarse en futuras ejecuciones depuradas.

### Variables auxiliares relevantes

```text
ECG_ID
archivo_origen
ruta_relativa
fecha_examen
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

### Dependencia de extracción PDF

El notebook utiliza:

```text
pypdfium2
```

### Configuración local que debe ajustarse

La versión revisada contiene rutas absolutas de Windows:

```python
ROOT = Path(r"C:/Users/viggo/Project/ELECTROCARDIOGRAMA")
OUT_DIR = Path(r"C:/Users/viggo/Project")
```

Para ejecutar el notebook en otro entorno, ambas rutas deben reemplazarse por rutas válidas o convertirse en parámetros relativos al repositorio.

---

## 8. Notebook 04: integración clínica–ECG

**Archivo:** `04_integracion_ecg.ipynb`

### Entradas

```text
Base_Ordenada_Subsets_TFM.xlsx
crosswalk_paciente_ecg.xlsx
ecg_dataset.xlsx
```

### Salidas

```text
Dataset_Multimodal_Integrado_TFM.xlsx
Auditoria_Integracion_ECG_TFM.xlsx
Reporte_Integracion_ECG_TFM.txt
```

### Esquema de integración

```text
Base clínica
PACIENTE_ID + REGISTRO_ID
        ↓
Crosswalk privado
PACIENTE_ID + REGISTRO_ID + clave_matching
        ↓
Dataset ECG
clave_matching
```

### Resultado verificado

| Indicador | Valor |
|---|---:|
| Registros clínicos | 3.779 |
| Registros con crosswalk | 3.773 |
| Cobertura de crosswalk | 99,84 % |
| Registros ECG extraídos | 2.679 |
| Claves ECG únicas disponibles para integración principal | 2.623 |
| ECG enviados a revisión por duplicidad | 108 |
| Registros con ECG integrado | 48 |
| Cobertura ECG integrada | 1,27 % |

### Cobertura ECG por pseudo-batería

| Pseudo-batería | Registros | Con ECG | Cobertura |
|---|---:|---:|---:|
| `BATERIA_A` | 936 | 16 | 1,71 % |
| `BATERIA_B` | 1.192 | 17 | 1,43 % |
| `BATERIA_C` | 837 | 15 | 1,79 % |
| `BATERIA_D` | 814 | 0 | 0,00 % |

La baja cobertura ECG integrada es una limitación metodológica del estudio y condiciona la interpretación del valor incremental observado.

---

## 9. Notebook 05: endpoint y escenarios experimentales

**Archivo:** `05_construccion_endpoint.ipynb`

### Entrada

```text
Dataset_Multimodal_Integrado_TFM.xlsx
```

### Salidas

```text
Dataset_Endpoint_TFM.xlsx
Dataset_E1_Clinico_TFM.xlsx
Dataset_E2_Clinico_NLP_TFM.xlsx
Dataset_E3_Clinico_ECG_TFM.xlsx
Dataset_E4_Clinico_NLP_ECG_TFM.xlsx
Reporte_Endpoint_TFM.txt
```

### Endpoint operacional

```text
RIESGO_CARDIOMETABOLICO = 1 si INDICE_RIESGO_CARDIOMETABOLICO >= 3
RIESGO_CARDIOMETABOLICO = 0 si INDICE_RIESGO_CARDIOMETABOLICO < 3
```

### Distribución verificada

| Clase | Registros | Porcentaje |
|---:|---:|---:|
| 0 | 3.339 | 88,36 % |
| 1 | 440 | 11,64 % |
| **Total** | **3.779** | **100,00 %** |

### Factores excluidos de los predictores

Los factores utilizados directamente para construir el endpoint se excluyen del entrenamiento para reducir fuga directa de información:

```text
FLAG_OBESIDAD_IMC
FLAG_PA_SISTOLICA_ALTA
FLAG_PA_DIASTOLICA_ALTA
FLAG_GLICEMIA_ALTA
FLAG_LDL_ALTO
FLAG_TRIGLICERIDOS_ALTOS
FLAG_HDL_BAJO
Diabetes_bin
ANT_HTA
ANT_DIABETES
ANT_DISLIPIDEMIA
ANT_OBESIDAD
```

### Escenarios

| Escenario | Modalidades | Registros | Features de entrenamiento |
|---|---|---:|---:|
| `E1_CLINICO` | Clínica | 3.779 | 22 |
| `E2_CLINICO_NLP` | Clínica + NLP | 3.779 | 34 |
| `E3_CLINICO_ECG` | Clínica + ECG | 3.779 | 33 |
| `E4_CLINICO_NLP_ECG` | Clínica + NLP + ECG | 3.779 | 45 |

Las cantidades 22, 34, 33 y 45 corresponden a la ejecución documentada e incluyen cuatro variables de control adicionales a la composición modal estricta. Esta condición se detalla en la sección del notebook 06.

---

## 10. Notebook 06: modelado predictivo

**Archivo:** `06_modelado_predictivo.ipynb`

### Entradas

```text
Dataset_E1_Clinico_TFM.xlsx
Dataset_E2_Clinico_NLP_TFM.xlsx
Dataset_E3_Clinico_ECG_TFM.xlsx
Dataset_E4_Clinico_NLP_ECG_TFM.xlsx
```

### Salidas

```text
Metricas_Modelado_TFM.xlsx
Metricas_Modelado_Subsets_TFM.xlsx
Predicciones_Modelos_TFM.xlsx
Variables_Modelado_TFM.xlsx
Reporte_Modelado_Predictivo_TFM.txt
modelos_entrenados/
```

### Configuración verificada

```text
RANDOM_STATE = 42
TEST_SIZE = 0.20
TRAIN_SIZE = 3.023
TEST_SIZE_REGISTROS = 756
POSITIVOS_TEST = 88
```

La evaluación utiliza una única división holdout estratificada 80/20 con semilla 42. Los modelos y las transformaciones de preprocesamiento se ajustan exclusivamente sobre el conjunto de entrenamiento. Las configuraciones se definen previamente y el ranking descriptivo se construye posteriormente con AUPRC, ROC-AUC y F1 obtenidos en el conjunto de prueba. No se implementa validación cruzada ni búsqueda exhaustiva de hiperparámetros. El uso del test para ordenar los modelos se reconoce como una limitación metodológica.

### Modelos

```text
Logistic Regression
Random Forest
XGBoost
LightGBM
```

### Métricas

```text
Accuracy
Precision
Recall
F1
ROC_AUC
AUPRC
TN
FP
FN
TP
Brier_Score
Calibration_Intercept
Calibration_Slope
```

La AUPRC se utiliza como criterio principal del ranking descriptivo, seguida por ROC-AUC y F1. El reporte textual del notebook aplica este mismo orden. Para los modelos evaluados se registran además Brier Score, intercepto y pendiente de calibración. La celda final de consulta de calibración reutiliza el artefacto generado mediante `METRICS_PATH`, sin depender de un archivo renombrado externamente.

### Mejores resultados por escenario

| Escenario | Mejor modelo | F1 | ROC-AUC | AUPRC |
|---|---|---:|---:|---:|
| `E1_CLINICO` | XGBoost | 0,9302 | 0,9967 | 0,9804 |
| `E2_CLINICO_NLP` | XGBoost | 0,9364 | 0,9967 | 0,9800 |
| `E3_CLINICO_ECG` | XGBoost | 0,9474 | 0,9968 | 0,9807 |
| `E4_CLINICO_NLP_ECG` | XGBoost | 0,9474 | 0,9969 | 0,9817 |

El notebook genera 16 combinaciones escenario–modelo y 64 filas de métricas por pseudo-batería.

### Variables de control presentes en la ejecución documentada

La ejecución que respalda las métricas actuales mantuvo entre los predictores cuatro columnas de control:

```text
ESCENARIO
flag_ecg_disponible
N_FACTORES_ENDPOINT_OBSERVADOS
N_FACTORES_ENDPOINT_FALTANTES
```

Estas columnas no corresponden estrictamente a las modalidades clínica, NLP o ECG. En particular, los conteos de factores observados y faltantes pueden reflejar indirectamente la completitud utilizada durante la construcción del endpoint. Los resultados publicados corresponden a esta ejecución y deben interpretarse considerando esta limitación; no representan una ejecución completamente depurada.

---

## 11. Notebook 07: evaluación incremental ECG

**Archivo:** `07_evaluacion_incremental_ecg.ipynb`

### Entradas

```text
Metricas_Modelado_TFM.xlsx
Metricas_Modelado_Subsets_TFM.xlsx
Predicciones_Modelos_TFM.xlsx
Variables_Modelado_TFM.xlsx
```

### Salidas

```text
Comparacion_Incremental_ECG_TFM.xlsx
Ranking_Modelos_Escenarios_TFM.xlsx
Resumen_Evaluacion_Incremental_TFM.txt
figuras_evaluacion_incremental/metricas_por_escenario_modelo.png
figuras_evaluacion_incremental/delta_incremental_ecg.png
figuras_evaluacion_incremental/ranking_auprc_por_escenario.png
```

### Comparaciones principales

```text
E1_CLINICO → E3_CLINICO_ECG
E2_CLINICO_NLP → E4_CLINICO_NLP_ECG
```

### Comparaciones complementarias

```text
E1_CLINICO → E2_CLINICO_NLP
E1_CLINICO → E4_CLINICO_NLP_ECG
E3_CLINICO_ECG → E4_CLINICO_NLP_ECG
```

### Hojas de `Comparacion_Incremental_ECG_TFM.xlsx`

```text
COMPARACION_INCREMENTAL
APORTE_ECG
COMPARACION_SUBSETS
RESUMEN_SUBSETS
```

### Hojas de `Ranking_Modelos_Escenarios_TFM.xlsx`

```text
RANKING_COMPLETO
MEJORES_ESCENARIO
MEJOR_GLOBAL
```

### Resultado global principal verificado

La configuración con mejor desempeño global es:

```text
Escenario: E4_CLINICO_NLP_ECG
Modelo: XGBoost
F1: 0,9474
ROC_AUC: 0,9969
AUPRC: 0,9817
```

### Bootstrap pareado e incertidumbre

El notebook aplica 2.000 iteraciones bootstrap pareadas sobre las predicciones del conjunto de prueba para las comparaciones principales:

| Comparación | ΔAUPRC | IC 95 % ΔAUPRC | ΔROC-AUC | ΔF1 |
|---|---:|---:|---:|---:|
| `E1_CLINICO → E3_CLINICO_ECG` | 0,000290 | [−0,002800; 0,003405] | 0,000034 | 0,017136 |
| `E2_CLINICO_NLP → E4_CLINICO_NLP_ECG` | 0,001710 | [−0,000723; 0,004922] | 0,000238 | 0,010952 |

Ambos intervalos de AUPRC incluyen cero. La incorporación de ECG produce una mejora puntual marginal y dependiente del modelo, pero no una mejora concluyente en la métrica principal. XGBoost presenta el patrón más favorable, mientras que los restantes algoritmos muestran efectos nulos, reducidos o mixtos.

---

## 12. Notebook 08: interpretabilidad mediante SHAP

**Archivo:** `08_interpretabilidad_shap.ipynb`

### Entradas

```text
modelos_entrenados/
Dataset_E3_Clinico_ECG_TFM.xlsx
Dataset_E4_Clinico_NLP_ECG_TFM.xlsx
Metricas_Modelado_TFM.xlsx
Ranking_Modelos_Escenarios_TFM.xlsx
Predicciones_Modelos_TFM.xlsx
Variables_Modelado_TFM.xlsx
```

### Salidas

```text
Resultados_SHAP_TFM.xlsx
Reporte_Interpretabilidad_SHAP_TFM.txt
Graficos_SHAP/shap_summary_beeswarm.png
Graficos_SHAP/shap_summary_bar.png
Graficos_SHAP/shap_importancia_modalidad.png
Graficos_SHAP/shap_top_variables.png
Graficos_SHAP/shap_ecg_variables.png
Graficos_SHAP/shap_waterfall_caso_alto_riesgo.png
Graficos_SHAP/shap_waterfall_caso_bajo_riesgo.png
Graficos_SHAP/shap_force_plot_sample.html
```

### Configuración verificada

```text
Escenarios interpretados: E4_CLINICO_NLP_ECG y E3_CLINICO_ECG
Modelo interpretado: XGBoost
MAX_SHAP_SAMPLE = 500
MAX_SHAP_SAMPLE_FALLBACK = 120
Fuente de la muestra: dataset completo
Semilla de muestreo: 42
```

XGBoost se interpreta en E3 y E4 por haber ocupado el primer lugar del ranking descriptivo calculado sobre el conjunto de prueba. Para cada escenario se seleccionan 500 observaciones desde el dataset completo, no exclusivamente desde el test. En consecuencia, el análisis describe el comportamiento global del modelo y no constituye una evaluación independiente de interpretabilidad sobre datos no utilizados durante el entrenamiento.

### Compatibilidad del explicador

En ambos escenarios, `TreeExplainer` no fue compatible con el modelo XGBoost serializado y produjo el mensaje:

```text
could not convert string to float: '[1.16440624E-1]'
```

El notebook no finalizó con error. Aplicó correctamente un fallback agnóstico basado en `predict_proba` mediante `PermutationExplainer`.

### Resultado verificado

| Escenario | Variables totales | Variables ECG | Importancia ECG agregada | Mejor variable ECG | Ranking |
|---|---:|---:|---:|---|---:|
| `E4_CLINICO_NLP_ECG` | 45 | 11 | 0,00 % | `SV1` | 22 |
| `E3_CLINICO_ECG` | 33 | 11 | 0,00 % | `SV5` | 19 |

La importancia agregada por modalidad fue:

| Escenario | Clínica | NLP | ECG |
|---|---:|---:|---:|
| `E3_CLINICO_ECG` | 100,00 % | No aplica | 0,00 % |
| `E4_CLINICO_NLP_ECG` | 99,78 % | 0,22 % | 0,00 % |

Los valores SHAP explican el comportamiento del modelo bajo esta configuración experimental. No constituyen evidencia causal ni validación clínica.

---

## 13. Dependencias

Dependencias principales verificadas en los notebooks:

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

Instalación recomendada:

```bash
pip install pandas numpy openpyxl xlsxwriter scikit-learn pypdfium2 matplotlib xgboost lightgbm shap joblib
```

El repositorio incluye el archivo `requirements.txt` con las dependencias principales utilizadas por los notebooks. Para una reproducción exacta del entorno, se recomienda complementar este archivo con versiones concretas de cada paquete.

---

## 14. Estructura recomendada del repositorio

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

La estructura anterior es una organización recomendada. La versión actual de los notebooks utiliza principalmente el directorio de trabajo como ubicación de entradas y salidas.

---

## 15. Privacidad y publicación

### No publicar

```text
Base de Datos Original.xlsx
crosswalk_paciente_ecg.xlsx
Auditoria_Privada_Trazabilidad_TFM.xlsx
Auditoria_Integracion_ECG_TFM.xlsx
reportes ECG PDF originales
nombres de pacientes
nombres normalizados
RUT u otros identificadores administrativos
fechas exactas sensibles
clave_matching
clave_hash_privada
rutas que contengan identificadores
información clínica potencialmente reidentificable
```

Los datasets internos se consideran seudonimizados mientras exista el archivo privado de correspondencia. Los modelos y artefactos derivados solo deben publicarse después de una revisión específica de privacidad y riesgo de reidentificación. La denominación «anonimizado» debe reservarse para versiones públicas sin identificadores directos, claves de vinculación ni mecanismos razonables de reidentificación.

### Publicables previa revisión

```text
notebooks sin datos reales ni rutas privadas
README metodológico
diccionarios sin identificadores personales
métricas agregadas
figuras de resultados
reportes técnicos sin identificadores
scripts y funciones utilitarias
datos sintéticos de ejemplo
```

---

## 16. Reproducibilidad

La reproducibilidad se apoya en:

1. ejecución secuencial de ocho notebooks;
2. entradas y salidas explícitas por etapa;
3. identificadores internos `PACIENTE_ID` y `REGISTRO_ID`;
4. crosswalk privado para integración ECG;
5. conservación de `SUBSET_BATERIA` para evaluación estructural;
6. exclusión de los identificadores, del índice y de los factores binarios utilizados directamente para construir el endpoint; las variables clínicas continuas de origen permanecen como predictores y generan una dependencia residual declarada;
7. semilla fija `RANDOM_STATE = 42` en etapas de modelado;
8. división holdout estratificada 80/20 con `RANDOM_STATE = 42`, compuesta por 3.023 registros de entrenamiento y 756 de prueba;
9. exportación de métricas globales, calibración y resultados por pseudo-batería;
10. persistencia de modelos entrenados;
11. reportes técnicos y figuras generadas automáticamente;
12. análisis SHAP reproducible con fallback documentado.

### Limitaciones de reproducción externa

- Los datos originales y artefactos privados no pueden publicarse.
- El notebook 03 requiere parametrización de rutas locales.
- La reproducción exacta depende de las versiones de Python y librerías.
- El ranking descriptivo utiliza métricas del conjunto de prueba; no existe una selección independiente mediante validación cruzada.
- La ejecución documentada del notebook 06 incluye cuatro variables de control que deben excluirse en una futura ejecución completamente depurada.
- El fallback SHAP basado en permutaciones tiene mayor coste computacional que `TreeExplainer`.
- SHAP se calculó sobre una muestra del dataset completo y no exclusivamente sobre el test.
- La integración clínica–ECG depende de un crosswalk privado no publicable.

---

## 17. Resultados metodológicos principales

- Cohorte analítica final: **3.779 registros**.
- Clase positiva del endpoint: **440 registros, 11,64 %**.
- ECG extraídos desde PDF: **2.679 registros**.
- ECG integrados en la cohorte final: **48 registros, 1,27 %**.
- División experimental: **3.023 registros de entrenamiento y 756 de prueba**, con 88 positivos en test.
- Mejor configuración puntual: **XGBoost en E4 Clínico + NLP + ECG**, según el ranking descriptivo del conjunto de prueba.
- Mejor F1 global: **0,9474**.
- Mejor ROC-AUC global: **0,9969**.
- Mejor AUPRC global: **0,9817**.
- E1→E3: **ΔAUPRC = 0,000290**, IC 95 % **[−0,002800; 0,003405]**.
- E2→E4: **ΔAUPRC = 0,001710**, IC 95 % **[−0,000723; 0,004922]**.
- Contribución SHAP agregada ECG: **0,00 % en E3 y E4**.

La evidencia muestra una señal incremental ECG puntual, marginal y dependiente del modelo. Los intervalos bootstrap de AUPRC incluyen cero, por lo que el aporte ECG no se considera concluyente bajo la cobertura disponible.

---

## 18. Relación con el TFM

| Capítulo | Evidencia técnica principal |
|---|---|
| Capítulo 4 | Notebooks 01–05: construcción de la cohorte multimodal, endpoint y escenarios experimentales |
| Capítulo 5 | Notebooks 06–08: modelado, evaluación incremental e interpretabilidad |
| Capítulo 6 | Notebooks 01–08, README y artefactos de reproducibilidad |
| Capítulo 7 | Métricas, comparación incremental y resultados SHAP |

---

## 19. Advertencia sobre uso clínico

Los notebooks, modelos, datasets derivados y resultados asociados tienen finalidad exclusivamente académica y experimental. No están validados para uso asistencial y no deben utilizarse para diagnóstico, tratamiento, estratificación clínica real ni toma de decisiones médicas.

Cualquier aplicación sanitaria requeriría validación externa, evaluación prospectiva, revisión clínica especializada, análisis de sesgo, controles de privacidad, evaluación regulatoria y mecanismos formales de seguridad e interoperabilidad.
