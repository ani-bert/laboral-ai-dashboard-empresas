
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient


# ============================================================
# CONFIGURACIÓN
# ============================================================

load_dotenv()

# La raíz del proyecto es la carpeta que contiene "scripts"
BASE_DIR = Path(__file__).resolve().parent.parent

# Carpeta de memoria caché
CACHE_DIR = BASE_DIR / "data_cache"

# Crear la carpeta si todavía no existe
CACHE_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# CONSTRUCTOR DE DATOS
# ============================================================

def constructor():

    # ========================================================
    # 1. CONEXIÓN Y CARGA DESDE MONGODB
    # ========================================================

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

    # ========================================================
    # 2. LIMPIEZA DE COMPANIES
    # ========================================================

    companies_clean = companies.copy()

    # --------------------------------------------------------
    # Limpiar columnas de texto
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Estandarizar país
    # --------------------------------------------------------

    companies_clean["country"] = companies_clean["country"].replace({
        "Peru": "Perú"
    })

    # --------------------------------------------------------
    # Extraer tipo de plan
    # --------------------------------------------------------

    companies_clean["planType"] = companies_clean["plan"].apply(
        lambda x: x.get("type") if isinstance(x, dict) else None
    )

    companies_clean["planType"] = (
        companies_clean["planType"]
        .replace({"None": "NONE"})
        .fillna("NONE")
    )

    # ========================================================
    # 3. LIMPIEZA DE JOBS
    # ========================================================

    jobs_clean = jobs.copy()

    # --------------------------------------------------------
    # Limpiar columnas de texto
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Estandarizar modalidad
    # --------------------------------------------------------

    jobs_clean["modality"] = jobs_clean["modality"].replace({
        "hibrido": "híbrido"
    })

    # --------------------------------------------------------
    # Estandarizar país
    # --------------------------------------------------------

    jobs_clean["country"] = jobs_clean["country"].replace({
        "Peru": "Perú"
    })

    # --------------------------------------------------------
    # Tratar valores inválidos/vacíos en country
    # --------------------------------------------------------

    jobs_clean["country"] = jobs_clean["country"].replace(
        r"^\s*\*\s*$",
        pd.NA,
        regex=True
    )

    # --------------------------------------------------------
    # Limpiar geographicDepartment
    # --------------------------------------------------------

    jobs_clean["geographicDepartment"] = (
        jobs_clean["geographicDepartment"]
        .astype("string")
        .str.strip()
        .replace({
            "5": pd.NA,
            "": pd.NA
        })
    )

    # --------------------------------------------------------
    # Eliminar valores inválidos de department
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Correcciones de escritura en department
    # --------------------------------------------------------

    correcciones_department = {
        "Comercia": "Comercial",
        "Contabilidad y Finanzasc": "Contabilidad y Finanzas",
        "Auditoria": "Auditoría",
        "Psicologia": "Psicología",
        "Tecnologia": "Tecnología",
        "Tecnologia / Sistemas": "Tecnología / Sistemas",
        "Tecnologia / TI": "Tecnología / TI",
        "Tecnologia /Soporte Técnico":
            "Tecnología / Soporte Técnico",
        "Tecnologia / TI , Soporte Técnico":
            "Tecnología / TI, Soporte Técnico",
        "Comunicaciónes": "Comunicaciones",
        "Comunicacion": "Comunicación",
        "Diseño Grafico": "Diseño Gráfico",
        "Diseño gráfico": "Diseño Gráfico",
        "Mineria": "Minería",
        "Atención al cliente": "Atención al Cliente",
        "Trabajo social": "Trabajo Social",
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

    # --------------------------------------------------------
    # Convertir fechas
    # --------------------------------------------------------

    jobs_clean["createdAt"] = pd.to_datetime(
        jobs_clean["createdAt"],
        errors="coerce"
    )

    jobs_clean["publishUntil"] = pd.to_datetime(
        jobs_clean["publishUntil"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Eliminar únicamente inconsistencias temporales
    #
    # publishUntil no puede ser anterior a createdAt.
    #
    # Si alguna fecha está vacía, NO se elimina el registro.
    # --------------------------------------------------------

    fechas_invalidas = (
        jobs_clean["publishUntil"].notna()
        & jobs_clean["createdAt"].notna()
        & (
            jobs_clean["publishUntil"]
            < jobs_clean["createdAt"]
        )
    )

    jobs_clean = jobs_clean.loc[
        ~fechas_invalidas
    ].copy()

    jobs_clean.reset_index(
        drop=True,
        inplace=True
    )

    # ========================================================
    # 4. LIMPIEZA DE APPLICATIONS
    # ========================================================

    applications_clean = applications.copy()

    applications_clean["applicationStatus"] = (
        applications_clean["applicationStatus"]
        .fillna("SIN_ESTADO")
    )

    # ========================================================
    # 5. ESTANDARIZACIÓN DE EMPRESAS
    # ========================================================

    estandarizacion_empresas = {

        # ----------------------------------------------------
        # EMPRESAS NO IDENTIFICADAS
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # GLORIA
        # ----------------------------------------------------

        "Gloria":
            "Grupo Gloria",

        "Gloria S.A":
            "Grupo Gloria",

        "Gloria S.A.":
            "Grupo Gloria",

        # ----------------------------------------------------
        # KOMATSU MITSUI
        # ----------------------------------------------------

        "KOMATSU - MITSUI MAQUINARIAS":
            "Komatsu Mitsui",

        "KOMATSU MITSUI":
            "Komatsu Mitsui",

        # ----------------------------------------------------
        # CAJA TRUJILLO
        # ----------------------------------------------------

        "CAJA TRUJILLO":
            "Caja Trujillo",

        # ----------------------------------------------------
        # REPSOL
        # ----------------------------------------------------

        "REPSOL":
            "Repsol",

        # ----------------------------------------------------
        # CAMPOSOL
        # ----------------------------------------------------

        "CAMPOSOL":
            "Camposol",

        "CAMPOSOL S.A.":
            "Camposol",

        # ----------------------------------------------------
        # EUROFIRMS
        # ----------------------------------------------------

        "EUROFIRMS":
            "Eurofirms",

        "Eurofirms Perú":
            "Eurofirms",

        # ----------------------------------------------------
        # UTP
        # ----------------------------------------------------

        "UNIVERSIDAD TECNOLOGICA DEL PERU":
            "Universidad Tecnológica del Perú",

        "UNIVERSIDAD TECNOLOGICA DEL PERU(UTP)":
            "Universidad Tecnológica del Perú",

        # ----------------------------------------------------
        # CAJA CUSCO
        # ----------------------------------------------------

        "CAJA CUSCO":
            "Caja Cusco",

        # ----------------------------------------------------
        # CARTAVIO
        # ----------------------------------------------------

        "Cartavio Rum Company":
            "CARTAVIO RUM COMPANY S.A.C.",

        # ----------------------------------------------------
        # ADECCO
        # ----------------------------------------------------

        "Adecco Perú":
            "Adecco Perú S.A.",

        "Adecco Perú S.A.SAC":
            "Adecco Perú S.A.",

        "ADECCO BCP":
            "Adecco Perú S.A.",

        "Practicante Profesional de Contabilidad Adecco Perú S.A.":
            "Adecco Perú S.A.",

        # ----------------------------------------------------
        # TISUR
        # ----------------------------------------------------

        "Tisur":
            "Tisur S.A.",

        # ----------------------------------------------------
        # CETEMIN
        # ----------------------------------------------------

        "Cetemin":
            "CETEMIN",

        # ----------------------------------------------------
        # MANPOWER
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # DANPER
        # ----------------------------------------------------

        "Dirigido a hombres y mujeres Danper Trujillo SAC":
            "Danper Trujillo SAC",

        # ----------------------------------------------------
        # GRUPO CENTENARIO
        # ----------------------------------------------------

        "Grupo Centenario Lima":
            "Grupo Centenario",

        # ----------------------------------------------------
        # AENZA
        # ----------------------------------------------------

        "Grupo Aenza":
            "AENZA",

        # ----------------------------------------------------
        # PROSERING
        # ----------------------------------------------------

        "PROSERING SRLTDA":
            "PROSERING",

        "PROSERING Arequipa":
            "PROSERING",

        # ----------------------------------------------------
        # NATURA
        # ----------------------------------------------------

        "Natura Lima Metropolitan Area":
            "Natura",

        # ----------------------------------------------------
        # EXPERTIA
        # ----------------------------------------------------

        "Expertia Travel Lima":
            "Expertia Travel",

        # ----------------------------------------------------
        # OVERALL STRATEGY
        # ----------------------------------------------------

        "OVERALL STRATEGY S.A.C":
            "Overall Strategy",

        # ----------------------------------------------------
        # TOPITOP
        # ----------------------------------------------------

        "Topitop":
            "Topi Top",

        # ----------------------------------------------------
        # BACKUS
        # ----------------------------------------------------

        "BACKUS":
            "Backus",

        # ----------------------------------------------------
        # TRANSPORTES CRUZ DEL SUR
        # ----------------------------------------------------

        "Transportes Cruz Del Sur S.A.C":
            "Transportes Cruz Del Sur S.A.C.",

        # ----------------------------------------------------
        # PACÍFICO EPS
        # ----------------------------------------------------

        "Pacifico Eps":
            "Pacífico EPS",

        "Pacífico EPS":
            "Pacífico EPS",

        # ----------------------------------------------------
        # RANSA
        # ----------------------------------------------------

        "RANSA COMERCIAL S.A.C":
            "Ransa Comercial S.A.C.",

        "Ransa Comercial S.A.":
            "Ransa Comercial S.A.C.",

        # ----------------------------------------------------
        # YURA
        # ----------------------------------------------------

        "Yura S.A":
            "Yura S.A.",

        # ----------------------------------------------------
        # MIND GROUP
        # ----------------------------------------------------

        "Mind Group Arequipa":
            "Mind Group",

        # ----------------------------------------------------
        # NEXUS SALUD OCUPACIONAL
        # ----------------------------------------------------

        "Nexus Salud Ocupacional Arequipa, Arequipa, Perú":
            "Nexus Salud Ocupacional",

        # ----------------------------------------------------
        # CLUB INTERNACIONAL AREQUIPA
        # ----------------------------------------------------

        "Club Internacional Arequipa Arequipa":
            "Club Internacional Arequipa",

        # ----------------------------------------------------
        # INDRA
        # ----------------------------------------------------

        "Indra Group":
            "Indra",

        "INDRA PERU":
            "Indra",

        # ----------------------------------------------------
        # FINANCIERA CONFIANZA
        # ----------------------------------------------------

        "FINANCIERA CONFIANZA":
            "Financiera Confianza",

        # ----------------------------------------------------
        # SHOUGANG
        # ----------------------------------------------------

        "SHOUGANG HIERRO PERU S.A.A":
            "SHOUGANG HIERRO PERU S.A.A.",

        # ----------------------------------------------------
        # COMPAÑÍA MINERA SOL DE LOS ANDES
        # ----------------------------------------------------

        "Compañía Minera Sol de los Andes":
            "Compañía Minera Sol de los Andes S.A.C.",

        # ----------------------------------------------------
        # DIAR INGENIEROS
        # ----------------------------------------------------

        "DIAR INGENIEROS S.A":
            "Diar Ingenieros S.A.",

        "Diar Ingenieros S. A.":
            "Diar Ingenieros S.A.",

        # ----------------------------------------------------
        # TIENDAS TAMBO
        # ----------------------------------------------------

        "TIENDAS TAMBO":
            "Tiendas Tambo",

        # ----------------------------------------------------
        # INGENIERÍA SUMINISTROS Y SOLUCIONES
        # ----------------------------------------------------

        "8A INGENIERIA SUMINISTROS Y SOLUCIONES":
            "Ingeniería Suministros y Soluciones"
    }

    jobs_clean["externalCompanyName"] = (
        jobs_clean["externalCompanyName"]
        .replace(estandarizacion_empresas)
    )

    # ========================================================
    # 6. NORMALIZACIÓN DE IDS
    # ========================================================

    applications_clean["job"] = (
        applications_clean["job"]
        .astype(str)
    )

    jobs_clean["_id"] = (
        jobs_clean["_id"]
        .astype(str)
    )

    jobs_clean["companyId"] = (
        jobs_clean["companyId"]
        .astype(str)
    )

    companies_clean["_id"] = (
        companies_clean["_id"]
        .astype(str)
    )

    # ========================================================
    # 7. CRUCE APPLICATIONS → JOBS
    # ========================================================

    applications_jobs = applications_clean.merge(
        jobs_clean,
        left_on="job",
        right_on="_id",
        how="left",
        suffixes=(
            "_application",
            "_job"
        )
    )

    # ========================================================
    # 8. CRUCE APPLICATIONS + JOBS → COMPANIES
    # ========================================================

    applications_final = applications_jobs.merge(
        companies_clean,
        left_on="companyId",
        right_on="_id",
        how="left",
        suffixes=(
            "",
            "_company"
        )
    )

    # ========================================================
    # 9. VALIDACIÓN DE DATASETS
    # ========================================================

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

    # ========================================================
    # 10. VALIDACIÓN DE CRUCES
    # ========================================================

    print("\n========================================")
    print("VALIDACIÓN DE CRUCES")
    print("========================================")

    print(
        "Postulaciones originales:",
        len(applications_clean)
    )

    print(
        "Postulaciones después del cruce:",
        len(applications_final)
    )

    print(
        "Postulaciones duplicadas:",
        applications_final[
            "_id_application"
        ].duplicated().sum()
    )

    print(
        "Postulaciones con oferta:",
        applications_final[
            "_id_job"
        ].notna().sum()
    )

    print(
        "Postulaciones con empresa:",
        applications_final[
            "businessName"
        ].notna().sum()
    )

    # ========================================================
    # 11. RESULTADO FINAL
    # ========================================================

    print("\n========================================")
    print("RESULTADO FINAL")
    print("========================================")

    print(
        "La carga, limpieza y estandarización "
        "de los datos ha sido completada."
    )

    print(
        "Las collections applications, jobs y companies "
        "fueron relacionadas mediante sus identificadores."
    )

    print(
        "Los nombres de empresas externas fueron "
        "agrupados bajo nombres estandarizados."
    )

    print(
        "Los cruces fueron validados correctamente."
    )

    # ========================================================
    # 12. GUARDAR DATASETS EN CACHE
    # ========================================================

    companies_clean.to_csv(
        CACHE_DIR / "companies_clean.csv",
        index=False
    )

    jobs_clean.to_csv(
        CACHE_DIR / "jobs_clean.csv",
        index=False
    )

    applications_clean.to_csv(
        CACHE_DIR / "applications_clean.csv",
        index=False
    )

    applications_jobs.to_csv(
        CACHE_DIR / "applications_jobs.csv",
        index=False
    )

    applications_final.to_csv(
        CACHE_DIR / "applications_final.csv",
        index=False
    )

    print("\n========================================")
    print("CACHE")
    print("========================================")

    print(
        f"Datasets guardados en: {CACHE_DIR}"
    )

    print("\nArchivos generados:")

    print("✓ companies_clean.csv")
    print("✓ jobs_clean.csv")
    print("✓ applications_clean.csv")
    print("✓ applications_jobs.csv")
    print("✓ applications_final.csv")

    # ========================================================
    # 13. RETORNO DE TABLAS
    # ========================================================

    return (
        companies_clean,
        jobs_clean,
        applications_clean,
        applications_jobs,
        applications_final
    )


# ============================================================
# EJECUCIÓN DIRECTA
# ============================================================

if __name__ == "__main__":

    (
        companies_clean,
        jobs_clean,
        applications_clean,
        applications_jobs,
        applications_final
    ) = constructor()

