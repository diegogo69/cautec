from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'usuarios.login' # login function
login_manager.login_message_category = 'info' # category of message generated at accesing a login required view without authentication
login_manager.login_message = 'Por favor inicie sesión en su cuenta para acceder'

mail = Mail()
