from scripts.conexion import conectar_mongo


def obtener_colecciones():
    """
    Obtiene la lista de colecciones disponibles
    en la base de datos de Laboral.ai.
    """

    cliente, db = conectar_mongo()

    try:
        colecciones = db.list_collection_names()

        print(f"Total de colecciones: {len(colecciones)}")
        print("\nColecciones:")

        for coleccion in sorted(colecciones):
            print(f"- {coleccion}")

        return colecciones

    finally:
        cliente.close()


if __name__ == "__main__":
    obtener_colecciones()