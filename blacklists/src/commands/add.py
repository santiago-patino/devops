from .base_command import BaseCommannd
from ..errors.errors import IncompleteOrInvalidFields, ExistingEmail, TokenNotFound, InvalidToken, InvalidAppUuid
import uuid
import requests
import os
from ..models import Blacklists, db
from datetime import datetime
import re

class Add(BaseCommannd):
  
  TOKEN = os.getenv("TOKEN", "secret")
  
  def __init__(self, auth,data):
    self.auth = auth
    self.data = data
  
  def execute(self):
    
    if not self.auth:
      return {'message': TokenNotFound.description, 'code': TokenNotFound.code}
      
    token = self.auth.split(" ")[1] if " " in self.auth else None
    
    if not token or token != self.TOKEN:
      return {'message': InvalidToken.description, 'code': InvalidToken.code}
    
    if not self.data.get('email') or not self.data.get('app_uuid'):
      return {'message': IncompleteOrInvalidFields.description, 'code': IncompleteOrInvalidFields.code}
    
    if not self.is_valid_uuid(self.data.get('app_uuid')):
      return {'message': InvalidAppUuid.description, 'code': InvalidAppUuid.code}

    existing_email = Blacklists.query.filter((Blacklists.email == self.data['email'])).first()
    
    if existing_email:
      return {'message': ExistingEmail.description, 'code': ExistingEmail.code}
    
    new_email = Blacklists(
          email=self.data['email'],
          app_uuid=self.data['app_uuid'],
          ip_address=self.data['ip_address'],
    )

    if self.data['blocked_reason']:
      new_email.blocked_reason = self.data['blocked_reason']
      
    db.session.add(new_email)
    db.session.commit()

    return {'message': 'Email registrado correctamente', 'code': 200}
  
  def is_valid_uuid(self, uuid_str):
    pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89ab][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'
    return bool(re.match(pattern, uuid_str)) 
