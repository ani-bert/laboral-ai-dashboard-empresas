import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import unicodedata

from scripts.constructor import constructor

from scripts.indicadores.indicadores import (
    calcular_total_unico,
    contar_categorias,
    contar_condicion,
    contar_por_mes,
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Dashboard de Empresas | Laboral.ai",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# COLORES
# ============================================================

AZUL_OSCURO = "#0B213C"
AZUL_PANEL = "#0B213C"
AZUL_HOVER = "#123557"
AZUL_DESPLIEGUE = "#0E2F51"
AZUL_SUAVE = "#E4F2FC"

BLANCO = "#FFFFFF"

FONDO = "#F5F7FA"

NEGRO = "#000000"

GRIS_TEXTO = "#6F7A86"
GRIS_BORDE = "#D6DEE7"
GRIS_CLARO = "#AAB6C2"

AMARILLO = "#F3C623"


# ============================================================
# COLORES DE GRÁFICOS
# ============================================================

VERDE_BARRA = "#A6C263"

CELESTE_BARRA = "#66C7D1"

AMARILLO_BARRA = "#FFDE59"

MORADO_BARRA = "#754480"

AZUL_LINEA = AZUL_OSCURO

AZUL_MAPA = "#0A99AC"

AZUL_MAPA_CLARO = "#E7F5F7"


# ============================================================
# URL GEOJSON DEL PERÚ
# ============================================================

PERU_GEOJSON_URL = (
    "https://raw.githubusercontent.com/"
    "juaneladio/peru-geojson/master/"
    "peru_departamental_simple.geojson"
)


# ============================================================
# CSS GENERAL
# ============================================================

st.markdown(
    f"""
    <style>

    /* ========================================================
       FONDO GENERAL
       ======================================================== */

    html,
    body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .stApp,
    .main {{
        background-color: {FONDO} !important;
    }}

    .block-container {{
        max-width: 1550px !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2.8rem !important;
        padding-right: 2.8rem !important;
    }}

    [data-testid="stHeader"] {{
        background: transparent !important;
        height: 0 !important;
        min-height: 0 !important;
        border: none !important;
    }}

    header {{
        background: transparent !important;
        height: 0 !important;
        min-height: 0 !important;
        border: none !important;
    }}

    [data-testid="stDecoration"] {{
        display: none !important;
    }}

    #MainMenu {{
        visibility: hidden !important;
    }}

    footer {{
        visibility: hidden !important;
    }}


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {{
        background-color: {AZUL_OSCURO} !important;
        border-right: none !important;
        box-shadow:
            4px 0 18px rgba(11, 33, 60, 0.10) !important;
    }}

    section[data-testid="stSidebar"] > div {{
        background-color: {AZUL_OSCURO} !important;
    }}

    section[data-testid="stSidebar"]
    [data-testid="stSidebarContent"] {{
        background-color: {AZUL_OSCURO} !important;
    }}

    section[data-testid="stSidebar"] * {{
        box-sizing: border-box;
    }}


    /* ========================================================
       BOTÓN SIDEBAR CERRADO
       ======================================================== */

    [data-testid="stSidebarCollapsedControl"] {{
        position: fixed !important;
        top: 16px !important;
        left: 16px !important;
        z-index: 999999 !important;
        width: 38px !important;
        height: 38px !important;
        min-width: 38px !important;
        min-height: 38px !important;
        max-width: 38px !important;
        max-height: 38px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background-color: {AZUL_DESPLIEGUE} !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow:
            0 4px 12px rgba(11, 33, 60, 0.22) !important;
        opacity: 1 !important;
        visibility: visible !important;
        overflow: hidden !important;
    }}

    [data-testid="stSidebarCollapsedControl"] button {{
        width: 38px !important;
        height: 38px !important;
        min-width: 38px !important;
        min-height: 38px !important;
        padding: 0 !important;
        margin: 0 !important;
        background-color: {AZUL_DESPLIEGUE} !important;
        border: none !important;
        border-radius: 8px !important;
        color: {BLANCO} !important;
        -webkit-text-fill-color: {BLANCO} !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    [data-testid="stSidebarCollapsedControl"] button:hover {{
        background-color: {AZUL_HOVER} !important;
        color: {BLANCO} !important;
    }}

    [data-testid="stSidebarCollapsedControl"] svg {{
        width: 20px !important;
        height: 20px !important;
        color: {BLANCO} !important;
        fill: none !important;
        stroke: {BLANCO} !important;
        stroke-width: 2.5 !important;
    }}

    [data-testid="stSidebarCollapsedControl"] svg path,
    [data-testid="stSidebarCollapsedControl"] svg line,
    [data-testid="stSidebarCollapsedControl"] svg polyline {{
        stroke: {BLANCO} !important;
        color: {BLANCO} !important;
    }}


    /* ========================================================
       TEXTO SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {{
        color: {BLANCO} !important;
    }}

    section[data-testid="stSidebar"] p {{
        color: #D4DEE8 !important;
    }}

    section[data-testid="stSidebar"] label {{
        color: {BLANCO} !important;
    }}

    section[data-testid="stSidebar"] label p {{
        color: {BLANCO} !important;
    }}

    .filter-label {{
        color: {BLANCO} !important;
        font-family: Arial, sans-serif;
        font-size: 14px;
        font-weight: 400;
        margin-bottom: 0.45rem;
    }}

    .date-section-title {{
        color: {BLANCO} !important;
        font-family: Arial, sans-serif;
        font-size: 14px;
        font-weight: 400;
        margin-top: 1.1rem;
        margin-bottom: 0.5rem;
    }}


    /* ========================================================
       SELECTBOX
       ======================================================== */

    section[data-testid="stSidebar"]
    [data-baseweb="select"] {{
        width: 100% !important;
    }}

    section[data-testid="stSidebar"]
    [data-baseweb="select"] > div {{
        background-color: {AZUL_PANEL} !important;
        color: {BLANCO} !important;
        border: 1px solid #8393A4 !important;
        border-radius: 10px !important;
        min-height: 42px !important;
        box-shadow: none !important;
    }}

    section[data-testid="stSidebar"]
    [data-baseweb="select"] > div:hover {{
        background-color: {AZUL_HOVER} !important;
        border-color: #B9C7D4 !important;
    }}

    section[data-testid="stSidebar"]
    [data-baseweb="select"] span {{
        color: {BLANCO} !important;
    }}

    section[data-testid="stSidebar"]
    [data-baseweb="select"] input {{
        color: {BLANCO} !important;
        background: transparent !important;
    }}

    section[data-testid="stSidebar"]
    [data-baseweb="select"] svg {{
        color: {BLANCO} !important;
        fill: {BLANCO} !important;
    }}


    /* ========================================================
       POPUP SELECTBOX
       ======================================================== */

    [data-baseweb="popover"] {{
        background-color: {BLANCO} !important;
        border: 1px solid {GRIS_BORDE} !important;
        border-radius: 10px !important;
        box-shadow:
            0 12px 30px rgba(11, 33, 60, 0.16) !important;
    }}

    [data-baseweb="menu"] {{
        background-color: {BLANCO} !important;
    }}

    [role="option"] {{
        background-color: {BLANCO} !important;
        color: #263442 !important;
    }}

    [role="option"]:hover {{
        background-color: #EEF4F9 !important;
        color: {AZUL_OSCURO} !important;
    }}


    /* ========================================================
       RADIO
       ======================================================== */

    section[data-testid="stSidebar"]
    [data-testid="stRadio"] {{
        margin-top: 0.2rem !important;
        margin-bottom: 1.2rem !important;
    }}

    section[data-testid="stSidebar"]
    [data-testid="stRadio"] label {{
        color: #E8EFF5 !important;
        font-size: 13px !important;
    }}

    section[data-testid="stSidebar"]
    [data-testid="stRadio"] label p {{
        color: #E8EFF5 !important;
    }}


    /* ========================================================
       FECHAS
       ======================================================== */

    section[data-testid="stSidebar"]
    [data-testid="stDateInput"] {{
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    section[data-testid="stSidebar"]
    [data-testid="stDateInput"] label {{
        color: #D6E0E9 !important;
        font-size: 11px !important;
    }}

    section[data-testid="stSidebar"]
    [data-testid="stDateInput"] label p {{
        color: #D6E0E9 !important;
        font-size: 11px !important;
    }}

    section[data-testid="stSidebar"]
    [data-testid="stDateInput"] > div > div {{
        background-color: {AZUL_PANEL} !important;
        border: 1px solid #8393A4 !important;
        border-radius: 12px !important;
        min-height: 42px !important;
        box-shadow: none !important;
    }}

    section[data-testid="stSidebar"]
    [data-testid="stDateInput"] > div > div:hover {{
        background-color: {AZUL_HOVER} !important;
        border-color: #B9C7D4 !important;
    }}

    section[data-testid="stSidebar"]
    [data-testid="stDateInput"] input {{
        background: transparent !important;
        color: {BLANCO} !important;
        -webkit-text-fill-color: {BLANCO} !important;
        border: none !important;
        box-shadow: none !important;
        font-size: 12px !important;
    }}

    section[data-testid="stSidebar"]
    [data-testid="stDateInput"] svg {{
        color: {BLANCO} !important;
        fill: {BLANCO} !important;
    }}


    /* ========================================================
       CALENDARIO
       ======================================================== */

    [data-baseweb="calendar"] {{
        background-color: #E4F2FC !important;
        border: none !important;
        border-radius: 14px !important;
        overflow: hidden !important;
        box-shadow:
            0 14px 40px rgba(11, 33, 60, 0.25) !important;
        padding: 0 !important;
    }}

    [data-baseweb="calendar"] > div:first-child {{
        background-color: #1E1E24 !important;
        border-radius: 14px 14px 0 0 !important;
        padding: 10px !important;
    }}

    [data-baseweb="calendar"] table {{
        background-color: #E4F2FC !important;
        border-collapse: separate !important;
        border-spacing: 3px !important;
        padding: 8px !important;
    }}

    [data-baseweb="calendar"] thead,
    [data-baseweb="calendar"] tbody,
    [data-baseweb="calendar"] tr,
    [data-baseweb="calendar"] td {{
        background-color: #E4F2FC !important;
    }}

    [data-baseweb="calendar"] th {{
        background-color: #E4F2FC !important;
        color: #1E1E24 !important;
        font-size: 11px !important;
        font-weight: 700 !important;
    }}

    [data-baseweb="calendar"]
    [role="gridcell"] button {{
        background-color: transparent !important;
        color: {NEGRO} !important;
        border: 1px solid transparent !important;
        border-radius: 50% !important;
        width: 34px !important;
        height: 34px !important;
        min-width: 34px !important;
        min-height: 34px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    [data-baseweb="calendar"]
    [role="gridcell"] button:hover {{
        background-color: #CFE7F6 !important;
        color: {NEGRO} !important;
    }}

    [data-baseweb="calendar"]
    [aria-selected="true"] button {{
        background-color: {AMARILLO} !important;
        color: {NEGRO} !important;
        border: 2px solid #D8A900 !important;
        border-radius: 50% !important;
        font-weight: 700 !important;
    }}


    /* ========================================================
       BOTONES SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"]
    .stButton > button {{
        background-color: {AZUL_SUAVE} !important;
        color: {AZUL_OSCURO} !important;
        -webkit-text-fill-color: {AZUL_OSCURO} !important;
        border: 1px solid {AZUL_SUAVE} !important;
        border-radius: 10px !important;
        min-height: 42px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }}

    section[data-testid="stSidebar"]
    .stButton > button:hover {{
        background-color: #D2E8F6 !important;
        color: {AZUL_OSCURO} !important;
        border-color: #D2E8F6 !important;
    }}


    /* ========================================================
       TÍTULOS
       ======================================================== */

    h1 {{
        color: {NEGRO} !important;
        font-size: 2.45rem !important;
        line-height: 1.1 !important;
        font-weight: 750 !important;
        letter-spacing: -0.035em !important;
    }}

    h2 {{
        color: {NEGRO} !important;
        font-size: 1.42rem !important;
        font-weight: 700 !important;
    }}

    h3 {{
        color: #27313D !important;
    }}


    /* ========================================================
       TEXTO GENERAL
       ======================================================== */

    .dashboard-subtitle {{
        color: #78828E !important;
        font-size: 0.96rem;
        margin-top: 0.15rem;
        margin-bottom: 1.8rem;
    }}

    .section-caption {{
        color: #8A939E !important;
        font-size: 0.82rem;
        margin-top: -0.35rem;
        margin-bottom: 1rem;
    }}


    /* ========================================================
       KPI
       ======================================================== */

    div[data-testid="stMetric"] {{
        background-color: #FFFFFF !important;
        border: 1px solid #E3E7EC !important;
        border-radius: 15px !important;
        min-height: 128px !important;
        padding: 1.15rem 1rem !important;
        box-shadow:
            0 5px 18px rgba(23, 32, 42, 0.045) !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
    }}

    div[data-testid="stMetric"]:hover {{
        box-shadow:
            0 8px 24px rgba(23, 32, 42, 0.08) !important;
        transform: translateY(-1px);
    }}

    div[data-testid="stMetric"]
    [data-testid="stMetricLabel"] {{
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        color: #000000 !important;
        font-family: Arial, sans-serif !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
        text-align: center !important;
    }}

    div[data-testid="stMetric"]
    [data-testid="stMetricLabel"] * {{
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-family: Arial, sans-serif !important;
        font-size: 13px !important;
        font-weight: 700 !important;
    }}

    div[data-testid="stMetric"]
    [data-testid="stMetricValue"] {{
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-family: Arial, sans-serif !important;
        font-size: 30px !important;
        font-weight: 750 !important;
        line-height: 1.1 !important;
        text-align: center !important;
    }}

    div[data-testid="stMetric"]
    [data-testid="stMetricValue"] * {{
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-family: Arial, sans-serif !important;
        font-size: 30px !important;
        font-weight: 750 !important;
    }}

    div[data-testid="stMetricDelta"] {{
        display: none !important;
    }}


    /* ========================================================
       TARJETAS DE GRÁFICOS
       ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {BLANCO} !important;
        border: 1px solid #E2E6EB !important;
        border-radius: 16px !important;
        box-shadow:
            0 5px 20px rgba(23, 32, 42, 0.045) !important;
        padding: 0.25rem !important;
    }}


    /* ========================================================
       TARJETAS ALINEADAS
       ======================================================== */

    .dashboard-card {{
        height: 100%;
        min-height: 600px;
        display: flex;
        flex-direction: column;
    }}

    .dashboard-card-content {{
        flex: 1;
        display: flex;
        flex-direction: column;
    }}

    .chart-title {{
        color: #27313D !important;
        font-size: 1rem;
        font-weight: 700;
        margin-top: 0.15rem;
        margin-bottom: 0.15rem;
    }}

    .chart-description {{
        color: #929AA4 !important;
        font-size: 0.76rem;
        margin-bottom: 0.3rem;
    }}


    /* ========================================================
       PLOTLY
       ======================================================== */

    .js-plotly-plot {{
        width: 100% !important;
    }}


    /* ========================================================
       SEPARADORES
       ======================================================== */

    hr {{
        border: none !important;
        border-top: 1px solid #E2E6EB !important;
        margin: 1.7rem 0 !important;
    }}


    /* ========================================================
       RESPONSIVE
       ======================================================== */

    @media (max-width: 900px) {{

        .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}

        h1 {{
            font-size: 2rem !important;
        }}

        [data-testid="stSidebarCollapsedControl"] {{
            top: 12px !important;
            left: 12px !important;
            width: 36px !important;
            height: 36px !important;
        }}

        [data-testid="stSidebarCollapsedControl"] button {{
            width: 36px !important;
            height: 36px !important;
        }}

        .dashboard-card {{
            min-height: auto;
        }}

    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNCIONES DE GRÁFICOS
# ============================================================

def estilizar_figura(
    fig,
    altura=350,
):

    fig.update_layout(
        height=altura,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family="Arial, sans-serif",
            color="#59636F",
            size=11,
        ),

        margin=dict(
            l=10,
            r=15,
            t=10,
            b=10,
        ),

        showlegend=False,

        hoverlabel=dict(
            bgcolor="#17202A",
            font_size=12,
            font_color="#FFFFFF",
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        showline=False,
        tickfont=dict(
            color="#7A838F",
            size=10,
        ),
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EEF1F4",
        gridwidth=1,
        zeroline=False,
        showline=False,
        tickfont=dict(
            color="#7A838F",
            size=10,
        ),
    )

    return fig


# ============================================================
# GRÁFICO DE BARRAS
# ============================================================

def grafico_barras(
    df,
    x,
    y,
    horizontal=False,
    altura=350,
    color=VERDE_BARRA,
):

    if df is None or df.empty:

        return None

    df = df.copy()

    if horizontal:

        fig = px.bar(
            df,
            x=y,
            y=x,
            orientation="h",
            text=y,
            color_discrete_sequence=[
                color
            ],
        )

        fig.update_yaxes(
            categoryorder="total ascending",
            automargin=True,
        )

        fig.update_traces(
            marker_color=color,
            marker_line_width=0,
            textposition="outside",
            cliponaxis=False,
            textfont=dict(
                color="#263442",
                size=11,
                family="Arial, sans-serif",
            ),
            hovertemplate=(
                "%{y}<br>"
                "<b>%{x}</b>"
                "<extra></extra>"
            ),
        )

    else:

        fig = px.bar(
            df,
            x=x,
            y=y,
            text=y,
            color_discrete_sequence=[
                color
            ],
        )

        fig.update_traces(
            marker_color=color,
            marker_line_width=0,
            textposition="outside",
            cliponaxis=False,
            textfont=dict(
                color="#263442",
                size=11,
                family="Arial, sans-serif",
            ),
            hovertemplate=(
                "%{x}<br>"
                "<b>%{y}</b>"
                "<extra></extra>"
            ),
        )

    fig.update_layout(
        uniformtext_minsize=9,
        uniformtext_mode="hide",
        margin=dict(
            l=10,
            r=45,
            t=25,
            b=10,
        ),
    )

    return estilizar_figura(
        fig,
        altura,
    )


# ============================================================
# FUNCIÓN COLOR HEX -> RGBA
# ============================================================

def hex_a_rgba(
    color_hex,
    alpha=0.14,
):

    color_hex = color_hex.lstrip("#")

    if len(color_hex) != 6:

        return (
            "rgba(11, 33, 60, "
            f"{alpha})"
        )

    rojo = int(
        color_hex[0:2],
        16,
    )

    verde = int(
        color_hex[2:4],
        16,
    )

    azul = int(
        color_hex[4:6],
        16,
    )

    return (
        f"rgba("
        f"{rojo}, "
        f"{verde}, "
        f"{azul}, "
        f"{alpha})"
    )


# ============================================================
# GRÁFICO DE LÍNEA CON ÁREA
# ============================================================

def grafico_linea(
    df,
    x,
    y,
    altura=340,
    color=AZUL_LINEA,
):

    if df is None or df.empty:

        return None

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df[x],
            y=df[y],
            mode="lines",
            line=dict(
                color=color,
                width=0,
            ),
            fill="tozeroy",
            fillcolor=hex_a_rgba(
                color,
                alpha=0.14,
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df[x],
            y=df[y],
            mode="lines+markers",
            line=dict(
                color=color,
                width=3,
            ),
            marker=dict(
                size=7,
                color=color,
                line=dict(
                    width=2,
                    color=BLANCO,
                ),
            ),
            hovertemplate=(
                "%{x}<br>"
                "<b>%{y}</b>"
                "<extra></extra>"
            ),
            showlegend=False,
        )
    )

    fig.update_layout(
        height=altura,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Arial, sans-serif",
            color="#59636F",
            size=11,
        ),
        margin=dict(
            l=10,
            r=15,
            t=10,
            b=10,
        ),
        showlegend=False,
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        showline=False,
        type="category",
        automargin=True,
        tickfont=dict(
            color="#7A838F",
            size=10,
        ),
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#EEF1F4",
        gridwidth=1,
        zeroline=False,
        showline=False,
        tickfont=dict(
            color="#7A838F",
            size=10,
        ),
    )

    return fig


# ============================================================
# TARJETA DE GRÁFICO
# ============================================================

def tarjeta_grafico(
    titulo,
    descripcion=None,
):

    st.markdown(
        f"""
        <div class="chart-title">
            {titulo}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if descripcion:

        st.markdown(
            f"""
            <div class="chart-description">
                {descripcion}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# NORMALIZAR IDS
# ============================================================

def normalizar_id(
    serie,
):

    return (
        serie
        .astype(str)
        .str.strip()
    )


# ============================================================
# NORMALIZAR TEXTO
# ============================================================

def normalizar_texto(
    texto,
):

    if pd.isna(texto):

        return ""

    texto = str(texto).strip()

    texto = unicodedata.normalize(
        "NFKD",
        texto,
    )

    texto = "".join(
        caracter

        for caracter in texto

        if not unicodedata.combining(
            caracter
        )
    )

    return texto.upper()


# ============================================================
# NORMALIZAR NOMBRE DE EMPRESA
# ============================================================

def normalizar_empresa(
    nombre,
):

    if pd.isna(nombre):

        return ""

    nombre = str(nombre).strip()

    if not nombre:

        return ""

    nombre = unicodedata.normalize(
        "NFKD",
        nombre,
    )

    nombre = "".join(
        caracter
        for caracter in nombre
        if not unicodedata.combining(
            caracter
        )
    )

    nombre = nombre.upper()

    nombre = (
        nombre
        .replace(".", " ")
        .replace(",", " ")
        .replace(";", " ")
        .replace(":", " ")
        .replace("-", " ")
        .replace("_", " ")
    )

    nombre = " ".join(
        nombre.split()
    )

    # ========================================================
    # HOMOLOGACIÓN DE FORMAS JURÍDICAS
    # ========================================================

    reemplazos = {
        " SOCIEDAD ANONIMA CERRADA": " SAC",
        " SOCIEDAD ANONIMA": " SA",
        " SOCIEDAD COMERCIAL DE RESPONSABILIDAD LIMITADA": " SRL",
        " SOCIEDAD COMERCIAL DE RESPONSABILIDAD LIMITADA ": " SRL",
        " S A C": " SAC",
        " S A": " SA",
        " S R L": " SRL",
        " S A A": " SAA",
    }

    for original, reemplazo in reemplazos.items():

        if nombre.endswith(original):

            nombre = (
                nombre[
                    : -len(original)
                ].strip()
                + reemplazo
            )

    return nombre.strip()


# ============================================================
# CARGA DE DATOS
# ============================================================

@st.cache_data
def cargar_datos():

    return constructor()


# ============================================================
# CARGAR GEOJSON DEL PERÚ
# ============================================================

@st.cache_data
def cargar_geojson_peru():

    respuesta = requests.get(
        PERU_GEOJSON_URL,
        timeout=30,
    )

    respuesta.raise_for_status()

    return respuesta.json()


# ============================================================
# CARGA ETL
# ============================================================

try:

    (
        companies_clean,
        jobs_clean,
        applications_clean,
        applications_jobs,
        applications_final,
    ) = cargar_datos()

except Exception as e:

    st.error(
        "No se pudieron cargar los datos del ETL."
    )

    st.exception(e)

    st.stop()


# ============================================================
# COPIAS DE TRABAJO
# ============================================================

companies = companies_clean.copy()

jobs = jobs_clean.copy()

applications = applications_clean.copy()

applications_jobs_df = applications_jobs.copy()

applications_final_df = applications_final.copy()


# ============================================================
# VALIDACIONES
# ============================================================

columnas_jobs_requeridas = [
    "_id",
    "createdAt",
]

faltantes_jobs = [
    columna
    for columna in columnas_jobs_requeridas
    if columna not in jobs.columns
]

if faltantes_jobs:

    st.error(
        "Faltan columnas necesarias en jobs_clean: "
        f"{faltantes_jobs}"
    )

    st.stop()


# ============================================================
# NORMALIZACIÓN DE FECHAS
# ============================================================

jobs["createdAt"] = pd.to_datetime(
    jobs["createdAt"],
    errors="coerce",
)

jobs = jobs.dropna(
    subset=["createdAt"]
).copy()


if jobs.empty:

    st.error(
        "No existen ofertas con fechas válidas."
    )

    st.stop()


# ============================================================
# ÁREAS PROFESIONALES
# ============================================================

areas_profesionales = [

    "Administración, Contabilidad y Finanzas",

    "Aduanas y Comercio Exterior",

    "Agricultura, Ganadería y Agroindustria",

    "Arquitectura, Diseño de Interiores y Decoración",

    "Comercial, Ventas y Desarrollo de Negocios",

    "Construcción e Ingeniería Civil",

    "Diseño y Artes Gráficas",

    "Gastronomía, Hotelería y Turismo",

    "Legal y Cumplimiento",

    "Logística, Abastecimiento y Transporte",

    "Mantenimiento y Reparaciones Técnicas",

    "Marketing, Publicidad y Comunicación",

    "Minería, Petróleo, Energía y Gas",

    "Producción, Manufactura y Operaciones",

    "Recursos Humanos y Capacitación",

    "Salud, Medicina y Farmacia",

    "Tecnología, Sistemas y Telecomunicaciones",

    "Otros",
]


if "professionalArea" not in jobs.columns:

    jobs["professionalArea"] = "Otros"


jobs["professionalArea"] = (
    jobs["professionalArea"]
    .fillna("Otros")
    .astype(str)
    .str.strip()
)


jobs.loc[
    ~jobs["professionalArea"].isin(
        areas_profesionales
    ),
    "professionalArea",
] = "Otros"


# ============================================================
# PREPARAR TIPO DE OFERTA
# ============================================================

if "isExternalOffer" not in jobs.columns:

    jobs["isExternalOffer"] = pd.NA


def clasificar_tipo_oferta(
    valor,
):

    if pd.isna(valor):

        return "No definido"

    if isinstance(valor, bool):

        if valor:

            return "Externas"

        return "Internas"

    valor_texto = str(valor).strip().lower()

    if valor_texto in [
        "true",
        "1",
        "1.0",
        "si",
        "sí",
        "yes",
    ]:

        return "Externas"

    if valor_texto in [
        "false",
        "0",
        "0.0",
        "no",
    ]:

        return "Internas"

    return "No definido"


jobs["tipo_oferta"] = (
    jobs["isExternalOffer"]
    .apply(clasificar_tipo_oferta)
)


# ============================================================
# RANGO DE FECHAS DISPONIBLE
# ============================================================

fecha_min = jobs["createdAt"].min()

fecha_max = jobs["createdAt"].max()


if pd.isna(fecha_min) or pd.isna(fecha_max):

    st.error(
        "No existen fechas válidas en las ofertas laborales."
    )

    st.stop()


# ============================================================
# CALLBACK PARA ACTUALIZAR LAS FECHAS SEGÚN EL PERÍODO
# ============================================================

def actualizar_periodo():

    periodo_actual = st.session_state[
        "filtro_periodo"
    ]

    if periodo_actual == "Últimos 7 días":

        fecha_inicio = (
            fecha_max
            - pd.Timedelta(days=7)
        )

    elif periodo_actual == "Últimos 30 días":

        fecha_inicio = (
            fecha_max
            - pd.Timedelta(days=30)
        )

    elif periodo_actual == "Últimos 3 meses":

        fecha_inicio = (
            fecha_max
            - pd.DateOffset(months=3)
        )

    elif periodo_actual == "Último año":

        fecha_inicio = (
            fecha_max
            - pd.DateOffset(years=1)
        )

    else:

        fecha_inicio = fecha_min

    fecha_inicio = max(
        fecha_inicio,
        fecha_min,
    )

    st.session_state[
        "filtro_fecha_inicio"
    ] = fecha_inicio.date()

    st.session_state[
        "filtro_fecha_fin"
    ] = fecha_max.date()


# ============================================================
# CALLBACK LIMPIAR FILTROS
# ============================================================

def limpiar_filtros():

    st.session_state[
        "filtro_area"
    ] = "Todas"

    st.session_state[
        "filtro_tipo_oferta"
    ] = "Todas"

    st.session_state[
        "filtro_periodo"
    ] = "Completo"

    st.session_state[
        "filtro_fecha_inicio"
    ] = fecha_min.date()

    st.session_state[
        "filtro_fecha_fin"
    ] = fecha_max.date()


# ============================================================
# INICIALIZAR FILTROS EN SESSION STATE
# ============================================================

if "filtro_area" not in st.session_state:

    st.session_state[
        "filtro_area"
    ] = "Todas"


if "filtro_tipo_oferta" not in st.session_state:

    st.session_state[
        "filtro_tipo_oferta"
    ] = "Todas"


if "filtro_periodo" not in st.session_state:

    st.session_state[
        "filtro_periodo"
    ] = "Completo"


if "filtro_fecha_inicio" not in st.session_state:

    st.session_state[
        "filtro_fecha_inicio"
    ] = fecha_min.date()


if "filtro_fecha_fin" not in st.session_state:

    st.session_state[
        "filtro_fecha_fin"
    ] = fecha_max.date()

# ============================================================
# FILTROS SIDEBAR
# ============================================================

with st.sidebar:

    # ========================================================
    # FILTRO ÁREA
    # ========================================================

    st.markdown(
        '<div class="filter-label">Área</div>',
        unsafe_allow_html=True,
    )

    area_seleccionada = st.selectbox(
        "Área",
        ["Todas"] + areas_profesionales,
        label_visibility="collapsed",
        key="filtro_area",
    )


    # ========================================================
    # FILTRO TIPO DE OFERTA
    # ========================================================

    st.markdown(
        '<div class="filter-label">Tipo de oferta</div>',
        unsafe_allow_html=True,
    )

    tipo_oferta = st.selectbox(
        "Tipo de oferta",
        [
            "Todas",
            "Internas",
            "Externas",
            "No definido",
        ],
        label_visibility="collapsed",
        key="filtro_tipo_oferta",
    )


    # ========================================================
    # FILTRO PERÍODO
    # ========================================================

    st.markdown(
        '<div class="date-section-title">Período</div>',
        unsafe_allow_html=True,
    )

    periodo = st.radio(
    "Período",
    [
        "Últimos 7 días",
        "Últimos 30 días",
        "Últimos 3 meses",
        "Último año",
        "Completo",
    ],
    label_visibility="collapsed",
    key="filtro_periodo",
    on_change=actualizar_periodo,
)


    # ========================================================
    # FECHAS
    # ========================================================

    st.markdown(
        '<div class="date-section-title">'
        "Seleccionar fechas"
        "</div>",
        unsafe_allow_html=True,
    )

    col_fecha1, col_fecha2 = st.columns(
        2,
        gap="small",
    )

    with col_fecha1:

        fecha_inicio = st.date_input(
            "Fecha inicio",
            min_value=fecha_min.date(),
            max_value=fecha_max.date(),
            format="DD/MM/YYYY",
            key="filtro_fecha_inicio",
        )

    with col_fecha2:

        fecha_fin = st.date_input(
            "Fecha fin",
            min_value=fecha_min.date(),
            max_value=fecha_max.date(),
            format="DD/MM/YYYY",
            key="filtro_fecha_fin",
        )


    # ========================================================
    # BOTONES
    # ========================================================

    st.markdown("---")


    if st.button(
        "Limpiar filtros",
        use_container_width=True,
        key="btn_limpiar_filtros",
        on_click=limpiar_filtros,
    ):

        st.rerun()


    if st.button(
        "Forzar recarga de datos",
        use_container_width=True,
        key="btn_recargar",
    ):

        st.cache_data.clear()

        st.rerun()


# ============================================================
# VALIDACIÓN DE FECHAS
# ============================================================

if fecha_inicio > fecha_fin:

    st.sidebar.error(
        "La fecha inicial no puede ser posterior "
        "a la fecha final."
    )

    st.stop()


# ============================================================
# TIMESTAMPS
# ============================================================

fecha_inicio_ts = pd.Timestamp(
    fecha_inicio
)

fecha_fin_ts = (
    pd.Timestamp(fecha_fin)
    + pd.Timedelta(days=1)
    - pd.Timedelta(seconds=1)
)


# ============================================================
# FILTRO PRINCIPAL POR FECHAS
# ============================================================

jobs_filtrados = jobs[
    (
        jobs["createdAt"]
        >= fecha_inicio_ts
    )
    &
    (
        jobs["createdAt"]
        <= fecha_fin_ts
    )
].copy()


# ============================================================
# FILTRO POR ÁREA
# ============================================================

if area_seleccionada != "Todas":

    jobs_filtrados = jobs_filtrados[
        jobs_filtrados[
            "professionalArea"
        ]
        == area_seleccionada
    ].copy()


# ============================================================
# FILTRO POR TIPO DE OFERTA
# ============================================================

if tipo_oferta != "Todas":

    jobs_filtrados = jobs_filtrados[
        jobs_filtrados[
            "tipo_oferta"
        ]
        == tipo_oferta
    ].copy()


# ============================================================
# IDS DE OFERTAS FILTRADAS
# ============================================================

ids_jobs_filtrados = set(
    normalizar_id(
        jobs_filtrados["_id"]
    )
)


# ============================================================
# POSTULACIONES
# ============================================================

if "_id_job" in applications_jobs_df.columns:

    aplicaciones_ids = normalizar_id(
        applications_jobs_df[
            "_id_job"
        ]
    )

    applications_filtradas = (
        applications_jobs_df[
            aplicaciones_ids.isin(
                ids_jobs_filtrados
            )
        ].copy()
    )

else:

    applications_filtradas = pd.DataFrame()


# ============================================================
# KPIs
# ============================================================

# ============================================================
# TOTAL DE OFERTAS
# ============================================================

total_empleos = len(
    jobs_filtrados
)


# ============================================================
# TOTAL DE POSTULACIONES
# ============================================================

total_postulaciones = len(
    applications_filtradas
)


# ============================================================
# PROMEDIO DE POSTULACIONES POR OFERTA
# ============================================================

if total_empleos > 0:

    promedio_postulaciones_oferta = (
        total_postulaciones
        / total_empleos
    )

else:

    promedio_postulaciones_oferta = 0


# ============================================================
# TOTAL DE EMPRESAS REGISTRADAS
# ============================================================

# IMPORTANTE:
# NO usamos companies["_id"].nunique()
# porque eso cuenta documentos/IDs y puede generar
# valores como 687 aunque existan muchas empresas
# repetidas con nombres diferentes.
# ============================================================
# TOTAL DE EMPRESAS REGISTRADAS
# ============================================================

if not companies.empty:

    if "_id" in companies.columns:

        total_empresas = (
            companies["_id"]
            .dropna()
            .astype(str)
            .str.strip()
            .replace("", pd.NA)
            .dropna()
            .nunique()
        )

    else:

        total_empresas = len(companies)

else:

    total_empresas = 0
    
# ============================================================
# TÍTULO
# ============================================================

st.title(
    "Dashboard de Empresas"
)


st.markdown(
    """
    <div class="dashboard-subtitle">
        Laboral.ai — Análisis de ofertas laborales y postulaciones
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# RESUMEN GENERAL
# ============================================================

st.markdown(
    "## Resumen general"
)


st.markdown(
    """
    <div class="section-caption">
        Indicadores principales de la vista seleccionada
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# KPI
# ============================================================

col1, col2, col3 = st.columns(
    3,
    gap="medium",
)


with col1:

    st.metric(
        label="Total de empresas registradas",
        value=f"{total_empresas:,}",
    )


with col2:

    st.metric(
        label="Total de ofertas laborales",
        value=f"{total_empleos:,}",
    )


with col3:

    st.metric(
        label="Total de postulaciones",
        value=f"{total_postulaciones:,}",
    )


# ============================================================
# OFERTAS LABORALES
# ============================================================

st.markdown("---")


st.markdown(
    "## Análisis de ofertas laborales"
)


st.markdown(
    """
    <div class="section-caption">
        Distribución de las ofertas según sus principales características
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FILA 1
# ============================================================

col_graf1, col_graf2 = st.columns(
    2,
    gap="large",
    vertical_alignment="top",
)


# ============================================================
# OFERTAS POR ÁREA
# ============================================================

with col_graf1:

    with st.container(
        border=True
    ):

        tarjeta_grafico(
            "Cantidad de ofertas laborales por área profesional",
            "Distribución de las ofertas según el área profesional",
        )

        if not jobs_filtrados.empty:

            ofertas_por_area = (
                jobs_filtrados[
                    "professionalArea"
                ]
                .value_counts()
                .reindex(
                    areas_profesionales,
                    fill_value=0,
                )
                .reset_index()
            )

            ofertas_por_area.columns = [
                "area",
                "cantidad",
            ]

            ofertas_por_area = (
                ofertas_por_area[
                    ofertas_por_area[
                        "cantidad"
                    ] > 0
                ]
                .sort_values(
                    "cantidad",
                    ascending=True,
                )
            )

            fig = grafico_barras(
                ofertas_por_area,
                x="area",
                y="cantidad",
                horizontal=True,
                altura=470,
                color=VERDE_BARRA,
            )

            if fig is not None:

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                    },
                )

        else:

            st.info(
                "No hay información para "
                "los filtros seleccionados."
            )


# ============================================================
# EMPRESAS CON MÁS OFERTAS
# ============================================================

with col_graf2:

    with st.container(
        border=True
    ):

        tarjeta_grafico(
            "Empresas con mayor cantidad de ofertas laborales",
            "Top 10 de empresas según cantidad de ofertas laborales",
        )

        empresas_base = jobs_filtrados.copy()


        # ====================================================
        # OFERTAS EXTERNAS
        # ====================================================

        externas = empresas_base[
            empresas_base[
                "tipo_oferta"
            ] == "Externas"
        ].copy()


        if (
            not externas.empty
            and
            "externalCompanyName"
            in externas.columns
        ):

            externas["empresa"] = (
                externas[
                    "externalCompanyName"
                ]
                .apply(normalizar_empresa)
            )

        else:

            externas["empresa"] = ""


        # ====================================================
        # OFERTAS INTERNAS
        # ====================================================

        internas = empresas_base[
            empresas_base[
                "tipo_oferta"
            ] == "Internas"
        ].copy()


        if (
            not internas.empty
            and "companyId"
            in internas.columns
            and "_id"
            in companies.columns
            and "businessName"
            in companies.columns
        ):

            empresas_internas_df = internas.merge(
                companies[
                    [
                        "_id",
                        "businessName",
                    ]
                ],
                left_on="companyId",
                right_on="_id",
                how="left",
            )

            empresas_internas_df["empresa"] = (
                empresas_internas_df[
                    "businessName"
                ]
                .apply(normalizar_empresa)
            )

        else:

            empresas_internas_df = internas.copy()

            empresas_internas_df["empresa"] = ""


        # ====================================================
        # UNIR EMPRESAS
        # ====================================================

        empresas_grafico = pd.concat(
            [
                externas[
                    ["empresa"]
                ],
                empresas_internas_df[
                    ["empresa"]
                ],
            ],
            ignore_index=True,
        )


        empresas_grafico["empresa"] = (
            empresas_grafico[
                "empresa"
            ]
            .fillna("")
            .astype(str)
            .str.strip()
        )


        # ====================================================
        # ELIMINAR EMPRESAS VACÍAS
        # ====================================================

        empresas_grafico = empresas_grafico[
            empresas_grafico[
                "empresa"
            ] != ""
        ].copy()


        empresas_grafico = empresas_grafico[
            ~empresas_grafico[
                "empresa"
            ].str.lower().isin(
                [
                    "nan",
                    "none",
                    "null",
                    "na",
                    "n a",
                    "n/a",
                ]
            )
        ].copy()


        # ====================================================
        # RANKING
        # ====================================================

        if not empresas_grafico.empty:

            ranking_empresas = (
                empresas_grafico
                .groupby(
                    "empresa",
                    as_index=False,
                )
                .size()
            )

            ranking_empresas = (
                ranking_empresas
                .rename(
                    columns={
                        "size": "cantidad"
                    }
                )
                .sort_values(
                    "cantidad",
                    ascending=False,
                )
                .head(10)
            )

            ranking_empresas = (
                ranking_empresas
                .sort_values(
                    "cantidad",
                    ascending=True,
                )
            )


            fig = grafico_barras(
                ranking_empresas,
                x="empresa",
                y="cantidad",
                horizontal=True,
                altura=470,
                color=CELESTE_BARRA,
            )


            if fig is not None:

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                    },
                )

        else:

            st.info(
                "No hay información de empresas "
                "para los filtros seleccionados."
            )


