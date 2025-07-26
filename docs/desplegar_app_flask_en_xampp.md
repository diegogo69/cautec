# Desplegar aplicación Flask en XAMPP Apache (Windows)   
Para nuestro proyecto utilizaremos un entorno virtual, para trabajar de forma más organizada y eficiente, y con el paquete **mod_wsgi** que es el encargado de indicarle a nuestro servidor Apache como ejecutar nuestra aplicación Flask.   

Este ejemplo asume lo siguiente:
- Nuestra Aplicación Flask se llama *mi_app*   
- La ruta de nuestra instalación de Apache es *C:\xampp\apache*   
- La carpeta de nuestra aplicación está ubicada en la carpeta *htdocs* de XAMPP (*C:\xampp\htdocs\mi_app*)   
- Nuestra aplicación utilizará el puerto *5001*


## Instalación de Visual C++ Build Tools   
Instala las librerías de Microsoft Visual C++ Build Tools (https://visualstudio.microsoft.com/visual-cpp-build-tools/). Se recomienda instalar la versión más reciente, aunque la mínima requerida es la 14.0.0.   


## Instalación completa de Python   
Debes tener una instalación completa de Python que incluya el instalador de paquetes **pip**, y te permita la creación de entornos virtuales.

**Verificar Python**: `python --version`   

**Verificar pip**: `pip --version`   


## Instalación de Apache o XAMPP   
Se recomienda usar una versión reciente de Apache, o de XAMPP que incluye Apache.

**Importante**: Todas las instalaciones deben ser de la misma arquitectura, es decir, todas son de 32-bits o todas son de 64-bits.


## Archivos del proyecto   
Nuestro proyecto debe incluir el archivo principal de nuestra aplicación, generalmente *app.py*, que define nuestra aplicación Flask y además incluir un archivo *.wsgi* que funcionará como el archivo de entrada para nuestro servidor Apache.


### mi_app.wsgi
Crea un archivo *.wsgi* con el nombre de tu aplicación, en este caso *mi_app.wsgi*, y añade el siguiente contenido:

```
import sys

sys.path.insert(0, 'C:\\xampp\\htdocs\\mi_app')

from app import app as application
```

El archivo es básicamente código python, que importa la aplicación flask (*app*) del archivo principal (*app.py*) con el nombre de *application*. Las primeras lineas definen a la ruta del proyecto como la primera ruta en la cual buscar los modulos importados, en este caso la importación de *app*.


### app.py
Este ejemplo define una aplicación Flask básica en un archivo *app.py* con el siguiente contenido:   

```
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Malditx apache de la mierdxxxxxxxxxxxxxxxxxxxxx"
    
if __name__ == "__main__":
    app.run()
```


## Instalar Apache como servicio   
Este paso es recomendable para evitar errores. Abre CMD como administrador y ejecuta el siguiente comando:   

`C:\xampp\apache\bin\httpd.exe -k install`

El comando utiliza la ruta por defecto de la instalación de XAMPP. En caso de que hayas elegido una ruta diferente para la instalación de XAMPP debes utilizar la ruta que elegiste. Al completar este paso puedes cerrar el CMD.   


## Definir variable de entorno para Apache   
Debemos indicar la ruta de nuestra instalación de Apache, que en este caso es una instalación de Apache con XAMPP. Para ello definimos una variable de entorno con la ruta nuestra instalación de Apache utilizando **diagonales hacia delante** ( **/** ), y no hacia atrás ( **\\** ).   

Abre una terminal CMD en el directorio de tu proyecto y ejecuta el siguiente comando:   

`set MOD_WSGI_APACHE_ROOTDIR=C:/xampp/apache`

**IMPORTANTE:** Asegúrate que la ruta de Apache en el comando usa diagonales hacia delante ( **////** )   


## Activar el entorno virtual   
La instalación del paquete mod_wsgi la haremos en el entorno virtual de nuestro proyecto. Si tu entorno virtual se llama *.venv* ejecuta el siguiente comando:   

`.venv\Scripts\activate`


## Instalar mod_wsgi   
Este es el paso que presenta más inconvenientes, habiendo seguido los pasos anteriores deberías estar tranquilo. Para la instalación del paquete se utilizarán tres directivas, la primera (*--require-virtualenv*) indica que la instalación sólo se realizará si el entorno virtual está activado, para evitar una instalación global; la segunda (*--no-cache-dir*) indica que se deshabilitará la caché para la instalación del paquete, para evitar una instalación posiblemente corrupta; y la tercera (*-U*) asegura que se instale la versión más reciente del paquete.

En el CMD con el entorno virtual activo ejecuta el siguiente comando:   

`pip install --require-virtualenv --no-cache-dir -U mod_wsgi`

**Nota:** Si existe una instalacion previa de mod_wsgi, global o en el entorno virtual, desinstalala con `pip uninstall mod_wsgi` para evitar errores en la instalación.   


## Obtener la configuración de mod_wsgi   
Debemos generar la configuración que utilizará Apache para nuestra aplicación Flask.

Ejecuta el siguiente comando:   

`mod_wsgi-express module-config`

Copia el texto que aparece en la terminal, que luce algo similar a esto:   

> LoadFile "c:/program files/python37/python37.dll"   
> LoadModule wsgi_module "C:/Users/prod_deploy/AppData/Roaming/Python/Python37/site-packages/mod_wsgi/server/mod_wsgi.cp37-win_amd64.pyd"   
> WSGIPythonHome "c:/program files/python37"   


## Añadir configuración de mod_wsgi a Apache   
La configuración de mod_wsgi que generamos ahora debemos añadirla al archivo **httpd.conf** de configuración de Apache.   

- Abre el archivo **httpd.conf** de Apache. Esto lo puedes hacer desde el botón config de Apache en XAMPP o desde la carpeta *conf* del directorio de Apache.

- Dentro del archivo busca la última línea que contenga *LoadModule*

- Pega el texto de configuracion después de todos los *LoadModule*


## Añadir configuración del puerto de la aplicación   
Debemos indicar a Apache el puerto que nuestra aplicación utilizará

Dentro de httpd.conf busca las líneas que digan *Listen*   

Debajo de la ultima línea *Listen* añade una línea para tu puerto:   

`Listen 5001`

En este ejemplo el puerto es *5001*


## Añadir configuración de ServerName de nuestra aplicación   
Siguiendo un proceso similar al anterior, debemos indicar a Apache el ServerName, o dominio, de nuestra aplicación. Este puede ser *localhost*, *127.0.0.1*, la dirección de nuestro computador, o un dominio real en caso de tenerlo.

Dentro de httpd.conf busca las línea que digan *ServerName*   

Justo debajo de la ultima añade una linea para tu aplicación:   

`ServerName localhost:5001`

En este ejemplo el ServerName es *localhost* y el puerto es *5001*   


## Añadir configuración del servidor   
Para que Apache muestre nuestra Aplicación debemos generar la configuración del servidor de nuestra aplicación. 

Pega la siguiente configuración al final del archivo **httpd.conf**, haciendo modificaciones respectivas según tu aplicación (puerto, servername, ruta del archivo *.wsgi* y de la carpeta del proyecto)   

```
<VirtualHost *:5001>
	ServerName localhost
	WSGIScriptAlias /mi_app C:/xampp/htdocs/mi_app/app.wsgi

	<Directory C:/xampp/htdocs/mi_app>
		Require all granted
	</Directory>
</VirtualHost>
```

## Voilà   
Activa el servidor Apache, y accede a tu aplicación desde http://localhost:5001/mi_app, si todo ha salido bien, deberías ver un bonito mensaje en pantalla.   
