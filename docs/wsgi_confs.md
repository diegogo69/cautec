https://dev.to/willmvs/flask-deployment-on-windows-139b

<VirtualHost *:80>
    ServerName flaskwill.com
    WSGIScriptAlias / C:/git/wsgi_scripts/yourapp.wsgi
    <Directory C:/git/yourapp>
        Require all granted
    </Directory>
</VirtualHost>


thilinamad MEDIUM https://thilinamad.medium.com/flask-app-deployment-in-windows-apache-server-mod-wsgi-82e1cfeeb2ed

<VirtualHost *:5000>
        ServerAdmin admin-name-here
        ServerName  server-name-here(e.g localhost:5000)
        WSGIScriptAlias / "D:/myapp/app/index/web.wsgi"
        DocumentRoot "D:/myapp/app"
        <Directory "D:/myapp/app/index">
                Order deny,allow
                Allow from all
                Require all granted
        </Directory>
        ErrorLog "D:/myapp/app/logs/error.log"
        CustomLog "D:/myapp/app/logs/access.log" common
</VirtualHost>


RIZAL MAULANA MEDIUM https://medium.com/swlh/serve-flask-app-with-xampp-apache-on-windows-4debb4eb0b91

<VirtualHost *:5000>
    ServerAdmin admin-name-here
    ServerName server-name-here (e.g:localhost:5000)
    WSGIScriptAlias / “F:/myapp/app/index/web.wsgi”

    DocumentRoot “F:/myapp”

    <Directory “F:/myapp/app/index”>
        Require all granted
        Options Indexes FollowSymLinks Includes ExecCGI
    </Directory>

    AddHandler wsgi-script .wsgi

    ErrorLog “F:/myapp/logs/error.log”
    CustomLog “F:/myapp/logs/access.log” common
</VirtualHost>


STACKOVERFLOW ANSWER 

<IfModule wsgi_module>
<VirtualHost *:5000>
    ServerName 127.0.0.1
    WSGIScriptAlias /myapp C:/Apache24/htdocs/flaskapp/my_app.wsgi

    <Directory C:/Apache24/htdocs/flaskapp>
        Options +Indexes +FollowSymLinks +Includes +ExecCGI
        Allow from all
        AllowOverride None
        Require all granted
    </Directory>

    ErrorLog "D:/var/logs/error.log"
    CustomLog "D:/var/logs/access.log" common
</VirtualHost>
</IfModule>


INDIAN GUY

WSGIApplicationGroup %{GLOBAL}
<VirtualHost *:80>
	ServerName 127.0.0.1
	WSGIScriptAlias /app C:/Users/shiva/Desktop/Channel/Flask_App/app.wsgi
	
	<Directory C:/Users/shiva/Desktop/Channel/Flask_App>
		Options FollowSymLinks
		AllowOverride None
		Require all granted
	</Directory>
</VirtualHost>

# prueba virtualhost config que me funcionó
<VirtualHost *:5001>
	ServerName localhost
	WSGIScriptAlias /prueba2 C:/xampp/htdocs/prueba2/app.wsgi
	
	<Directory C:/xampp/htdocs/prueba2>
		Options FollowSymLinks
		AllowOverride None
		Require all granted
	</Directory>
</VirtualHost>

MIA. APACHE 2.4

<VirtualHost *:5001>
    # ServerAdmin admin-name-here
    ServerName localhost
    WSGIScriptAlias /[my_app(or none)] [my_app.wsgi]

    <Directory [my_app]>
		# Options FollowSymLinks ExecCGI
		# AllowOverride None
        Require all granted
    </Directory>

    # AddHandler wsgi-script .wsgi

    # ErrorLog “[myapp]/logs/error.log”
    # CustomLog “[myapp]/logs/access.log” common
</VirtualHost>