# ============================================================
# MAPA + TIPO DE PUESTO
# ============================================================

st.markdown("")


col_mapa, col_jobtype = st.columns(
    [1.55, 1],
    gap="large",
    vertical_alignment="top",
)


# ============================================================
# MAPA DE OFERTAS POR DEPARTAMENTO
# ============================================================

with col_mapa:

    with st.container(
        border=True
    ):

        tarjeta_grafico(
            "Cantidad de ofertas laborales por departamento",
            "Distribución geográfica de las ofertas laborales en el Perú",
        )

        if "geographicDepartment" in jobs_filtrados.columns:

            ofertas_departamento = (
                jobs_filtrados[
                    "geographicDepartment"
                ]
                .fillna(
                    "SIN DEPARTAMENTO"
                )
                .astype(str)
                .str.strip()
            )

            departamentos_df = pd.DataFrame(
                {
                    "Departamento_original":
                        ofertas_departamento
                }
            )

            departamentos_df[
                "Departamento"
            ] = departamentos_df[
                "Departamento_original"
            ].apply(
                normalizar_texto
            )

            departamentos_df = (
                departamentos_df
                .groupby(
                    "Departamento"
                )
                .size()
                .reset_index(
                    name="Cantidad"
                )
            )

            try:

                geojson_peru = (
                    cargar_geojson_peru()
                )

                for feature in geojson_peru[
                    "features"
                ]:

                    properties = feature.get(
                        "properties",
                        {}
                    )

                    nombre_departamento = (
                        properties.get(
                            "NOMBDEP",
                            ""
                        )
                    )

                    properties[
                        "DEPARTAMENTO_NORMALIZADO"
                    ] = normalizar_texto(
                        nombre_departamento
                    )

                mapa_departamentos = pd.DataFrame(
                    {
                        "Departamento":
                            [
                                feature[
                                    "properties"
                                ].get(
                                    "DEPARTAMENTO_NORMALIZADO",
                                    ""
                                )

                                for feature
                                in geojson_peru[
                                    "features"
                                ]
                            ]
                    }
                )

                mapa_departamentos = (
                    mapa_departamentos
                    .drop_duplicates()
                    .merge(
                        departamentos_df,
                        on="Departamento",
                        how="left",
                    )
                )

                mapa_departamentos[
                    "Cantidad"
                ] = (
                    mapa_departamentos[
                        "Cantidad"
                    ]
                    .fillna(0)
                    .astype(int)
                )

                fig_mapa = px.choropleth(
                    mapa_departamentos,
                    geojson=geojson_peru,
                    locations="Departamento",
                    featureidkey=(
                        "properties."
                        "DEPARTAMENTO_NORMALIZADO"
                    ),
                    color="Cantidad",
                    color_continuous_scale=[
                        [
                            0.00,
                            "#EEF2F6",
                        ],
                        [
                            0.15,
                            "#D7E0E9",
                        ],
                        [
                            0.40,
                            "#A8B9CA",
                        ],
                        [
                            0.70,
                            "#5C7895",
                        ],
                        [
                            1.00,
                            "#0A223C",
                        ],
                    ],
                    hover_name="Departamento",
                    hover_data={
                        "Cantidad": True,
                        "Departamento": False,
                    },
                )

                fig_mapa.update_traces(
                    marker_line_color="#FFFFFF",
                    marker_line_width=1.2,
                    hovertemplate=(
                        "<b>%{hovertext}</b><br>"
                        "Ofertas: "
                        "<b>%{z}</b>"
                        "<extra></extra>"
                    ),
                )

                fig_mapa.update_geos(
                    fitbounds="geojson",
                    visible=False,
                    showcountries=False,
                    showcoastlines=False,
                    showland=False,
                    showframe=False,
                    bgcolor="rgba(0,0,0,0)",
                )

                fig_mapa.update_layout(

                    height=560,

                    paper_bgcolor="rgba(0,0,0,0)",

                    plot_bgcolor="rgba(0,0,0,0)",

                    margin=dict(
                        l=0,
                        r=0,
                        t=55,
                        b=0,
                    ),

                    coloraxis_colorbar=dict(

                        title="Ofertas",

                        orientation="h",

                        x=0.5,

                        xanchor="center",

                        y=1.02,

                        yanchor="bottom",

                        len=0.72,

                        thickness=12,

                        bgcolor=(
                            "rgba("
                            "255,255,255,0.90)"
                        ),

                        bordercolor="#E2E6EB",

                        borderwidth=1,

                        tickfont=dict(
                            size=10,
                            color="#59636F",
                        ),

                        title_font=dict(
                            size=11,
                            color="#59636F",
                        ),

                        outlinewidth=0,

                        ticks="outside",

                        ticklen=4,
                    ),
                )

                st.plotly_chart(
                    fig_mapa,
                    use_container_width=True,
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                        "scrollZoom": False,
                    },
                )

            except Exception as e:

                st.warning(
                    "No se pudo cargar el mapa "
                    "departamental del Perú."
                )

                st.caption(
                    f"Detalle técnico: {e}"
                )

        else:

            st.info(
                "No existe la columna "
                "'geographicDepartment' "
                "en los datos de ofertas."
            )


