# Desplegar aplicación Flask en XAMPP Apache (Windows)

Para nuestro proyecto utilizaremos un entorno virtual, para trabajar de forma más organizada y eficiente, y con el paquete **mod_wsgi** que es el encargado de indicarle a nuestro servidor Apache como ejecutar nuestra aplicación Flask.

Este ejemplo asume lo siguiente:

- Nuestra Aplicación Flask se llama _mi_app_
- La ruta de nuestra instalación de Apache es _C:\xampp\apache_
- La carpeta de nuestra aplicación está ubicada en la carpeta _htdocs_ de XAMPP (_C:\xampp\htdocs\mi_app_)
- Nuestra aplicación utilizará el puerto _5001_

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

Nuestro proyecto debe incluir el archivo principal de nuestra aplicación, generalmente _app.py_, que define nuestra aplicación Flask y además incluir un archivo _.wsgi_ que funcionará como el archivo de entrada para nuestro servidor Apache.

### mi_app.wsgi

Crea un archivo _.wsgi_ con el nombre de tu aplicación, en este caso _mi_app.wsgi_, y añade el siguiente contenido:

```
import sys

sys.path.insert(0, 'C:\\xampp\\htdocs\\mi_app')

from app import app as application
```

El archivo es básicamente código python, que importa la aplicación flask (_app_) del archivo principal (_app.py_) con el nombre de _application_. Las primeras lineas definen a la ruta del proyecto como la primera ruta en la cual buscar los modulos importados, en este caso la importación de _app_.

### app.py

Este ejemplo define una aplicación Flask básica en un archivo _app.py_ con el siguiente contenido:

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

La instalación del paquete mod_wsgi la haremos en el entorno virtual de nuestro proyecto. Si tu entorno virtual se llama _.venv_ ejecuta el siguiente comando:

`.venv\Scripts\activate`

## Instalar mod_wsgi

Este es el paso que presenta más inconvenientes, habiendo seguido los pasos anteriores deberías estar tranquilo. Para la instalación del paquete se utilizarán tres directivas, la primera (_--require-virtualenv_) indica que la instalación sólo se realizará si el entorno virtual está activado, para evitar una instalación global; la segunda (_--no-cache-dir_) indica que se deshabilitará la caché para la instalación del paquete, para evitar una instalación posiblemente corrupta; y la tercera (_-U_) asegura que se instale la versión más reciente del paquete.

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

- Abre el archivo **httpd.conf** de Apache. Esto lo puedes hacer desde el botón config de Apache en XAMPP o desde la carpeta _conf_ del directorio de Apache.

- Dentro del archivo busca la última línea que contenga _LoadModule_

- Pega el texto de configuracion después de todos los _LoadModule_

## Añadir configuración del puerto de la aplicación

Debemos indicar a Apache el puerto que nuestra aplicación utilizará

Dentro de httpd.conf busca las líneas que digan _Listen_

Debajo de la ultima línea _Listen_ añade una línea para tu puerto:

`Listen 5001`

En este ejemplo el puerto es _5001_

## Añadir configuración de ServerName de nuestra aplicación

Siguiendo un proceso similar al anterior, debemos indicar a Apache el ServerName, o dominio, de nuestra aplicación. Este puede ser _localhost_, _127.0.0.1_, la dirección de nuestro computador, o un dominio real en caso de tenerlo.

Dentro de httpd.conf busca las línea que digan _ServerName_

Justo debajo de la ultima añade una linea para tu aplicación:

`ServerName localhost:5001`

En este ejemplo el ServerName es _localhost_ y el puerto es _5001_

## Añadir configuración VirtualHost del servidor

Para que Apache muestre nuestra Aplicación debemos generar la configuración del servidor de nuestra aplicación.

Pega la siguiente configuración al final del archivo **httpd.conf**, haciendo modificaciones respectivas según tu aplicación (puerto, servername, ruta del archivo _.wsgi_ y de la carpeta del proyecto)

