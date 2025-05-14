# Instalación del proyecto   

## Crear un entorno virtual   
Ubicate en la carpeta del proyecto, y crea un entorno virtual para el proyecto. El siguiente comanto crea un entorno virtual con el nombre de ".venv"   
`python3 -m venv .venv`   

## Activa el entorno virtual
Una vez creado el entorno virtual, es necesario activarlo. Ejecuta uno de los siguientes comandos   

### macOS y Linux
`. .venv/bin/activate`   

### Windows
`.venv\Scripts\activate`   

## Desactivar el entorno virtual
Para desactivar el entorno virtual utiliza el siguiente comando      
`deactivate` 

## Instalar dependencias desde requirements.txt
Para instalar los paquetes y dependencias requeridos por el proyecto, ejecuta el siguiente comando:   
`pip install -r requirements.txt`   

## Ejecutar la aplicación
Ubicate en la carpeta del proyecto y ejecuta el siguiente comando desde la terminal:   
`flask run`   

Para ejecutarlo en modo depuración utiliza `flask run --debug`

## Abrela en tu navegador
Ingresa en la siguiente dirección en tu navegador **http://127.0.0.1:5000** y voilá