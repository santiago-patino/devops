from flask import Flask, jsonify, request, Blueprint
from ..commands.add import Add
from ..commands.get import Get
from ..commands.reset import Reset
import os

blacklists_blueprint = Blueprint('blacklists', __name__)

@blacklists_blueprint.route('/blacklists', methods = ['POST'])
def add_email():
    auth_header = request.headers.get('Authorization')
    json = request.get_json()
    
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    json['ip_address'] = ip_address
    
    result = Add(auth_header, json).execute()
    return jsonify(result.get('message')), result.get('code')

@blacklists_blueprint.route('/blacklists/<string:email>', methods = ['GET'])
def get_email(email):
    auth_header = request.headers.get('Authorization')
    result = Get(auth_header, email).execute()
    return jsonify(result.get('message')), result.get('code')

@blacklists_blueprint.route('/blacklists/ping', methods = ['GET'])
def ping():
    return jsonify('pong'), 200

@blacklists_blueprint.route('/blacklists/reset', methods = ['POST'])
def reset_users():
    result = Reset().execute()
    return jsonify(result.get('message')), result.get('code')
