from src.commands.get import Get
from src.errors.errors import TokenNotFound, InvalidToken
import json
from src.main import app
from unittest.mock import patch

class TestGet():
  
  emailData = {
    "email": "destinee36@yahoo.com",
    "app_uuid": "f8938825-34ed-4b6f-9673-82f9f1bcbf79",
    "blocked_reason": "fraud"
  }
  
  def test_get_user_without_auth(self):
        result = Get({}, self.emailData['email']).execute()
        assert result['code'] == TokenNotFound.code
        assert result['message'] == TokenNotFound.description
        
  def test_get_user_without_token(self):
      result = Get("Bearer", self.emailData['email']).execute()
      assert result['code'] == InvalidToken.code
      assert result['message'] == InvalidToken.description
    
  @patch('src.commands.get.Get.execute')
  def test_get_email_not_exist(self, mock_execute):
    
    mock_execute.return_value = {
        'code': 200,
        'message': {
            'exist': False
        }
    }
    
    result = Get("Bearer secret", "email@gmail.com").execute()
    
    assert result['code'] == 200
    assert result['message'] == {'exist': False}
      
  @patch('src.commands.get.Get.execute')
  def test_get_email(self, mock_execute):
      
    mock_execute.return_value = {
        'code': 200,
        'message': {
            'exist': True
        }
    }
      
    result = Get("Bearer secret", self.emailData['email']).execute()
      
    assert result['code'] == 200
    assert result['message'] == {'exist': True}