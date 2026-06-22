# Notebooks del TFM

Esta carpeta contiene los notebooks desarrollados para reproducir los procesos técnicos asociados al Trabajo Fin de Máster:

**Evaluación del valor incremental de parámetros ECG en riesgo cardiometabólico**

Los notebooks documentan la construcción de la cohorte experimental, el procesamiento clínico, la generación de variables mediante PLN/NLP, la segmentación estructural en pseudo-baterías clínicas, la extracción estructurada de parámetros ECG desde reportes PDF, la integración multimodal, la construcción del endpoint, el modelado predictivo y la interpretabilidad.

## Objetivo de la carpeta

El objetivo de esta carpeta es centralizar los cuadernos ejecutables que respaldan la trazabilidad técnica del TFM.

Los notebooks permiten reproducir, documentar y auditar las principales transformaciones realizadas sobre los datos, desde la base clínica original hasta los datasets preparados para modelado predictivo y evaluación incremental del aporte de los parámetros ECG.

## Orden recomendado de ejecución

| Orden | Notebook                                            | Propósito                                                   | Entrada principal                                    | Salida principal                                     |
| ----: | --------------------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- |
|     1 | `01_proceso_pln1_anonimizacion_normalizacion.ipynb` | Anonimización, normalización clínica y PLN/NLP              | `Base de Datos Original.xlsx`                        | `Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx` |
|     2 | `02_proceso_pln2_subsets_baterias.ipynb`            | Cálculo de completitud y segmentación estructural           | `Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx` | `Base_Ordenada_Subsets_TFM.xlsx`                     |
|     3 | `03_extraccion_ecg_pdf.ipynb`                       | Extracción estructurada de parámetros ECG desde PDF         | Carpeta de reportes ECG PDF                          | `ecg_dataset.xlsx`                                   |
|     4 | `04_integracion_ecg.ipynb`                          | Integración de parámetros ECG con la cohorte clínica        | `Base_Ordenada_Subsets_TFM.xlsx` + `ecg_dataset.xlsx`| Dataset multimodal integrado                         |
|     5 | `05_construccion_endpoint.ipynb`                    | Construcción del endpoint experimental                      | Dataset multimodal integrado                         | `RIESGO_CARDIOMETABOLICO`                            |
|     6 | `06_modelado_predictivo.ipynb`                      | Entrenamiento de modelos supervisados                       | Dataset final de modelado                            | Métricas por modelo y escenario                      |
|     7 | `07_evaluacion_incremental_ecg.ipynb`               | Comparación incremental entre escenarios clínicos y ECG     | Métricas consolidadas                                | Tablas de diferencias y análisis comparativo         |
|     8 | `08_interpretabilidad_shap.ipynb`                   | Interpretabilidad de modelos mediante SHAP                  | Modelos entrenados                                   | Gráficos y tablas SHAP                               |

## Proceso 1: Anonimización, normalización clínica y PLN/NLP

El primer proceso toma como entrada la base clínica original:

```text
Base de Datos Original.xlsx
```

y reproduce el pipeline implementado en:

```text
pipeline_cohorte_tfm.py
01_proceso_pln1_anonimizacion_normalizacion.ipynb
```

La salida principal es:

```text
Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx
```

### Necesidad metodológica

La base clínica original contiene información sensible y variables en formatos heterogéneos. Para su utilización dentro del TFM, fue necesario construir una versión anonimizada, estructurada y analíticamente consistente.

Este proceso permite:

* proteger la privacidad de los pacientes mediante anonimización;
* eliminar identificadores directos;
* crear un identificador interno no derivado de datos personales;
* conservar trazabilidad mediante `PACIENTE_ID`;
* normalizar variables clínicas numéricas;
* estructurar antecedentes médicos originalmente registrados como texto libre;
* generar variables binarias clínicas derivadas;
* construir indicadores cardiometabólicos reproducibles;
* documentar el proceso mediante diccionarios, conteos y logs de transformación.

### Transformaciones principales

El pipeline realiza las siguientes operaciones:

