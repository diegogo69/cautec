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

## Errores al activar el entorno virtual en PowerShell

Si al intentar activr el entorno virtual obtienes el siguiente error:

> No se puede cargar el archivo ...\.venv\Scripts\Activate.ps1 porque la ejecución de scripts está deshabilitada en este sistema.

Abre una terminal de PowerShell como administrador

Ejecuta el siguiente comando:  
`Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

## Instalar dependencias desde requirements.txt

Con el entorno virtual activo instala los paquetes y dependencias requeridos por el proyecto ejecutanto el siguiente comando:  
`pip install -r requirements.txt`

## Instalar wkhtmltopdf

Para la generación de reportes en formato PDF se requiere la librería wkhtmltopdf, que trabaja en conjunto con el paquete Jinja2 que se instala junto con Flask.

### Linux Ubuntu

Puedes hacer una instalación rápida, aunque quizás no de la versión más reciente de wkhtmltopdf, ejecutando el siguiente comando:
`apt-get install wkhtmltopdf`

Puedes verificar de antemano la versión que se instalará con el siguiente comando:
`apt-cache policy wkhtmltopdf`

Para instalar la versión más reciente, busca el instalador para tu arquitectura en la página de [descargas de wkhtmltopdf](https://wkhtmltopdf.org/downloads.html), y copia el link de descarga.

Instala o actualiza wget:  
`sudo apt update && sudo apt install wget`

Descarga el paquete usando wget y el link de descarga que copiaste:
`wget .../wkhtmltox_0.12.6.1-2.jammy_amd64.deb`

Instala el paquete recién descargado, asegúrate que el nombre sea el correcto:
`sudo apt install -f ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb`

Verifica la instalación:
`wkhtmltopdf --version`

### Windows

Descarga el instalador compatible para tu versión de windows desde la página de [descargas de wkhtmltopdf](https://wkhtmltopdf.org/downloads.html).

Ejecuta el instalador, y copia la ruta en la que se instalará, por defecto es en la carpeta de archivos de programas _C:\Program Files\wkhtmltopdf_

En el inicio de windows busca "env" y abre la configuración de _Variables de entorno del sistema_

Haz click en **Variables de entorno**

En la sección inferior de _Variables del sistema_ haz doble click en _Path_

Haz click en **Nuevo**

Pega la ruta donde se instaló wkhtmltopdf añadiendo el texto "\bin" al final de ruta, tal que así: _C:\Program Files\wkhtmltopdf\bin_. Y presiona la tecla Enter.

Haz click en aceptar hasta salir de la configuración.

Verifica la instalación con el comando `wkhtmltopdf --version`. Y que se agregó al _Path_ correctamente ejecutando `where wkhtmltopdf`, te debe devolver la ruta del ejecutable de wkhtmltopdf.

## Ejecutar la aplicación

Ejecuta el servidor de la aplicacón aplicación utilizando el siguiente comando desde la terminal:  
`flask run`

Para ejecutarlo en modo depuración utiliza `flask run --debug`

## Abrela en tu navegador

Desde tu navegador ingresa a la aplicación web a través de la dirección url: **http://127.0.0.1:5000**. Y voilá.
