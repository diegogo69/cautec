ESTADOS_REPORTE = [
    'nuevo',
    'pendiente',
    'en proceso',
    'cerrado',
]

TIPOS_DISPOSITIVOS = [
    "monitor",
    "mouse",
    "teclado",
    "cpu",
    "impresora",
    "escáner",
    "cornetas",
    "regulador de voltaje",
]

FALLAS_DISPOSITIVOS = [
    # {'tipo', 'predeterminada', 'descripcion'},
    {'tipo': 'general', 'predeterminada': True, 'descripcion': 'no enciende'},
    {'tipo': 'general', 'predeterminada': True, 'descripcion': 'se apaga'},
    {'tipo': 'general', 'predeterminada': True, 'descripcion': 'se queda pegada'},
    {'tipo': 'general', 'predeterminada': True, 'descripcion': 'monitor no muestra imagen'},
]
