Create an environment. Create a project folder and a .venv folder within
python3 -m venv .venv

Activate the environment
. .venv/bin/activate

Install Flask
pip install Flask

run the application
flask --app hello run
if the file is named app.py or wsgi.py, you don’t have to use --app

Debug Mode
flask --app WHERE_TO_FIND_IT run --debug

Variable Rules
variable sections to a URL by marking sections with <variable_name> or <converter:variable_name>

string:  any text without a slash
int: positive integers
float: floating point values
path: like string but also accepts slashes
uuid: accepts UUID strings


Install Flask-MySQLdb
First, you may need to install some dependencies for mysqlclient if you don't already have them, see [here](https://github.com/PyMySQL/mysqlclient#install).

Second, install Flask-MySQLdb:
pip install flask-mysqldb