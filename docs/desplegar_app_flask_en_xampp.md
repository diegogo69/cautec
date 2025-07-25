# Desplegar aplicación Flask en XAMPP Apache (Windows)
Para nuestro proyecto utilizaremos un entorno virtual, para trabajar de forma más organizada y eficiente.   
**mod_wsgi** es el encargado de indicarle a nuestro servidor Apache como ejecutar nuestra aplicación Flask.   

Este ejemplo asume lo siguiente:
- Nuestra Aplicación Flask se llama *mi_app*   
- La ruta de nuestra instalación de Apache es *C:\xampp\apache*   
- La carpeta de nuestra aplicación está ubicada en la carpeta *htdocs* de XAMPP (*C:\xampp\htdocs\mi_app*)   
- Nuestra aplicación utilizará el puerto *5001*


## Instalación de Visual C++ Build Tools   
Instala las librerías de Microsoft Visual C++ Build Tools (https://visualstudio.microsoft.com/visual-cpp-build-tools/).   

## Instalación completa de Python   
Debes tener una instalación completa de Python que incluya el instalador de paquetes **pip**, y te permita la creación de entornos virtuales.

**Verificar Python**: `python --version`   

**Verificar pip**: `pip --version`   


## Instalar Apache como servicio   
Este paso es recomendable para evitar errores. Abre CMD como administrador y ejecuta el siguiente comando:   

`C:\xampp\apache\bin\httpd.exe -k install`

El comando utiliza la ruta por defecto de la instalación de XAMPP. En caso de que hayas elegido una ruta diferente para la instalación de XAMPP debes utilizar la ruta que elegiste.   

## Definir variable de entorno para Apache   
Debemos indicar la ruta de nuestra instalación de Apache, que en este caso es una instalación de Apache con XAMPP. Para ello definimos una variable de entorno con la ruta nuestra instalación de Apache utilizando **diagonales hacia delante** ( **/** ), y no hacia atrás ( **\\** ).   

Abre una terminal CMD en el directorio de tu proyecto y ejecuta el siguiente comando:   

`set MOD_WSGI_APACHE_ROOTDIR=C:/xampp/apache`

**IMPORTANTE:** Asegúrate que la ruta de Apache en el comando usa diagonales hacia delante ( **////** )   

## Activar el entorno virtual
La instalación del paquete mod_wsgi la haremos en el entorno virtual de nuestro proyecto. Si tu entorno virtual se llama *.venv* ejecuta el siguiente comando:   

`.venv\Scripts\activate`

## Instalar mod_wsgi
Este es el paso que presenta más inconvenientes, habiendo seguido los pasos anteriores deberías estar tranquilo. Para la instalación del paquete se utilizarán dos directivas, la primera (*--require-virtualenv*) indica que la instalación sólo se realizará si el entorno virtual está activado, para evitar una instalación global; la segunda (*--no-cache-dir*) indica que se deshabilitará la caché para la instalación del paquete, para evitar una instalación posiblemente corrupta.

En el CMD con el entorno virtual activo ejecuta el siguiente comando:   

`pip install --require-virtualenv --no-cache-dir mod_wsgi`


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

## Añadir configuración del servidor
Para que Apache muestre nuestra Aplicación debemos generar la configuración del servidor de nuestra aplicación. 

Pega la siguiente configuración al final del archivo **httpd.conf**, haciendo modificaciones respectivas según tu aplicación (puerto, servername, ruta del archivo *.wsgi* y de la carpeta del proyecto)   

```
<VirtualHost *:5001>
	ServerName localhost
	WSGIScriptAlias /mi_app C:/xampp/htdocs/mi_app/app.wsgi

	<Directory C:/xampp/htdocs/mi_app>
		Options FollowSymLinks
		AllowOverride None
		Require all granted
	</Directory>
</VirtualHost>
```

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

## Archivos del proyecto
Nuestro proyecto debe incluir el archivo principal de nuestra aplicación, generalmente *app.py*, que define nuestra aplicación Flask y además incluir un archivo *.wsgi* que funcionará como el archivo de entrada para nuestro servidor Apache.

### mi_app.wsgi
Crea un archivo *.wsgi* con el nombre de tu aplicación y añade el siguiente contenido:

```
import sys

sys.path.insert(0, 'C:\\xampp\\htdocs\\mi_app')

from app import app as application
```

El archivo es básicamente código python, que importa la aplicación flask (*app*) del archivo principal (*app.py*) con el nombre de *application*. Las primeras lineas definen a la ruta del proyecto como la primera ruta en la cual buscar los modulos importados, en este caso la importación de *app*.

# app.py
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



VERIFICA QUE APACHE FUNCIONA DESPUES DE CADA PASO. PARA VERIFICAR CUANDO Y POR QU� DEJA DE FUNCIONAR

---------- issue https://github.com/GrahamDumpleton/mod_wsgi/issues/835#issue-1687776735 ---------

set the environment variable MOD_WSGI_APACHE_ROOTDIR to the directory containing the Apache distribution. Ensure you use forward slashes in the directory path

Also be aware that xampp distributions of Apache often don't work as they lack the required DLL import libraries needed when compiling the Apache module. That is a separate issue though. The ApacheLounge distribution of Apache is what is recommended.

sys.path es una lista que define las rutas en las cuales python buscar� las importaciones de modulos (archivos de python), en ese sentido .insert(0, <ruta>) define la primera ruta a utilizar, mientras que .append(<ruta>) la a�ade pero al final de la lista 
------------- -------------------
<mi_app> C:/xampp/htdocs/mi_app C:\xampp\htdocs\mi_app

error: Microsoft Visual C++ 14.0 or greater is required
https://visualstudio.microsoft.com/visual-cpp-build-tools/

RuntimeError: No Apache installation can be found.
set MOD_WSGI_APACHE_ROOTDIR=C:\xampp\apache
set MOD_WSGI_APACHE_ROOTDIR=C:/xampp/apache

C:\xampp\apache\bin\httpd.exe -k install


indian guy video tutorial

# app.wsgi
import sys
import os

sys.path.append(<path to app dir>) # \\ double backslash

from app import app as application

# app.py


# get load module config and paste on httpd.conf before any loadmodule right after listen port
# paths use "quotes" and forward slash "C:/..."

# creates separate mi_app.conf file. # localhost or 127.0.0.1 or IP address

WSGIApplicationGroup %{GLOBAL}
<VirtualHost *:80>
	ServerName localhost
	WSGIScriptAlias /mi_app C:/xampp/htdocs/mi_app/app.wsgi
	
	<Directory C:/xampp/htdocs/mi_app>
		Options FollowSymLinks
		AllowOverride None
		Require all granted
	</Directory>
</VirtualHost>

# Include mi_app.conf file. Gu�ate de los otros Include conf/extra para verificar
Include conf/extra/mi_app.conf 

# Add Listen port and ServerName to httpd.conf. Verify servername and listen syntax
Listen <port>
ServerName <address>:<port>




------------------ Page issues ----------
You need to use double backslashes in your web.wsgi file:
sys.path.insert(0, 'D:\\Tirumalesh\\dev\\text_basic')


------------- Me testing ------------
Las rutas en la configuracion de virtualhost funcionan de ambas formas con y sin comillas
Las rutas en la configuracion de virtualhost funcionan de ambas formas con slash de frente y hacia atr�s
En el archivo .wsgi ambas sys.path.append(<ruta>) y sys.path.insert(0, <ruta>) funcionan
Si hay Listen <puerto> pero no hay ServerName:<puerto> FUNCIONA
Si no hay Listen <puerto> NO FUNCIONA
Utilizando el mismo puerto que apache (80) y WSGIScriptAlias / FUNCIONA el servidor de la app se sobrepone al de apache
Python instalado para todos los usuarios FUNCIONA
Python instalado para el usuario FUNCIONA
Apache NO instalado como servicio FUNCIONA A VECES SI A VECES NO. Tuve un error que se soluciono al instalar apache como servicio, aunque luego lo volv� a desinstalar y mod_wsgi instalaba igual, as� que no s� bien. Pero me da la sensacion que es mejor hacer el paso de instalar apache como servicio.



