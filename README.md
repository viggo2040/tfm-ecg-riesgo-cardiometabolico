# tfm-ecg-riesgo-cardiometabolico

Repositorio del Trabajo Fin de Máster orientado a la construcción de una cohorte clínica multimodal y a la evaluación del valor incremental de parámetros electrocardiográficos estructurados en modelos predictivos de riesgo cardiometabólico.

## Descripción

Este repositorio contiene notebooks, scripts y documentación técnica desarrollados para reproducir el pipeline experimental del TFM:

**Evaluación del valor incremental de parámetros ECG en riesgo cardiometabólico**

El proyecto se centra en la construcción de una cohorte clínica anonimizada, el procesamiento de antecedentes médicos mediante PLN/NLP, la generación de variables clínicas derivadas, la segmentación estructural de la cohorte en pseudo-baterías clínicas y la posterior evaluación de modelos predictivos basados en variables clínicas, antecedentes textuales estructurados y parámetros ECG.

El objetivo principal es determinar si la incorporación de parámetros electrocardiográficos estructurados derivados de reportes ECG digitales aporta valor incremental frente a modelos construidos únicamente con variables clínicas tradicionales.

## Objetivo del repositorio

El repositorio busca disponibilizar de forma trazable y reproducible los procesos técnicos asociados al TFM, incluyendo:

* anonimización de registros clínicos;
* normalización de variables clínicas;
* procesamiento de antecedentes médicos mediante PLN/NLP;
* generación de indicadores cardiometabólicos;
* construcción de subconjuntos estructurales de la cohorte;
* integración de información clínica y electrocardiográfica;
* construcción del endpoint experimental;
* entrenamiento y evaluación de modelos predictivos;
* análisis de interpretabilidad mediante SHAP;
* documentación de trazabilidad y reproducibilidad experimental.

## Contexto metodológico

La base clínica original corresponde a registros procedentes de evaluaciones médicas reales. Debido a su naturaleza heterogénea, no todos los pacientes disponen del mismo conjunto de variables, antecedentes clínicos o exámenes complementarios.

Por esta razón, el flujo técnico del TFM no utiliza directamente la base original, sino que aplica procesos previos de anonimización, normalización, estructuración semántica y análisis de completitud.

El pipeline completo sigue la siguiente lógica:

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
Integración ECG + endpoint + modelado predictivo
        ↓
Evaluación incremental + interpretabilidad SHAP
```

## Procesos principales

### Proceso 1: Anonimización, normalización clínica y PLN/NLP

El primer proceso toma como entrada la base clínica original:

```text
Base de Datos Original.xlsx
```

y ejecuta el pipeline implementado en:

```text
pipeline_cohorte_tfm.py
Notebook_Proceso_PLN1.ipynb
```

Este proceso genera como salida principal:

```text
Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx
```

#### Transformaciones principales

El proceso realiza las siguientes operaciones:

```text
1. Lectura de la base clínica original.
2. Limpieza y estandarización de nombres de columnas.
3. Eliminación de identificadores directos.
4. Generación de PACIENTE_ID secuencial anónimo.
5. Generalización temporal de fechas de atención.
6. Normalización de variables clínicas numéricas.
7. Codificación binaria de variables clínicas.
8. Limpieza textual de antecedentes médicos.
9. Detección de conceptos clínicos mediante reglas PLN/NLP.
10. Detección básica de negaciones clínicas.
11. Generación de variables ANT_*.
12. Generación de flags cardiometabólicos FLAG_*.
13. Cálculo de completitud y conteos.
14. Exportación de archivo Excel procesado, diccionario clínico y log.
```

#### Variables derivadas mediante PLN/NLP

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

#### Indicadores cardiometabólicos generados

También se generan variables derivadas asociadas a factores de riesgo cardiometabólico:

```text
FLAG_PA_SISTOLICA_ALTA
FLAG_PA_DIASTOLICA_ALTA
FLAG_GLICEMIA_ALTA
FLAG_LDL_ALTO
FLAG_TRIGLICERIDOS_ALTOS
FLAG_OBESIDAD_IMC
FLAG_HDL_BAJO
```

Estas variables sirven como insumo para la construcción del endpoint operacional:

```text
RIESGO_CARDIOMETABOLICO
```

### Proceso 2: Segmentación estructural y pseudo-baterías clínicas

El segundo proceso toma como entrada:

```text
Base_Datos_Original_Anonimizada_Procesada_TFM.xlsx
```

y reproduce la generación del archivo:

```text
Base_Ordenada_Subsets_TFM.xlsx
```

mediante el notebook:

```text
Notebook_Proceso_PLN2.ipynb
```

#### Finalidad metodológica

La cohorte procesada presenta heterogeneidad estructural. Esto significa que la disponibilidad de información no es idéntica para todos los pacientes.

En lugar de eliminar registros incompletos, este proceso permite representar explícitamente la disponibilidad diferencial de información mediante subconjuntos estructurales o pseudo-baterías clínicas.

#### Lógica técnica

El proceso reconstruido se basa en:

```text
1. Cálculo de completitud por paciente.
2. Construcción de matriz binaria de presencia/ausencia.
3. Segmentación estructural mediante clustering.
4. Asignación de pacientes a pseudo-baterías clínicas.
```

El clustering estructural se realiza con:

```python
KMeans(n_clusters=4, random_state=42)
```

Los subconjuntos generados son:

```text
BATERIA_A
BATERIA_B
BATERIA_C
BATERIA_D
```

Estos subconjuntos no representan grupos clínicos, diagnósticos ni demográficos. Representan configuraciones de disponibilidad de datos.

## Estructura recomendada del repositorio

```text
tfm-ecg-riesgo-cardiometabolico/
│
├── README.md
├── requirements.txt
├── environment.yml
├── .gitignore
├── LICENSE
│
├── notebooks/
│   ├── 01_proceso_pln1_anonimizacion_normalizacion.ipynb
│   ├── 02_proceso_pln2_subsets_baterias.ipynb
│   ├── 03_integracion_ecg.ipynb
│   ├── 04_construccion_endpoint.ipynb
│   ├── 05_modelado_predictivo.ipynb
│   ├── 06_evaluacion_incremental_ecg.ipynb
│   └── 07_interpretabilidad_shap.ipynb
│
├── src/
│   ├── pipeline_cohorte_tfm.py
│   ├── preprocessing.py
│   ├── nlp_clinico.py
│   ├── subset_clustering.py
│   ├── modelado.py
│   └── utils.py
│
├── data/
│   ├── raw/
│   │   └── README.md
│   ├── processed/
│   │   └── README.md
│   └── synthetic/
│       └── datos_ejemplo_sinteticos.xlsx
│
├── outputs/
│   ├── metrics/
│   ├── figures/
│   └── logs/
│
├── docs/
│   ├── descripcion_metodologica.md
│   ├── diccionario_variables.md
│   ├── trazabilidad_datasets.md
│   └── privacidad_datos.md
│
└── reports/
    └── tablas_resultados_entrega3.xlsx