# ============================================================
# OFERTAS POR TIPO DE PUESTO
# ============================================================

with col_jobtype:

    with st.container(
        border=True
    ):

        tarjeta_grafico(
            "Cantidad de ofertas laborales por tipo de puesto",
            "Distribución de las ofertas según el nivel o tipo de puesto",
        )

        if "jobType" in jobs_filtrados.columns:

            jobtype_df = jobs_filtrados[
                ["jobType"]
            ].copy()

            jobtype_df["jobType"] = (
                jobtype_df["jobType"]
                .fillna("Sin especificar")
                .astype(str)
                .str.strip()
            )

            jobtype_df.loc[
                jobtype_df["jobType"] == "",
                "jobType"
            ] = "Sin especificar"

            jobtype_grafico = (
                jobtype_df[
                    "jobType"
                ]
                .value_counts()
                .reset_index()
            )

            jobtype_grafico.columns = [
                "Tipo de puesto",
                "Cantidad",
            ]

            jobtype_grafico = (
                jobtype_grafico
                .sort_values(
                    "Cantidad",
                    ascending=True,
                )
            )

            fig_jobtype = grafico_barras(
                jobtype_grafico,
                x="Tipo de puesto",
                y="Cantidad",
                horizontal=True,
                altura=560,
                color=MORADO_BARRA,
            )

            if fig_jobtype is not None:

                st.plotly_chart(
                    fig_jobtype,
                    use_container_width=True,
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                    },
                )

        else:

            st.info(
                "No existe la columna "
                "'jobType' "
                "en los datos de ofertas."
            )