1. Lectura de la base clínica original.
2. Limpieza y estandarización de nombres de columnas.
3. Eliminación de identificadores directos.
4. Generación de `PACIENTE_ID` secuencial anónimo.
5. Generalización temporal de fechas de atención.
6. Normalización de variables clínicas numéricas.
7. Codificación binaria de variables como tabaquismo y diabetes.
8. Limpieza textual de antecedentes médicos.
9. Detección de conceptos clínicos mediante reglas PLN/NLP.
10. Detección básica de negaciones clínicas.
11. Generación de variables `ANT_*`.
12. Generación de flags cardiometabólicos `FLAG_*`.
13. Cálculo de completitud y conteos.
14. Exportación de archivo Excel procesado, diccionario clínico y log.

### Variables generadas mediante PLN/NLP

El procesamiento de antecedentes médicos transforma texto libre en variables binarias como:

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

Estas variables permiten incorporar información clínica previamente no estructurada dentro de los modelos experimentales del TFM.

### Indicadores cardiometabólicos generados

El pipeline también genera variables derivadas orientadas a representar factores de riesgo cardiometabólico:

```text
FLAG_PA_SISTOLICA_ALTA
FLAG_PA_DIASTOLICA_ALTA
FLAG_GLICEMIA_ALTA
FLAG_LDL_ALTO
FLAG_TRIGLICERIDOS_ALTOS
FLAG_OBESIDAD_IMC
FLAG_HDL_BAJO
```

Estas variables son utilizadas posteriormente para construir el endpoint operacional del estudio:

```text
RIESGO_CARDIOMETABOLICO
```

### Salidas del Proceso 1

```text
Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx
Diccionario_Normalizacion_Antecedentes.csv
Log_Transformacion_Cohorte_TFM.txt
```

## Proceso 2: Segmentación estructural y pseudo-baterías clínicas

El segundo proceso toma como entrada la base clínica anonimizada y procesada:

```text
Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx
```

y reproduce la generación del archivo:

```text
Base_Ordenada_Subsets_TFM.xlsx
```

mediante el notebook:

```text
02_proceso_pln2_subsets_baterias.ipynb
```

### Necesidad metodológica

La cohorte procesada presenta heterogeneidad estructural. No todos los pacientes disponen del mismo conjunto de variables clínicas, antecedentes procesados o exámenes complementarios.

En lugar de eliminar todos los registros incompletos, el Proceso 2 representa explícitamente la disponibilidad diferencial de información mediante subconjuntos estructurales o pseudo-baterías clínicas.

Este proceso permite:

* preservar la mayor cantidad posible de registros;
* evitar una reducción excesiva del tamaño muestral;
* representar la heterogeneidad estructural de la cohorte;
* identificar patrones de disponibilidad de información;
* construir subconjuntos comparables para análisis posterior;
* preparar la evaluación de estabilidad de modelos predictivos;
* documentar la estructura real de los datos disponibles.

### Reconstrucción técnica del proceso

El proceso se basa en dos componentes:

1. Cálculo de completitud por paciente.
2. Segmentación estructural mediante clustering sobre matriz de presencia/ausencia.

### Cálculo de completitud

Se calcula una variable:

```text
TOTAL_RESULTADOS
```

correspondiente al conteo de campos clínicos disponibles por paciente dentro de un conjunto definido de variables clínicas, temporales y normalizadas.

A partir de esta variable se calcula:

```text
PORCENTAJE_COMPLETITUD = TOTAL_RESULTADOS / TOTAL_VARIABLES_EVALUADAS * 100
```

Este indicador permite cuantificar el nivel de información disponible para cada individuo.

### Segmentación estructural

Posteriormente se construye una matriz binaria de presencia/ausencia de variables clínicas normalizadas. Esta matriz no representa similitud clínica entre pacientes, sino similitud estructural en la disponibilidad de datos.

Sobre esta matriz se aplica un algoritmo de clustering:

```python
KMeans(n_clusters=4, random_state=42)
```

El resultado permite asignar cada paciente a un subconjunto estructural:

```text
BATERIA_A
BATERIA_B
BATERIA_C
BATERIA_D
```

Cada batería representa una configuración distinta de disponibilidad de información.

### Subconjuntos generados

El archivo final contiene las siguientes hojas:

```text
BASE_COMPLETA
BATERIA_A
BATERIA_B
BATERIA_C
BATERIA_D
```

La hoja `BASE_COMPLETA` conserva la totalidad de la cohorte procesada, incorporando las variables de completitud y pertenencia estructural.

Las hojas `BATERIA_A` a `BATERIA_D` contienen subconjuntos de pacientes agrupados según patrones similares de disponibilidad de información.

### Interpretación metodológica

