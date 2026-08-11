# ============================================================
# 0. IMPORTACIÓN DE LIBRERÍAS
# ============================================================

import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# 1. CARGA DE DATOS DESDE MONGODB
# ============================================================

def constructor():

    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("DB_NAME")]

    # --------------------------------------------------------
    # Columnas necesarias de companies
    # --------------------------------------------------------

    companies_columns = [
        "_id",
        "businessName",
        "industry",
        "verificationStatus",
        "country",
        "plan",
        "isActive",
        "createdAt"
    ]

    # --------------------------------------------------------
    # Columnas necesarias de jobs
    # --------------------------------------------------------

    jobs_columns = [
        "_id",
        "companyId",
        "title",
        "department",
        "modality",
        "publishUntil",
        "status",
        "createdAt",
        "country",
        "geographicDepartment",
        "jobType",
        "verificationStatus",
        "isExternalOffer",
        "externalCompanyName"
    ]

    # --------------------------------------------------------
    # Columnas necesarias de applications
    # --------------------------------------------------------

    applications_columns = [
        "_id",
        "job",
        "createdAt",
        "applicationStatus"
    ]

    # --------------------------------------------------------
    # Obtener datos desde MongoDB
    # --------------------------------------------------------

    companies = pd.DataFrame(
        db["companies"].find(
            {},
            {column: 1 for column in companies_columns}
        )
    )

    jobs = pd.DataFrame(
        db["jobs"].find(
            {},
            {column: 1 for column in jobs_columns}
        )
    )

    applications = pd.DataFrame(
        db["applications"].find(
            {},
            {column: 1 for column in applications_columns}
        )
    )

    return companies, jobs, applications


companies, jobs, applications = constructor()


# ============================================================
# 2. LIMPIEZA DE DATOS
# ============================================================


# ============================================================
# 2.1 LIMPIEZA DE COMPANIES
# ============================================================

companies_clean = companies.copy()

# ------------------------------------------------------------
# Limpiar columnas de texto
# ------------------------------------------------------------

columnas_texto_companies = [
    "businessName",
    "industry",
    "verificationStatus",
    "country"
]

for col in columnas_texto_companies:

    companies_clean[col] = (
        companies_clean[col]
        .astype("string")
        .str.strip()
    )


# ------------------------------------------------------------
# Limpiar país
# ------------------------------------------------------------

companies_clean["country"] = companies_clean["country"].replace({
    "Peru": "Perú"
})


# ------------------------------------------------------------
# Extraer tipo de plan
# ------------------------------------------------------------

companies_clean["planType"] = companies_clean["plan"].apply(
    lambda x: x.get("type") if isinstance(x, dict) else None
)

companies_clean["planType"] = (
    companies_clean["planType"]
    .replace({"None": "NONE"})
    .fillna("NONE")
)


# ============================================================
# 2.2 LIMPIEZA DE JOBS
# ============================================================

jobs_clean = jobs.copy()

# ------------------------------------------------------------
# Limpiar columnas de texto
# ------------------------------------------------------------

columnas_texto_jobs = [
    "title",
    "department",
    "modality",
    "status",
    "country",
    "geographicDepartment",
    "jobType",
    "verificationStatus",
    "externalCompanyName"
]

for col in columnas_texto_jobs:

    jobs_clean[col] = (
        jobs_clean[col]
        .astype("string")
        .str.strip()
    )


# ------------------------------------------------------------
# Estandarizar modalidad
# ------------------------------------------------------------

jobs_clean["modality"] = jobs_clean["modality"].replace({
    "hibrido": "híbrido"
})


# ------------------------------------------------------------
# Estandarizar país
# ------------------------------------------------------------

jobs_clean["country"] = jobs_clean["country"].replace({
    "Peru": "Perú"
})


# ------------------------------------------------------------
# Tratar valores vacíos en country
# ------------------------------------------------------------

jobs_clean["country"] = jobs_clean["country"].replace(
    r"^\s*$",
    pd.NA,
    regex=True
)


# ------------------------------------------------------------
# Limpiar geographicDepartment
# ------------------------------------------------------------

jobs_clean["geographicDepartment"] = (
    jobs_clean["geographicDepartment"]
    .astype("string")
    .str.strip()
    .replace({
        "5": pd.NA,
        "": pd.NA
    })
)


# ------------------------------------------------------------
# Eliminar valores inválidos de department
# ------------------------------------------------------------

valores_invalidos = [
    "test",
    "prueba",
    "Test de departamento",
    "Test de Funcionalidades",
    "fghjklñ",
    "Lima"
]

jobs_clean["department"] = jobs_clean["department"].replace(
    valores_invalidos,
    pd.NA
)


# ------------------------------------------------------------
# Correcciones de escritura en department
# ------------------------------------------------------------