# ============================================================
# FILA 2
# ============================================================

col_graf3, col_graf4 = st.columns(
    2,
    gap="large",
    vertical_alignment="top",
)


# ============================================================
# MODALIDAD
# ============================================================

with col_graf3:

    with st.container(
        border=True
    ):

        tarjeta_grafico(
            "Distribución de ofertas laborales por modalidad",
            "Distribución de ofertas laborales por modalidad de trabajo",
        )

        if "modality" in jobs_filtrados.columns:

            ofertas_modalidad_grafico = (
                jobs_filtrados[
                    "modality"
                ]
                .fillna(
                    "Sin especificar"
                )
                .astype(str)
                .str.strip()
                .value_counts()
                .reset_index()
            )

            ofertas_modalidad_grafico.columns = [
                "Modalidad",
                "Cantidad",
            ]

            ofertas_modalidad_grafico.loc[
                ofertas_modalidad_grafico[
                    "Modalidad"
                ] == "",
                "Modalidad"
            ] = "Sin especificar"

            fig = px.pie(
                ofertas_modalidad_grafico,
                names="Modalidad",
                values="Cantidad",
                title="",
                hole=0.45,
                color_discrete_sequence=[
                    "#0A99AC",
                    "#087F8F",
                    "#66C7D1",
                    "#A6C263",
                ],
            )

            fig.update_traces(
                textinfo="label+percent",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Ofertas: %{value}<br>"
                    "Porcentaje: %{percent}"
                    "<extra></extra>"
                ),
            )

            fig.update_layout(
                height=350,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(
                    l=10,
                    r=10,
                    t=5,
                    b=10,
                ),
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02,
                    font=dict(
                        size=10,
                        color="#59636F",
                    ),
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

        else:

            st.info(
                "No existe información "
                "de modalidad."
            )


# ============================================================
# ESTADOS POSTULACIONES
# ============================================================

with col_graf4:

    with st.container(
        border=True
    ):

        tarjeta_grafico(
            "Cantidad de postulaciones por estado",
            "Estado de las postulaciones asociadas "
            "a las ofertas filtradas",
        )

        if (
            not applications_filtradas.empty
            and
            "applicationStatus"
            in applications_filtradas.columns
        ):

            estados = (
                contar_categorias(
                    applications_filtradas,
                    "applicationStatus",
                    etiqueta_nulos="SIN_ESTADO",
                )
                .reset_index()
            )

            estados.columns = [
                "estado",
                "cantidad",
            ]

            estados = (
                estados
                .sort_values(
                    "cantidad",
                    ascending=True,
                )
            )

            fig = grafico_barras(
                estados,
                x="estado",
                y="cantidad",
                horizontal=True,
                altura=350,
                color=AMARILLO_BARRA,
            )

            if fig is not None:

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                    },
                )

        else:

            st.info(
                "No existen postulaciones "
                "para los filtros seleccionados."
            )


