# Laboral.AI — Dashboard de Empresas

## Descripción del proyecto

Laboral.AI es una plataforma que conecta **empresas y postulantes**, permitiendo a las empresas publicar oportunidades laborales y gestionar procesos de selección.

Este proyecto consiste en el desarrollo de un **dashboard interactivo para el módulo Empresas**, cuyo objetivo es transformar y consolidar información proveniente de diferentes colecciones de MongoDB para facilitar el análisis de las empresas registradas y su actividad dentro de la plataforma.

El dashboard busca proporcionar al área comercial una visión clara sobre el **crecimiento, características, estado y nivel de actividad de las empresas**, mediante indicadores y visualizaciones interactivas que apoyen la toma de decisiones basada en datos.

---

## Objetivos

### Objetivo general

Diseñar e implementar un dashboard de empresas que permita analizar la información de las empresas registradas en Laboral.AI y monitorear su actividad dentro de la plataforma mediante indicadores claros y visualizaciones interactivas.

### Objetivos específicos

* Analizar la información de las empresas registradas.
* Consolidar información proveniente de diferentes colecciones de MongoDB.
* Limpiar y transformar los datos para su análisis.
* Identificar indicadores relevantes para el área comercial.
* Analizar la evolución del registro de empresas.
* Analizar las características y el estado de las empresas.
* Medir la actividad empresarial mediante las ofertas laborales publicadas.
* Facilitar la exploración de los datos mediante filtros interactivos.
* Presentar los resultados mediante un dashboard visual y de fácil interpretación.

---

## Fuente de datos

La información utilizada proviene de la base de datos **MongoDB de Laboral.AI**.

Para la construcción del dashboard se consideran principalmente las siguientes colecciones:

* `companies`
* `jobs`
* `applications`

Estas colecciones permiten integrar información sobre las empresas, sus ofertas laborales y las postulaciones recibidas.

---

## Procesamiento de datos

El proceso de preparación de los datos contempla las siguientes etapas:

1. Conexión con MongoDB mediante variables de entorno.
2. Extracción de las colecciones necesarias.
3. Conversión de los datos a DataFrames mediante Pandas.
4. Selección de las columnas relevantes para el análisis.
5. Limpieza y tratamiento de valores nulos.
6. Normalización de categorías y nombres de empresas.
7. Transformación de estructuras anidadas.
8. Normalización de identificadores.
9. Cruce de información entre las colecciones.
10. Eliminación de registros duplicados cuando corresponde.
11. Creación de variables derivadas.
12. Construcción de datasets finales para el análisis.
13. Validación de los datos utilizados para los indicadores del dashboard.

---

## Análisis

El dashboard permite analizar principalmente:

### Crecimiento de empresas

* Evolución mensual de empresas registradas.
* Cantidad total de empresas.
* Comportamiento de nuevos registros.

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

La información de `applications` permite complementar el análisis de las ofertas laborales mediante la cantidad de postulaciones asociadas a cada oportunidad.

---

## Visualizaciones

Para facilitar la interpretación de los resultados se utilizan diferentes tipos de visualizaciones:

* **Tarjetas KPI** para mostrar indicadores principales.
* **Gráficos de barras** para comparar empresas, industrias y categorías.
* **Gráficos de dona** para representar distribuciones.
* **Gráficos de líneas** para analizar la evolución temporal.
* **Gráficos de barras horizontales** para rankings de empresas.
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
├── aplicación.py              # Aplicación principal del dashboard
├── README.md                  # Documentación del proyecto
├── requisitos.txt             # Dependencias del proyecto
├── .env.example               # Plantilla de variables de entorno
├── .gitignore                 # Archivos excluidos del repositorio
│
├── data/
│   └── cache/                 # Datos procesados almacenados temporalmente
│
└── scripts/
    ├── __init__.py            # Inicialización del paquete
    ├── conexion.py            # Conexión con MongoDB
    ├── constructor.py         # Procesamiento y construcción de datasets
    │
    └── indicadores/
        ├── __init__.py
        └── indicadores.py     # Cálculo de indicadores y generación
                               # de visualizaciones
```

> El archivo `.env` se utiliza únicamente de forma local y no se incluye en el repositorio, ya que puede contener información sensible.

---

## Funcionamiento

El dashboard funciona mediante un flujo de extracción, procesamiento, transformación y visualización de los datos provenientes de MongoDB.

### Flujo general

```text
MongoDB
   │
   ├── companies
   ├── jobs
   └── applications
          │
          ▼
    Extracción de datos
          │
          ▼
    Limpieza y transformación
          │
          ▼
    Integración de colecciones
          │
          ▼
    Construcción de datasets
          │
          ▼
    Cálculo de indicadores
          │
          ▼
    Visualizaciones con Plotly
          │
          ▼
    Dashboard con Streamlit
          │
          ▼
    Análisis interactivo
```

### Proceso de funcionamiento

1. **Conexión con MongoDB**
   La aplicación establece la conexión con la base de datos mediante las variables de entorno configuradas. Las credenciales no se almacenan directamente en el código fuente.

2. **Extracción de información**
   Se consultan las colecciones necesarias de MongoDB para obtener información sobre empresas, ofertas laborales y postulaciones.

3. **Procesamiento de datos**
   Los datos extraídos son convertidos a DataFrames mediante Pandas para facilitar su manipulación y análisis.

4. **Limpieza y transformación**
   Se realizan procesos de limpieza, tratamiento de valores nulos, normalización de categorías y nombres, transformación de estructuras anidadas y normalización de identificadores.

5. **Integración de información**
   Se relacionan los datos provenientes de las diferentes colecciones mediante los identificadores correspondientes, permitiendo analizar conjuntamente empresas, ofertas y postulaciones.

6. **Construcción de datasets**
   `constructor.py` contiene las funciones encargadas de procesar y construir los datasets que serán utilizados posteriormente por el dashboard.

7. **Cálculo de indicadores**
   Las funciones ubicadas en `scripts/indicadores/indicadores.py` permiten calcular los indicadores utilizados para analizar el crecimiento, perfil y actividad de las empresas.

8. **Generación de visualizaciones**
   Los resultados obtenidos son representados mediante gráficos interactivos utilizando Plotly.

9. **Presentación del dashboard**
   `aplicación.py` integra los datos, indicadores y visualizaciones en una interfaz desarrollada con Streamlit.

10. **Exploración interactiva**
    El usuario puede utilizar los filtros disponibles para segmentar la información y analizar diferentes características de las empresas y sus ofertas laborales.

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

El dashboard proporciona una visión centralizada de las empresas registradas en Laboral.AI y permite analizar su crecimiento, características y nivel de actividad.

La información obtenida puede servir como apoyo al **área comercial para el monitoreo de empresas, identificación de tendencias y toma de decisiones basada en datos**.
