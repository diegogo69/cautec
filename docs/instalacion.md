# Instalación del proyecto

## Crear un entorno virtual

Ubicate en la carpeta del proyecto, y crea un entorno virtual para el proyecto. El siguiente comanto crea un entorno virtual con el nombre de ".venv"  
**linux**: `python3 -m venv .venv`  
**windows**: `python -m venv .venv`

## Activa el entorno virtual

Una vez creado el entorno virtual, es necesario activarlo. Ejecuta uno de los siguientes comandos

### macOS y Linux

`. .venv/bin/activate`

### Windows

`.venv\Scripts\activate`

Para desactivar el entorno virtual utiliza el comando `deactivate`

## Instalar dependencias desde requirements.txt

Con el entorno virtual activo instala los paquetes y dependencias requeridos por el proyecto ejecutanto el siguiente comando:  
`pip install -r requirements.txt`

## Ejecutar la aplicación

Ejecuta el servidor de la aplicacón aplicación utilizando el siguiente comando desde la terminal:  
`flask run`

Para ejecutarlo en modo depuración utiliza `flask run --debug`

## Abrela en tu navegador

Desde tu navegador ingresa a la aplicación web a través de la dirección url: **http://127.0.0.1:5000**. Y voilá.