Los subconjuntos generados no deben interpretarse como grupos clínicos, diagnósticos o demográficos. Representan exclusivamente configuraciones estructurales de disponibilidad de datos.

Esta distinción es relevante para el TFM, porque el objetivo no es descubrir fenotipos clínicos, sino construir una estrategia metodológica que permita evaluar modelos predictivos sobre datos clínicos heterogéneos reales.

## Proceso 3: Extracción estructurada de datos ECG desde PDF

El tercer proceso toma como entrada una carpeta local de reportes ECG en formato PDF:

```text
ELECTROCARDIOGRAMA/
```

y genera un dataset tabular estructurado:

```text
ecg_dataset.xlsx
ecg_dataset.csv
ecg_resumen.txt
```

mediante el notebook:

```text
03_extraccion_ecg_pdf.ipynb
```

### Necesidad metodológica

Los reportes ECG disponibles se encuentran en formato PDF. Para incorporar esta fuente al análisis predictivo, es necesario extraer los parámetros electrocardiográficos relevantes y convertirlos en variables tabulares compatibles con la cohorte clínica procesada.

Este proceso permite:

* leer reportes ECG PDF de forma recursiva;
* extraer texto embebido desde los documentos;
* recuperar parámetros ECG estructurados;
* normalizar valores numéricos con coma decimal;
* generar variables electrocardiográficas tabulares;
* construir una clave operacional de matching paciente-fecha;
* identificar duplicados de ECG del mismo paciente en el mismo día;
* auditar errores, completitud y parámetros faltantes;
* generar una salida reutilizable para integración multimodal.

### Variables ECG extraídas

El notebook extrae, cuando están disponibles, las siguientes variables:

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

También se generan variables auxiliares:

```text
archivo_origen
ruta_relativa
año
mes
fecha_examen
paciente_id
sexo
edad
nombre_paciente
nombre_paciente_norm
fecha
clave_matching
num_ecg_mismo_paciente_fecha
duplicado_mismo_dia
pdf_valido
parametros_extraidos
observaciones_extraccion
```

### Estrategia de matching

El identificador `paciente_id` extraído desde el PDF no debe asumirse como identificador clínico real. La estrategia operacional de cruce se basa en:

```text
nombre_paciente_norm + fecha
```

La variable resultante es:

```text
clave_matching
```

Esta clave se utiliza posteriormente para asociar los parámetros ECG con la cohorte clínica procesada.

### Control de calidad

El proceso calcula:

* número total de PDFs procesados;
* número de PDFs válidos;
* número de errores de extracción;
* completitud por variable;
* ECG con cinco parámetros core completos;
* distribución por año y mes;
* distribución de `parametros_extraidos`;
* duplicados por paciente y fecha;
* observaciones no vacías de extracción.

Los cinco parámetros core evaluados son:

```text
ECG_HR
ECG_PR
ECG_QRS
ECG_QTC
ECG_AXIS
```

## Proceso 4: Integración ECG con cohorte clínica

El cuarto proceso toma como entrada:

```text
Base_Ordenada_Subsets_TFM.xlsx
ecg_dataset.xlsx
```

y genera un dataset multimodal integrado.

Notebook asociado:

```text
04_integracion_ecg.ipynb
```

### Objetivo metodológico

El objetivo es vincular la información clínica estructurada con los parámetros ECG extraídos desde PDF, utilizando una clave de matching operacional basada en nombre normalizado y fecha de examen.

Este proceso permite construir escenarios comparables para evaluar el valor incremental de los parámetros ECG respecto de la información clínica basal.

### Salida esperada

```text
Dataset multimodal integrado
```

La salida de este proceso será utilizada por el notebook de construcción del endpoint experimental.

## Proceso 5: Construcción del endpoint experimental

El quinto proceso construye la variable objetivo operacional del estudio:

```text
RIESGO_CARDIOMETABOLICO
```

Notebook asociado:

```text
05_construccion_endpoint.ipynb
```

### Objetivo metodológico

El endpoint representa una aproximación operacional al riesgo cardiometabólico compuesto, construida a partir de variables clínicas disponibles y flags derivados.

Este endpoint tiene finalidad académica y experimental. No corresponde a un diagnóstico clínico ni a una escala clínica validada externamente.

## Proceso 6: Modelado predictivo

El sexto proceso entrena modelos supervisados sobre los datasets preparados.

Notebook asociado:

