from flask import Flask, jsonify
from .blueprints.operations import blacklists_blueprint
import os
from flask_sqlalchemy import SQLAlchemy
from .models import db
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

app = Flask(__name__)

# Variables globales
db_name = os.getenv("DB_NAME", "blacklists")
db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "postgres")
db_host = os.getenv("DB_HOST", "database-1.ct080mawcvct.us-east-2.rds.amazonaws.com")
db_port = os.getenv("DB_PORT", "5432")

def create_db_if_not_exists():

    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}';")
        exists = cursor.fetchone()

        if not exists:
            print(f"⚙️  Creando base de datos '{db_name}'...")
            cursor.execute(f'CREATE DATABASE "{db_name}";')
        else:
            print(f"✅ La base de datos '{db_name}' ya existe.")

        cursor.close()
        connection.close()
    except Exception as e:
        print("❌ Error al verificar o crear la base de datos:", e)

if os.getenv("ENV") == "test":
    dataBaseUri = os.getenv("DATABASE_URI", "sqlite:///:memory:")
else:
    create_db_if_not_exists()
    dataBaseUri = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

app.config['SQLALCHEMY_DATABASE_URI'] = dataBaseUri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(blacklists_blueprint)