correcciones_department = {

    "Comercia":
        "Comercial",

    "Contabilidad y Finanzasc":
        "Contabilidad y Finanzas",

    "Auditoria":
        "Auditoría",

    "Psicologia":
        "Psicología",

    "Tecnologia":
        "Tecnología",

    "Tecnologia / Sistemas":
        "Tecnología / Sistemas",

    "Tecnologia / TI":
        "Tecnología / TI",

    "Tecnologia /Soporte Técnico":
        "Tecnología / Soporte Técnico",

    "Tecnologia / TI , Soporte Técnico":
        "Tecnología / TI, Soporte Técnico",

    "Comunicaciónes":
        "Comunicaciones",

    "Comunicacion":
        "Comunicación",

    "Diseño Grafico":
        "Diseño Gráfico",

    "Diseño gráfico":
        "Diseño Gráfico",

    "Mineria":
        "Minería",

    "Atención al cliente":
        "Atención al Cliente",

    "Trabajo social":
        "Trabajo Social",

    "Administración y Finanzas.":
        "Administración y Finanzas",

    "Administración y Oficina.":
        "Administración y Oficina",

    "Logística y Cadena de Suministro.":
        "Logística y Cadena de Suministro",

    "Tecnología e Innovación.":
        "Tecnología e Innovación",

    "Seguridad Industrial / SSOMA.":
        "Seguridad Industrial / SSOMA",

    "Ingeniería Industrial y Operaciones.":
        "Ingeniería Industrial y Operaciones",

    "Electricidad Industrial, Electrotecnia o Electricidad.":
        "Electricidad Industrial, Electrotecnia o Electricidad",

    "Energía y Electricidad.":
        "Energía y Electricidad",

    "Mantenimiento Eléctrico Industrial":
        "Mantenimiento Eléctrico Industrial"
}

jobs_clean["department"] = jobs_clean["department"].replace(
    correcciones_department
)


# ------------------------------------------------------------
# Convertir fechas
# ------------------------------------------------------------

jobs_clean["createdAt"] = pd.to_datetime(
    jobs_clean["createdAt"],
    errors="coerce"
)

jobs_clean["publishUntil"] = pd.to_datetime(
    jobs_clean["publishUntil"],
    errors="coerce"
)


# ------------------------------------------------------------
# Eliminar únicamente inconsistencias temporales
#
# publishUntil no puede ser anterior a createdAt.
#
# Los registros donde alguna fecha esté vacía NO se eliminan.
# ------------------------------------------------------------

fechas_invalidas = (
    jobs_clean["publishUntil"].notna()
    & jobs_clean["createdAt"].notna()
    & (jobs_clean["publishUntil"] < jobs_clean["createdAt"])
)

jobs_clean = jobs_clean.loc[~fechas_invalidas].copy()

jobs_clean.reset_index(drop=True, inplace=True)


# ============================================================
# 2.3 LIMPIEZA DE APPLICATIONS
# ============================================================

applications_clean = applications.copy()

applications_clean["applicationStatus"] = (
    applications_clean["applicationStatus"]
    .fillna("SIN_ESTADO")
)


# ============================================================
# 3. ESTANDARIZACIÓN DE NOMBRES DE EMPRESAS
# ============================================================
#
# Esta parte corresponde específicamente al trabajo de
# empresas.
#
# Se utiliza externalCompanyName de jobs.
#
# El objetivo es agrupar diferentes formas de escribir una
# misma empresa bajo un único nombre estandarizado.
#
# NO se realiza ninguna relación entre colecciones.
# ============================================================