```text
06_modelado_predictivo.ipynb
```

### Objetivo metodológico

El objetivo es comparar el desempeño predictivo bajo distintos escenarios de entrada:

```text
Escenario clínico basal
Escenario clínico + ECG
```

Los modelos considerados pueden incluir, según la versión experimental final:

```text
Logistic Regression
Random Forest
XGBoost
LightGBM
```

## Proceso 7: Evaluación incremental de parámetros ECG

El séptimo proceso consolida las métricas obtenidas y evalúa el aporte incremental de los parámetros ECG.

Notebook asociado:

```text
07_evaluacion_incremental_ecg.ipynb
```

### Objetivo metodológico

El objetivo no es demostrar utilidad clínica directa, sino evaluar si la inclusión de variables extraídas desde los ECG PDF mejora el desempeño predictivo experimental respecto de un escenario clínico basal.

La comparación puede considerar métricas como:

```text
ROC-AUC
PR-AUC
F1-score
Recall
Specificity
Balanced Accuracy
```

## Proceso 8: Interpretabilidad mediante SHAP

El octavo proceso incorpora interpretabilidad sobre los modelos entrenados.

Notebook asociado:

```text
08_interpretabilidad_shap.ipynb
```

### Objetivo metodológico

El objetivo es identificar el peso relativo de variables clínicas y ECG dentro de los modelos predictivos, aportando trazabilidad y explicabilidad al análisis experimental.

## Relación entre procesos

Los procesos forman una cadena reproducible de preparación, integración, modelado y evaluación:

```text
Base de Datos Original.xlsx
        ↓
Proceso 1: anonimización + normalización + PLN/NLP + flags clínicos
        ↓
Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx
        ↓
Proceso 2: completitud + clustering estructural + pseudo-baterías
        ↓
Base_Ordenada_Subsets_TFM.xlsx
        ↓
Proceso 3: extracción estructurada desde ECG PDF
        ↓
ecg_dataset.xlsx
        ↓
Proceso 4: integración ECG + cohorte clínica
        ↓
Dataset multimodal integrado
        ↓
Proceso 5: construcción del endpoint operacional
        ↓
RIESGO_CARDIOMETABOLICO
        ↓
Proceso 6: modelado predictivo
        ↓
Métricas por escenario
        ↓
Proceso 7: evaluación incremental ECG
        ↓
Tablas comparativas de aporte incremental
        ↓
Proceso 8: interpretabilidad SHAP
```

## Relación con el TFM

Estos notebooks respaldan principalmente los siguientes capítulos del TFM:

```text
Capítulo 4: Construcción de la cohorte experimental multimodal.
Capítulo 5: Desarrollo experimental y modelado predictivo.
Capítulo 6: Notebooks, código fuente y datos analizados.
Capítulo 7: Conclusiones.
Capítulo 8: Limitaciones y prospectiva.
```

## Consideraciones de privacidad

La base original, las salidas intermedias con información derivada de pacientes y los PDFs ECG originales no deben publicarse en un repositorio público.

No deben publicarse en GitHub:

```text
Base de Datos Original.xlsx
Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx
Base_Ordenada_Subsets_TFM.xlsx
ecg_dataset.xlsx
ecg_dataset.csv
PDFs ECG originales
archivos con nombres de pacientes
rutas relativas con identificadores
RUT
fechas de nacimiento
información clínica reidentificable
```

Para disponibilización pública, se recomienda incluir únicamente:

```text
notebooks
scripts
diccionarios
logs anonimizados
estructura de carpetas
archivos de ejemplo sintéticos
documentación metodológica
```

## Reproducibilidad

La reproducibilidad se garantiza mediante:

* notebooks ejecutables;
* scripts Python modulares;
* semillas fijas en clustering;
* diccionarios de normalización;
* logs de transformación;
* separación entre datos originales, intermedios y derivados;
* documentación de entradas y salidas;
* control de completitud;
* trazabilidad mediante claves operacionales de matching.

Cada notebook debe ejecutarse siguiendo el orden definido en la tabla inicial.

## Advertencia sobre uso clínico

Este repositorio tiene finalidad académica y experimental.

Los notebooks, pipelines y resultados asociados no constituyen una herramienta clínica validada, no deben utilizarse para diagnóstico, tratamiento ni toma de decisiones médicas, y requieren validación externa antes de cualquier uso aplicado en contextos sanitarios reales.
