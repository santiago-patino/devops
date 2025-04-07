class ApiError(Exception):
    code = 422
    description = "Default message"

class IncompleteOrInvalidFields():
    code = 400
    description = "Campos incompletos y/o invalidos"
    
class ExistingEmail():
    code = 409
    description = "El email ya se encuentra registrado"
    
class TokenNotFound():
    code = 403
    description = "El token no está en el encabezado de la solicitud"
    
class InvalidToken():
    code = 401
    description = "El token no es válido o está vencido"
    
class InvalidAppUuid():
    code = 400
    description = "El app_uuid no tiene el formato correcto"