estandarizacion_empresas = {

    # ========================================================
    # EMPRESAS NO IDENTIFICADAS
    # ========================================================

    "Importante empresa del sector":
        "Importante Empresa en el sector",

    "Importante Empresa en el sector":
        "Importante Empresa en el sector",

    "Importante del Sector":
        "Importante Empresa en el sector",

    "Importante":
        "Importante Empresa en el sector",

    "Empresa importante en el sector":
        "Importante Empresa en el sector",

    "Empresa Confidencial":
        "Importante Empresa en el sector",

    "Confidencial":
        "Importante Empresa en el sector",


    # ========================================================
    # GLORIA
    # ========================================================

    "Gloria":
        "Grupo Gloria",

    "Gloria S.A":
        "Grupo Gloria",

    "Gloria S.A.":
        "Grupo Gloria",


    # ========================================================
    # KOMATSU MITSUI
    # ========================================================

    "KOMATSU - MITSUI MAQUINARIAS":
        "Komatsu Mitsui",

    "KOMATSU MITSUI":
        "Komatsu Mitsui",


    # ========================================================
    # CAJA TRUJILLO
    # ========================================================

    "CAJA TRUJILLO":
        "Caja Trujillo",


    # ========================================================
    # REPSOL
    # ========================================================

    "REPSOL":
        "Repsol",


    # ========================================================
    # CAMPOSOL
    # ========================================================

    "CAMPOSOL":
        "Camposol",

    "CAMPOSOL S.A.":
        "Camposol",


    # ========================================================
    # EUROFIRMS
    # ========================================================

    "EUROFIRMS":
        "Eurofirms",

    "Eurofirms Perú":
        "Eurofirms",


    # ========================================================
    # UTP
    # ========================================================

    "UNIVERSIDAD TECNOLOGICA DEL PERU":
        "Universidad Tecnológica del Perú",

    "UNIVERSIDAD TECNOLOGICA DEL PERU(UTP)":
        "Universidad Tecnológica del Perú",


    # ========================================================
    # CAJA CUSCO
    # ========================================================

    "CAJA CUSCO":
        "Caja Cusco",


    # ========================================================
    # CARTAVIO
    # ========================================================

    "Cartavio Rum Company":
        "CARTAVIO RUM COMPANY S.A.C.",


    # ========================================================
    # ADECCO
    # ========================================================

    "Adecco Perú":
        "Adecco Perú S.A.",

    "Adecco Perú S.A.SAC":
        "Adecco Perú S.A.",

    "ADECCO BCP":
        "Adecco Perú S.A.",

    "Practicante Profesional de Contabilidad Adecco Perú S.A.":
        "Adecco Perú S.A.",


    # ========================================================
    # TISUR
    # ========================================================

    "Tisur":
        "Tisur S.A.",


    # ========================================================
    # CETEMIN
    # ========================================================

    "Cetemin":
        "CETEMIN",


    # ========================================================
    # MANPOWER
    # ========================================================

    "Manpower":
        "ManpowerGroup",

    "ManpowerGroup Perú":
        "ManpowerGroup",

    "MANPOWER PERU S.A.C.":
        "ManpowerGroup",

    "Manpower Perú":
        "ManpowerGroup",

    "MANPOWER RPO BCP":
        "ManpowerGroup",

    "ManpowerGroup RPO":
        "ManpowerGroup",

    "Practicante de tesorería Manpower":
        "ManpowerGroup",


    # ========================================================
    # DANPER
    # ========================================================

    "Dirigido a hombres y mujeres Danper Trujillo SAC":
        "Danper Trujillo SAC",


    # ========================================================
    # GRUPO CENTENARIO
    # ========================================================

    "Grupo Centenario Lima":
        "Grupo Centenario",


    # ========================================================
    # AENZA
    # ========================================================

    "Grupo Aenza":
        "AENZA",


    # ========================================================
    # PROSERING
    # ========================================================

    "PROSERING SRLTDA":
        "PROSERING",

    "PROSERING Arequipa":
        "PROSERING",


    # ========================================================
    # NATURA
    # ========================================================

    "Natura Lima Metropolitan Area":
        "Natura",


    # ========================================================
    # EXPERTIA
    # ========================================================

    "Expertia Travel Lima":
        "Expertia Travel",


    # ========================================================
    # OVERALL STRATEGY
    # ========================================================

    "OVERALL STRATEGY S.A.C":
        "Overall Strategy",


    # ========================================================
    # TOPITOP
    # ========================================================

    "Topitop":
        "Topi Top",


    # ========================================================
    # BACKUS
    # ========================================================

    "BACKUS":
        "Backus",


    # ========================================================
    # TRANSPORTES CRUZ DEL SUR
    # ========================================================

    "Transportes Cruz Del Sur S.A.C":
        "Transportes Cruz Del Sur S.A.C.",


    # ========================================================
    # PACÍFICO EPS
    # ========================================================

    "Pacifico Eps":
        "Pacífico EPS",

    "Pacífico EPS":
        "Pacífico EPS",


    # ========================================================
    # RANSA
    # ========================================================

    "RANSA COMERCIAL S.A.C":
        "Ransa Comercial S.A.C.",

    "Ransa Comercial S.A.":
        "Ransa Comercial S.A.C.",


    # ========================================================
    # YURA
    # ========================================================

    "Yura S.A":
        "Yura S.A.",


    # ========================================================
    # MIND GROUP
    # ========================================================

    "Mind Group Arequipa":
        "Mind Group",


    # ========================================================
    # NEXUS SALUD OCUPACIONAL
    # ========================================================

    "Nexus Salud Ocupacional Arequipa, Arequipa, Perú":
        "Nexus Salud Ocupacional",


    # ========================================================
    # CLUB INTERNACIONAL AREQUIPA
    # ========================================================

    "Club Internacional Arequipa Arequipa":
        "Club Internacional Arequipa",


    # ========================================================
    # INDRA
    # ========================================================

    "Indra Group":
        "Indra",

    "INDRA PERU":
        "Indra",


    # ========================================================
    # FINANCIERA CONFIANZA
    # ========================================================

    "FINANCIERA CONFIANZA":
        "Financiera Confianza",


    # ========================================================
    # SHOUGANG
    # ========================================================

    "SHOUGANG HIERRO PERU S.A.A":
        "SHOUGANG HIERRO PERU S.A.A.",


    # ========================================================
    # COMPAÑÍA MINERA SOL DE LOS ANDES
    # ========================================================

    "Compañía Minera Sol de los Andes":
        "Compañía Minera Sol de los Andes S.A.C.",


    # ========================================================
    # DIAR INGENIEROS
    # ========================================================

    "DIAR INGENIEROS S.A":
        "Diar Ingenieros S.A.",

    "Diar Ingenieros S. A.":
        "Diar Ingenieros S.A.",


    # ========================================================
    # TIENDAS TAMBO
    # ========================================================

    "TIENDAS TAMBO":
        "Tiendas Tambo",


    # ========================================================
    # INGENIERÍA SUMINISTROS Y SOLUCIONES
    # ========================================================

    "8A INGENIERIA SUMINISTROS Y SOLUCIONES":
        "Ingeniería Suministros y Soluciones"
}


