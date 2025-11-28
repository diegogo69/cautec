ESTADOS_REPORTE = [
    'nuevo',
    'pendiente',
    'en proceso',
    'cerrado',
]

TIPOS_DISPOSITIVOS = [
    "cpu",
    "teclado",
    "mouse",
    "monitor",
    "regulador",
    "impresora",
    "router",
    # "cornetas",
    # "regulador de voltaje",
    'otro',
]

FALLAS_DISPOSITIVOS = [
    # {'tipo', 'predeterminada', 'descripcion'},
    {'tipo': 'general', 'predeterminada': True, 'descripcion': 'no enciende'},
    {'tipo': 'general', 'predeterminada': True, 'descripcion': 'se apaga'},
    {'tipo': 'general', 'predeterminada': True, 'descripcion': 'se queda pegada'},
    {'tipo': 'general', 'predeterminada': True, 'descripcion': 'monitor no muestra imagen'},
]
