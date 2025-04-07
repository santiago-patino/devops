from src.commands.add import Add
from src.errors.errors import IncompleteOrInvalidFields, InvalidToken, TokenNotFound, InvalidAppUuid
import json
from src.main import app
class TestAdd():
    
  emailData = {
    "email": "destinee36@yahoo.com",
    "app_uuid": "f8938825-34ed-4b6f-9673-82f9f1bcbf79",
    "blocked_reason": "fraud"
  }
    
  def test_add_email_without_fields(self):
      result = Add('Bearer secret', {}).execute()
      assert result['code'] == IncompleteOrInvalidFields.code
      assert result['message'] == IncompleteOrInvalidFields.description
  
  def test_add_email_without_token(self):
      result = Add('Bearer 123', {}).execute()
      assert result['code'] == InvalidToken.code
      assert result['message'] == InvalidToken.description
  
  def test_add_email_without_auth(self):
      result = Add(None, {}).execute()
      assert result['code'] == TokenNotFound.code
      assert result['message'] == TokenNotFound.description
      
  def test_add_email_invalid_uuidd(self):
      data = self.emailData
      data['app_uuid'] = 'invalid-uuid'
      result = Add('Bearer secret', data).execute()
      assert result['code'] == InvalidAppUuid.code
      assert result['message'] == InvalidAppUuid.description