```

## Archivos principales

```text
pipeline_cohorte_tfm.py
Notebook_Proceso_PLN1.ipynb
Notebook_Proceso_PLN2.ipynb
```

Según disponibilidad y restricciones de privacidad, el repositorio puede incluir también:

```text
Diccionario_Normalizacion_Antecedentes.csv
Log_Transformacion_Cohorte_TFM.txt
datos sintéticos de ejemplo
tablas de métricas anonimizadas
figuras generadas
documentación metodológica
```

## Datos clínicos y privacidad

La base clínica original contiene información sensible y no debe publicarse en un repositorio público.

No deben publicarse:

```text
Base de Datos Original.xlsx
PDFs ECG originales
archivos con nombres de pacientes
rutas relativas con identificadores
campos nombre_paciente
campos nombre_paciente_norm
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
archivos sintéticos de ejemplo
README técnico
documentación metodológica
```

Los datos reales deben mantenerse en un entorno privado o ser reemplazados por versiones sintéticas, anonimizadas y autorizadas para fines académicos.

## Reproducibilidad

La reproducibilidad del proyecto se apoya en:

```text
notebooks ejecutables
scripts Python modulares
semillas fijas en clustering
diccionarios de normalización
logs de transformación
separación entre datos originales, intermedios y derivados
documentación de entradas y salidas
```

Cada notebook debe ejecutarse siguiendo el orden numérico definido en la carpeta `notebooks/`.

## Relación con el TFM

Este repositorio respalda principalmente los siguientes capítulos del TFM:

```text
Capítulo 4: Construcción de la cohorte experimental multimodal.
Capítulo 5: Desarrollo experimental y modelado predictivo.
Capítulo 6: Notebooks, código fuente y datos analizados.
```

Su propósito es aportar evidencia técnica reproducible para la construcción de la cohorte, la preparación de datos, la integración multimodal y la evaluación experimental del valor incremental de parámetros ECG.

## Licencia

Este repositorio utiliza licencia MIT.

La licencia cubre el código fuente, notebooks y documentación técnica del repositorio. No autoriza la publicación ni reutilización de datos clínicos reales que puedan estar sujetos a restricciones de privacidad, confidencialidad o autorización institucional.

## Advertencia sobre uso clínico

Este repositorio tiene finalidad académica y experimental.

Los modelos, notebooks y resultados asociados no constituyen una herramienta clínica validada, no deben utilizarse para diagnóstico, tratamiento ni toma de decisiones médicas, y requieren validación externa antes de cualquier uso aplicado en contextos sanitarios reales.
