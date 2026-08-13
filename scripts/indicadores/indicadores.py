import pandas as pd
import plotly.express as px


# ============================================================
# FUNCIONES MODULARES PARA INDICADORES
# ============================================================


def calcular_total_unico(df, columna):
    """
    Calcula el total de registros únicos de una columna.

    Puede reutilizarse para contar:
    - Empresas
    - Empleos
    - Postulaciones
    """

    return df[columna].nunique()


def contar_categorias(df, columna, etiqueta_nulos=None):
    """
    Cuenta la cantidad de registros de cada categoría.

    Si se proporciona una etiqueta para los valores nulos,
    estos serán reemplazados antes de realizar el conteo.
    """

    datos = df[columna].copy()

    if etiqueta_nulos is not None:
        datos = datos.fillna(etiqueta_nulos)

    return datos.value_counts()


def generar_ranking(df, columna, top_n=10):
    """
    Genera un ranking de los valores más frecuentes
    de una columna.

    top_n indica la cantidad máxima de resultados.
    """

    return (
        df[columna]
        .dropna()
        .value_counts()
        .head(top_n)
    )


def contar_condicion(df, columna, valor):
    """
    Cuenta la cantidad de registros que cumplen
    una condición determinada.

    Ejemplo:
    contar_condicion(jobs_clean, "isExternalOffer", True)
    """

    return df[columna].eq(valor).sum()


def contar_por_mes(df, columna_fecha):
    """
    Cuenta la cantidad de registros agrupados por mes
    utilizando una columna de fecha.
    """

    datos = df.copy()

    datos[columna_fecha] = pd.to_datetime(
        datos[columna_fecha],
        errors="coerce"
    )

    datos = datos.dropna(
        subset=[columna_fecha]
    )

    datos["mes"] = datos[columna_fecha].dt.to_period("M")

    return (
        datos["mes"]
        .value_counts()
        .sort_index()
    )


def crear_grafico_barras(
    df,
    x,
    y,
    titulo,
    color="#0a99ac"
):
    """
    Crea un gráfico de barras reutilizable
    utilizando Plotly.
    """

    fig = px.bar(
        df,
        x=x,
        y=y,
        title=titulo,
        text=y
    )

    fig.update_traces(
        marker_color=color,
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title=x,
        yaxis_title=y,
        hovermode="x unified"
    )

    return fig