# ============================================================
# EVOLUCIÓN TEMPORAL
# ============================================================

st.markdown("---")


st.markdown(
    "## Evolución de ofertas y postulaciones"
)


st.markdown(
    """
    <div class="section-caption">
        Comportamiento mensual de las ofertas laborales
        y postulaciones
    </div>
    """,
    unsafe_allow_html=True,
)


col_tiempo1, col_tiempo2 = st.columns(
    2,
    gap="large",
    vertical_alignment="top",
)


# ============================================================
# EVOLUCIÓN OFERTAS
# ============================================================

with col_tiempo1:

    with st.container(
        border=True
    ):

        tarjeta_grafico(
            "Evolución de ofertas laborales",
            "Cantidad de ofertas laborales creadas por mes",
        )

        if not jobs_filtrados.empty:

            ofertas_mes = (
                contar_por_mes(
                    jobs_filtrados,
                    "createdAt",
                )
                .reset_index()
            )

            ofertas_mes.columns = [
                "mes",
                "cantidad",
            ]

            ofertas_mes["mes"] = (
                ofertas_mes["mes"]
                .astype(str)
            )

            fig = grafico_linea(
                ofertas_mes,
                x="mes",
                y="cantidad",
                altura=350,
                color=AZUL_LINEA,
            )

            if fig is not None:

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={
                        "displayModeBar": False,
                        "responsive": True,
                    },
                )

        else:

            st.info(
                "No existen ofertas "
                "para mostrar."
            )


