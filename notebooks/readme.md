# Notebooks del TFM

Esta carpeta contiene los notebooks desarrollados para reproducir los procesos técnicos asociados al Trabajo Fin de Máster:

**Evaluación del valor incremental de parámetros ECG en riesgo cardiometabólico**

Los notebooks documentan la construcción de la cohorte experimental, el procesamiento clínico, la generación de variables mediante PLN/NLP, la segmentación estructural en pseudo-baterías clínicas y las etapas posteriores de integración, modelado e interpretabilidad.

## Objetivo de la carpeta

El objetivo de esta carpeta es centralizar los cuadernos ejecutables que respaldan la trazabilidad técnica del TFM.

Los notebooks permiten reproducir, documentar y auditar las principales transformaciones realizadas sobre los datos, desde la base clínica original hasta los datasets preparados para modelado predictivo.

## Orden recomendado de ejecución

| Orden | Notebook                                            | Propósito                                         | Entrada principal                                    | Salida principal                                     |
| ----: | --------------------------------------------------- | ------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- |
|     1 | `01_proceso_pln1_anonimizacion_normalizacion.ipynb` | Anonimización, normalización clínica y PLN/NLP    | `Base de Datos Original.xlsx`                        | `Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx` |
|     2 | `02_proceso_pln2_subsets_baterias.ipynb`            | Cálculo de completitud y segmentación estructural | `Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx` | `Base_Ordenada_Subsets_TFM.xlsx`                     |
|     3 | `03_integracion_ecg.ipynb`                          | Integración de parámetros ECG estructurados       | Base clínica procesada + `ecg_dataset.xlsx`          | Dataset multimodal integrado                         |
|     4 | `04_construccion_endpoint.ipynb`                    | Construcción del endpoint experimental            | Dataset integrado                                    | `RIESGO_CARDIOMETABOLICO`                            |
|     5 | `05_modelado_predictivo.ipynb`                      | Entrenamiento de modelos supervisados             | Dataset final de modelado                            | Métricas por modelo y escenario                      |
|     6 | `06_evaluacion_incremental_ecg.ipynb`               | Comparación incremental de modalidades            | Métricas consolidadas                                | Tablas de diferencias y análisis comparativo         |
|     7 | `07_interpretabilidad_shap.ipynb`                   | Interpretabilidad de modelos mediante SHAP        | Modelos entrenados                                   | Gráficos y tablas SHAP                               |

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

## Relación entre procesos

Los procesos forman una cadena reproducible de preparación de datos:

```text
Base de Datos Original.xlsx
        ?
Proceso 1: anonimización + normalización + PLN/NLP + flags clínicos
        ?
Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx
        ?
Proceso 2: completitud + clustering estructural + pseudo-baterías
        ?
Base_Ordenada_Subsets_TFM.xlsx
        ?
Integración ECG + endpoint + modelado predictivo
```

El Proceso 1 transforma la base original en una cohorte anonimizada y analíticamente utilizable.

El Proceso 2 organiza esa cohorte en subconjuntos estructurales que permiten estudiar la estabilidad del modelado predictivo bajo diferentes configuraciones de disponibilidad de información.

## Relación con el TFM

Estos notebooks respaldan principalmente los siguientes capítulos del TFM:

```text
Capítulo 4: Construcción de la cohorte experimental multimodal.
Capítulo 5: Desarrollo experimental y modelado predictivo.
Capítulo 6: Notebooks, código fuente y datos analizados.
```

## Consideraciones de privacidad

La base original contiene información sensible y no debe ser publicada en un repositorio público.

No deben publicarse en GitHub:

```text
Base de Datos Original.xlsx
Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx
Base_Ordenada_Subsets_TFM.xlsx
ecg_dataset.xlsx
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
* script Python modular;
* semillas fijas en clustering;
* diccionarios de normalización;
* logs de transformación;
* separación entre datos originales, intermedios y derivados;
* documentación de entradas y salidas.

Cada notebook debe ejecutarse siguiendo el orden definido en la tabla inicial.

## Advertencia sobre uso clínico

Este repositorio tiene finalidad académica y experimental.

Los notebooks, pipelines y resultados asociados no constituyen una herramienta clínica validada, no deben utilizarse para diagnóstico, tratamiento ni toma de decisiones médicas, y requieren validación externa antes de cualquier uso aplicado en contextos sanitarios reales.
