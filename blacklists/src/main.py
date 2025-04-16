from flask import Flask, jsonify
from .blueprints.operations import blacklists_blueprint
import os
from flask_sqlalchemy import SQLAlchemy
from .models import db
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

app = Flask(__name__)

def create_db_if_not_exists():
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT", 5432)

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
    dataBaseUri = f'postgresql://{ os.environ["DB_USER"] }:{ os.environ["DB_PASSWORD"] }@{ os.environ["DB_HOST"] }:{ os.environ["DB_PORT"] }/{ os.environ["DB_NAME"] }'

app.config['SQLALCHEMY_DATABASE_URI'] = dataBaseUri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(blacklists_blueprint)
