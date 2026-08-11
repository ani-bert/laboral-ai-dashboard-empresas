import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


def constructor():
    # Conexión a MongoDB
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("DB_NAME")]

    # Columnas necesarias de companies
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

    # Columnas necesarias de jobs
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

    # Columnas necesarias de applications
    applications_columns = [
        "_id",
        "job",
        "createdAt",
        "applicationStatus"
    ]

    # Obtener datos desde MongoDB
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