from src.main import app
import json
import os
from unittest.mock import patch

class TestBlacklists():
  
  emailData = {
    "email": "destinee36@yahoo.com",
    "app_uuid": "f8938825-34ed-4b6f-9673-82f9f1bcbf79",
    "blocked_reason": "fraud"
  }
  
  @patch('src.commands.reset.Reset.execute')
  def reset_database(self, mock_reset):
    
    mock_reset.return_value = {
        'status_code': 200,
        'msg': 'Todos los datos fueron eliminados'
    }
    
    with app.test_client() as test_client:
      response = test_client.post('/blacklists/reset')
      assert response.status_code == 200
    
  @patch('src.commands.add.Add.execute')
  def add_email(self, mock_create, test_case='default'):
    
    mock_create.return_value = {
        'code': 200,
        'message': 'Email registrado correctamente'
    }
    
    with app.test_client() as test_client:
      response = test_client.post(
        '/blacklists',
        json=self.emailData
      )
      response_json = json.loads(response.data)
      return {'response_json': response_json, 'response': response}
      
  def test_add_email(self):
     
    with app.test_client() as test_client:
      add_email = self.add_email()
      
      assert add_email['response'].status_code == 201
      
    self.reset_database()

  def test_get_email(self):
        
    with patch('src.commands.get.Get.execute') as mock_get_email:
        mock_get_email.return_value = {
            'code': 200,
            'message': {
                'exist': True,
                'blocked_reason': 'fraud'
            }
        }

        response = app.test_client().get(
            f'/blacklists/{self.emailData["email"]}',
        )
        response_json = json.loads(response.data)
            
        assert response.status_code == 200
        assert 'exist' in response_json

    self.reset_database()

  def test_ping(self):
    with app.test_client() as test_client:
      response = test_client.get('/blacklists/ping')
      response_json = json.loads(response.data)
      
      assert response.status_code == 200
      assert response_json == 'pong'
