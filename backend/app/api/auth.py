from typing import Dict, Tuple, Any
from app.services.auth_service import AuthService
from app.dtos.auth_dto import UserRegister, UserLogin, GenericMessage

# Initialize service
auth_service = AuthService()

def register(body: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    # Validate and parse input
    request_dto = UserRegister(**body)
    
    auth_service.register_user(request_dto)
    
    # Create response
    response_dto = GenericMessage(message="User created successfully")
    return response_dto.model_dump(), 201

def login(body: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    # Validate and parse input
    request_dto = UserLogin(**body)
    
    response_dto = auth_service.login_user(request_dto)
    
    # Convert DTO -> Dict (Response Object)
    return response_dto.model_dump(), 200