# ============================================================
# APLICAR ESTANDARIZACIÓN
# ============================================================

jobs_clean["externalCompanyName"] = (
    jobs_clean["externalCompanyName"]
    .replace(estandarizacion_empresas)
)


# ============================================================
# 4. VALIDACIÓN DE LA LIMPIEZA
# ============================================================

print("========================================")
print("RESUMEN DE DATASETS")
print("========================================")

print("\n========== COMPANIES ==========")
print("Filas:", companies_clean.shape[0])
print("Columnas:", companies_clean.shape[1])

print("\n========== JOBS ==========")
print("Filas:", jobs_clean.shape[0])
print("Columnas:", jobs_clean.shape[1])

print("\n========== APPLICATIONS ==========")
print("Filas:", applications_clean.shape[0])
print("Columnas:", applications_clean.shape[1])


# ============================================================
# 5. EMPRESAS DESPUÉS DE LA ESTANDARIZACIÓN
# ============================================================

print("\n========================================")
print("EMPRESAS ESTANDARIZADAS")
print("========================================")

print(
    jobs_clean["externalCompanyName"]
    .value_counts(dropna=False)
    .head(30)
    .to_string()
)


# ============================================================
# 6. REVISAR VALORES NULOS
# ============================================================

print("\n========================================")
print("VALORES NULOS")
print("========================================")

print("\n========== COMPANIES ==========")
print(companies_clean.isnull().sum())

print("\n========== JOBS ==========")
print(jobs_clean.isnull().sum())

print("\n========== APPLICATIONS ==========")
print(applications_clean.isnull().sum())


# ============================================================
# 7. VERIFICAR EMPRESAS ESTANDARIZADAS
# ============================================================

empresas_a_verificar = [

    "ManpowerGroup",
    "Caja Trujillo",
    "Komatsu Mitsui",
    "Universidad Tecnológica del Perú",
    "Repsol",
    "Camposol",
    "Eurofirms",
    "Grupo Gloria",
    "Adecco Perú S.A.",
    "CETEMIN",
    "Caja Cusco",
    "Tisur S.A.",
    "AENZA",
    "PROSERING",
    "Natura",
    "Expertia Travel",
    "Overall Strategy",
    "Topi Top",
    "Backus",
    "Pacífico EPS",
    "Ransa Comercial S.A.C.",
    "Yura S.A.",
    "Mind Group",
    "Nexus Salud Ocupacional",
    "Club Internacional Arequipa",
    "Indra",
    "Financiera Confianza",
    "SHOUGANG HIERRO PERU S.A.A.",
    "Tiendas Tambo",
    "Ingeniería Suministros y Soluciones",
    "Importante Empresa en el sector"
]


verificacion = (
    jobs_clean[
        jobs_clean["externalCompanyName"].isin(empresas_a_verificar)
    ]["externalCompanyName"]
    .value_counts()
    .rename_axis("Empresa estandarizada")
    .reset_index(name="Cantidad")
)


print("\n========================================")
print("VERIFICACIÓN DE EMPRESAS")
print("========================================")

print(
    verificacion.to_string(index=False)
)


# ============================================================
# 8. RESULTADO FINAL
# ============================================================

print("\n========================================")
print("RESULTADO FINAL")
print("========================================")

print(
    "La limpieza y estandarización de empresas ha sido completada."
)

print(
    "No se realizaron relaciones ni cruces entre collections."
)

print(
    "Los nombres de empresas externas fueron agrupados "
    "bajo nombres estandarizados."
)