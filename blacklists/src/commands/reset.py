from .base_command import BaseCommannd
from ..models import Blacklists, db

class Reset(BaseCommannd):
  def __init__(self):
    pass
  
  def execute(self):
    
    db.session.query(Blacklists).delete()
    db.session.commit()
    
    return {'message': {'msg': 'Todos los datos fueron eliminados'}, 'code': 200 }