# ============================================================
# EVOLUCIÓN POSTULACIONES
# ============================================================

with col_tiempo2:

    with st.container(
        border=True
    ):

        tarjeta_grafico(
            "Evolución de postulaciones",
            "Cantidad de postulaciones creadas por mes",
        )

        if not applications_filtradas.empty:

            columnas_fecha_postulacion = [

                "createdAt_application",

                "createdAt",

                "created_at",

                "createdAtApplication",
            ]

            columna_fecha = next(
                (
                    columna
                    for columna
                    in columnas_fecha_postulacion
                    if columna
                    in applications_filtradas.columns
                ),
                None,
            )

            if columna_fecha:

                aplicaciones_temp = (
                    applications_filtradas.copy()
                )

                aplicaciones_temp[
                    columna_fecha
                ] = pd.to_datetime(
                    aplicaciones_temp[
                        columna_fecha
                    ],
                    errors="coerce",
                )

                aplicaciones_temp = (
                    aplicaciones_temp
                    .dropna(
                        subset=[
                            columna_fecha
                        ]
                    )
                )

                if not aplicaciones_temp.empty:

                    postulaciones_mes = (
                        contar_por_mes(
                            aplicaciones_temp,
                            columna_fecha,
                        )
                        .reset_index()
                    )

                    postulaciones_mes.columns = [
                        "mes",
                        "cantidad",
                    ]

                    postulaciones_mes["mes"] = (
                        postulaciones_mes[
                            "mes"
                        ]
                        .astype(str)
                    )

                    fig = grafico_linea(
                        postulaciones_mes,
                        x="mes",
                        y="cantidad",
                        altura=350,
                        color=AZUL_LINEA,
                    )

                    if fig is not None:

                        st.plotly_chart(
                            fig,
                            use_container_width=True,
                            config={
                                "displayModeBar": False,
                                "responsive": True,
                            },
                        )

                else:

                    st.info(
                        "No existen fechas válidas "
                        "de postulaciones."
                    )

            else:

                st.info(
                    "No se encontró una columna "
                    "de fecha para las postulaciones."
                )

        else:

            st.info(
                "No existen postulaciones "
                "para mostrar."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")


st.markdown(
    """
    <div style="
        text-align:center;
        color:#9AA1AA;
        font-size:0.76rem;
        padding:0.6rem 0 1.2rem 0;
    ">
        Dashboard de Empresas · Laboral.ai
    </div>
    """,
    unsafe_allow_html=True,
)