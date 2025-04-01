import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables

# Default values may be provided for enviroment variables. So it works anyway
# All app.config configurations, grouped in a class. key=value format
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') # Usa una clave segura
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')
    
    MYSQL_CURSORCLASS = "DictCursor"
    
