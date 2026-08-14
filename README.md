# Laboral.AI — Dashboard de Empresas

## Descripción del proyecto

Laboral.AI es una plataforma que conecta **empresas y postulantes**, permitiendo a las empresas publicar oportunidades laborales y gestionar procesos de selección.

Este proyecto consiste en el desarrollo de un **dashboard interactivo para el módulo Empresas**, cuyo objetivo es transformar y consolidar información proveniente de diferentes colecciones de MongoDB para facilitar el análisis de las empresas registradas y su actividad dentro de la plataforma.

El dashboard proporciona al área comercial una visión sobre el **crecimiento, características y nivel de actividad de las empresas**, mediante indicadores y visualizaciones interactivas que apoyan la toma de decisiones basada en datos.

---

## Objetivos

### Objetivo general

Diseñar e implementar un dashboard de empresas que permita analizar la información de las empresas registradas en Laboral.AI y monitorear su actividad mediante indicadores y visualizaciones interactivas.

### Objetivos específicos

* Analizar la información de las empresas registradas.
* Consolidar información de diferentes colecciones de MongoDB.
* Limpiar y transformar los datos para su análisis.
* Identificar indicadores relevantes para el área comercial.
* Analizar la evolución y características de las empresas.
* Medir la actividad empresarial mediante las ofertas laborales publicadas.
* Facilitar la exploración de los datos mediante filtros interactivos.
* Presentar los resultados mediante un dashboard visual y de fácil interpretación.

---

## Fuente de datos

La información utilizada proviene de la base de datos **MongoDB de Laboral.AI**.

Las principales colecciones utilizadas son:

* `companies`
* `jobs`
* `applications`

Estas colecciones permiten integrar información sobre las empresas, sus ofertas laborales y las postulaciones recibidas.

---

## Procesamiento de datos

El procesamiento de los datos contempla las siguientes etapas:

1. Conexión con MongoDB mediante variables de entorno.
2. Extracción de las colecciones necesarias.
3. Conversión de los datos a DataFrames mediante Pandas.
4. Selección de las columnas relevantes.
5. Limpieza y tratamiento de valores nulos.
6. Normalización de categorías, nombres e identificadores.
7. Transformación de estructuras anidadas.
8. Cruce de información entre las colecciones.
9. Eliminación de duplicados cuando corresponde.
10. Creación de variables derivadas.
11. Construcción y validación de los datasets utilizados por el dashboard.

---

## Análisis

El dashboard permite analizar:

### Crecimiento de empresas

* Evolución mensual de empresas registradas.
* Cantidad total de empresas.
* Nuevos registros.

### Perfil empresarial

* Distribución por industria.
* Estado de actividad.
* Estado de verificación.
* Distribución por plan.

### Actividad empresarial

* Cantidad de ofertas publicadas.
* Empresas con mayor número de publicaciones.
* Evolución de las ofertas laborales.
* Modalidad de las ofertas.
* Distribución geográfica.
* Nivel de los puestos publicados.

### Postulaciones

La colección `applications` permite complementar el análisis mediante la cantidad de postulaciones asociadas a las ofertas laborales.

---

## Visualizaciones

El dashboard utiliza:

* **Tarjetas KPI** para los principales indicadores.
* **Gráficos de barras** para comparar categorías y empresas.
* **Gráficos de dona** para representar distribuciones.
* **Gráficos de líneas** para analizar tendencias temporales.
* **Gráficos de barras horizontales** para rankings.
* **Filtros interactivos** para segmentar la información.

---

## Tecnologías utilizadas

* **Python**
* **Pandas**
* **NumPy**
* **Plotly**
* **Streamlit**
* **MongoDB**
* **GitHub**

---

## Estructura del proyecto

```text
laboral-ai-dashboard-empresas/
│
├── aplicación.py
├── README.md
├── requisitos.txt
├── .env.example
├── .gitignore
│
├── data/
│   └── cache/
│
└── scripts/
    ├── __init__.py
    ├── conexion.py
    ├── constructor.py
    │
    └── indicadores/
        ├── __init__.py
        └── indicadores.py
```

* `aplicación.py`: aplicación principal del dashboard.
* `conexion.py`: conexión con MongoDB.
* `constructor.py`: procesamiento y construcción de datasets.
* `indicadores.py`: cálculo de indicadores y generación de visualizaciones.
* `data/cache/`: almacenamiento temporal de datos procesados.

> El archivo `.env` se utiliza únicamente de forma local y no se incluye en el repositorio debido a que puede contener información sensible.

---

## Funcionamiento

El dashboard sigue un flujo de procesamiento que integra los datos de MongoDB y los transforma en indicadores y visualizaciones interactivas.

```text
MongoDB
   │
   ├── companies
   ├── jobs
   └── applications
          │
          ▼
    Extracción y procesamiento
          │
          ▼
    Integración de datos
          │
          ▼
    Datasets procesados
          │
          ▼
    Indicadores
          │
          ▼
    Visualizaciones con Plotly
          │
          ▼
    Dashboard con Streamlit
```

---

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/ani-bert/laboral-ai-dashboard-empresas.git
cd laboral-ai-dashboard-empresas
```

### 2. Crear un entorno virtual

En macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar las dependencias

```bash
pip install -r requisitos.txt
```

### 4. Configurar las variables de entorno

Crear un archivo `.env` a partir de `.env.example` y completar las variables necesarias para la conexión con MongoDB.

Por seguridad, **no se deben incluir credenciales reales en el repositorio**.

### 5. Ejecutar el dashboard

```bash
streamlit run aplicación.py
```

---

## Resultado esperado

El dashboard proporciona una visión centralizada de las empresas registradas en Laboral.AI, permitiendo analizar su crecimiento, características y nivel de actividad.

La información puede servir como apoyo al **área comercial para identificar tendencias y tomar decisiones basadas en datos**.

---

## Autor

**Anahis Ramirez**
