from flask import Flask, jsonify
from .blueprints.operations import blacklists_blueprint
import os
from flask_sqlalchemy import SQLAlchemy
from .models import db

app = Flask(__name__)

dataBaseUri = f'postgresql://{ os.environ["DB_USER"] }:{ os.environ["DB_PASSWORD"] }@{ os.environ["DB_HOST"] }:{ os.environ["DB_PORT"] }/{ os.environ["DB_NAME"] }'

app.config['SQLALCHEMY_DATABASE_URI'] = dataBaseUri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
        db.create_all()

app.register_blueprint(blacklists_blueprint)
