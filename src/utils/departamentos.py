from src.models.departamento import Departamento


AREAS_TIPOS = [
    "aula",
    "coordinación",
    "cubiculo",
    "dirección",
    "departamento",
    "dependencia",
    "laboratorio",
    "unidad",
    "oficina",
]


def departamentos_json():
    departamentos_lista = []
    departamentos_db = Departamento.query.all()
    print()
    print(departamentos_db)

    for dep in departamentos_db:
        id = dep.id
        tipo = dep.tipo
        nombre = dep.nombre
        ubicacion = dep.ubicacion
        nombre_coordinador = dep.nombre_coordinador
        linea_telefonica = dep.linea_telefonica

        dep_diccionario = {
            "id": id,
            "tipo": tipo,
            "nombre": nombre,
            "ubicacion": ubicacion,
            "nombre_coordinador": nombre_coordinador,
            "linea_telefonica": linea_telefonica,
        }

        departamentos_lista.append(dep_diccionario)

    return departamentos_lista


def departamentosToCsv():
    import csv

    departamentos_lista = []
    departamentos_db = Departamento.query.all()
    print()
    print(departamentos_db)

    for dep in departamentos_db:
        id = dep.id
        tipo = dep.tipo
        nombre = dep.nombre
        ubicacion = dep.ubicacion
        nombre_coordinador = dep.nombre_coordinador
        linea_telefonica = dep.linea_telefonica

        dep_diccionario = {
            "id": id,
            "tipo": tipo,
            "nombre": nombre,
            "ubicacion": ubicacion,
            "nombre_coordinador": nombre_coordinador,
            "linea_telefonica": linea_telefonica,
        }

        departamentos_lista.append(dep_diccionario)

    with open("local/csv/departamentos.csv", "w") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "id",
                "tipo",
                "nombre",
                "ubicacion",
                "nombre_coordinador",
                "linea_telefonica",
            ],
        )

        writer.writeheader()
        for dep in departamentos_lista:
            writer.writerow(dep)

    file.close()