```
<VirtualHost *:5001>
	ServerName localhost
	WSGIScriptAlias /mi_app C:/xampp/htdocs/mi_app/app.wsgi

	<Directory C:/xampp/htdocs/mi_app>
		Require all granted
	</Directory>
</VirtualHost>
```

### Configuración adicional

Dependiendo de los paquetes que tu aplicación utiliza puede que sea necesario añadir la siguiente línea dentro de la configuración del VirtualHost:  
`WSGIApplicationGroup %{GLOBAL}`

Esta configuración forza a la aplicación WSGI a ejecutarse en el interprete principal de Python, lo cual es necesario para dependencias que no se ejecutan en un sub-interprete de Python, el cual mod_wsgi usa por defecto. Un ejemplo de un error que esto soluciona es:

> ImportError: PyO3 modules compiled for CPython 3.8 or older may only be initialized once per interpreter process

## Voilà

Activa el servidor Apache, y accede a tu aplicación desde http://localhost:5001/mi_app, si todo ha salido bien, deberías ver un bonito mensaje en pantalla.

## Acceder desde la red local

Para acceder a nuestra aplicación desde otros dispositivos conectados a nuestra misma red debemos añadir las siguientes configuraciones.

### Obtener la dirección IP del servidor

Para acceder a nuestra aplicación es necesario conocer la dirección IP del servidor Apache. Desde el computador en el que está instalado nuestro servidor Apache ejecuta el siguiente comando en una ventana de CMD:

`ipconfig`

En la terminal debe aparecer una línea _Dirección IPV4_ con nuestra dirección IP que debe lucir algo así:

> Dirección IPv4. . . . . . . . . . . . . . : x.x.x.x

Copia la dirección IP, en este caso como ejemplo es _x.x.x.x_.

### Añadir nuestra dirección IP en el servidor Apache

Modifica las líneas de configuración que añadiste para la aplicación en el archivo _httpd.conf_, añadiendo la dirección IP:

Reemplaza la línea `Listen 5001` por `Listen x.x.x.x:5001`

Reemplaza la línea `ServerName localhost:5001` por `ServerName x.x.x.x:5001`

En la configuración VirtualHost del servidor, al final del archivo, reemplaza la línea `ServerName localhost` por `ServerName x.x.x.x`. De esta forma:

```
<VirtualHost *:5001>
  ServerName x.x.x.x
...
```

Reemplaza la dirección IP de ejemplo _x.x.x.x_ por tu dirección IP.

### Configuración de Firewall de windows

Debes configurar el firewall de windows para que permmita el acceso al servidor Apache a través de la red local.

- Abre el _Firewall de Windows_
- Ingresa a _Configuración avanzada_
- En el panel izquierdo ingresa en _Reglas de entrada_
- Busca las reglas que digan "_Apache HTTP Server_" y eliminalas
- En el panel derecho haz click en _Nueva regla_
- Elige la opción de **Puerto** y haz click en _siguiente_
- Selecciona las opciones de **TCP** y **Puertos específicos**, ingresa el número de puerto de tu aplicación en la casilla de texto y haz click en siguiente
- Selecciona **Permitir la conexión**
- Selecciona las casillas de **Dominio**, **Privado** y **Público**
- Añade un nombre de configuración, por ejemplo: _puerto_mi_app_
- Abre el Panel de Control de XAMPP y activa el servidor Apache
- En la ventana que se despliega del Firewall de Windows selecciona ambas casillas de **Redes privadas** y **Redes públicas**, y haz click en **Permitir acceso**
- Accede a la aplicación desde la dirección **x.x.x.x:5001** en el navegador desde un dispositivo conectado a la misma red, donde _x.x.x.x_ es la dirección del servidor Apache y _5001_ el puerto de tu aplicación

### Voilà x2
Ahora tienes tu aplicación Flask desplegada en un servidor Apache, disponible dentro de tu red local
