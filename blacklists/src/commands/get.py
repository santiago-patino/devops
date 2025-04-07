from .base_command import BaseCommannd
from ..models import Blacklists, db
from ..errors.errors import IncompleteOrInvalidFields, TokenNotFound, InvalidToken
from datetime import datetime
import os

class Get(BaseCommannd):
  
  TOKEN = os.getenv("TOKEN")
  
  def __init__(self, auth, email):
    self.auth = auth
    self.email = email
  
  def execute(self):
    
    if not self.auth:
      return {'message': TokenNotFound.description, 'code': TokenNotFound.code}
      
    token = self.auth.split(" ")[1] if " " in self.auth else None
    
    if not token or token != self.TOKEN:
      return {'message': InvalidToken.description, 'code': InvalidToken.code}

    if not self.email:
      return {'message': IncompleteOrInvalidFields.description, 'code': IncompleteOrInvalidFields.code}

    email_data = Blacklists.query.filter((Blacklists.email == self.email)).first()

    email_return = {
        'exist': bool(email_data)
    }
    
    if email_data:
      email_return['blocked_reason'] = email_data.blocked_reason
    
    return {'message': email_return, 'code': 200 }