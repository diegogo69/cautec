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

AREAS_TIPOS_PLURAL = {
    "aula": "aulas",
    "coordinación": "coordinaciones",
    "cubiculo": "cubiculos",
    "dirección": "direcciones",
    "departamento": "departamentos",
    "dependencia": "dependencias",
    "laboratorio": "laboratorios",
    "unidad": "unidades",
    "oficina": "oficinas",
}


def departamentos_json():
    departamentos_db = Departamento.query.all()

    # departamentos_lista = []
    dep_json = {}

    for tipo in AREAS_TIPOS:
        dep_json[tipo] = []

    for dep in departamentos_db:

        if dep.tipo not in dep_json.keys():
            raise 'El area no es valida'
        
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

        dep_json[tipo].append(dep_diccionario)
        # departamentos_lista.append(dep_diccionario)

    print()
    print(dep_json)
    return dep_json


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
