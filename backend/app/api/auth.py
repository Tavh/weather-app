from typing import Dict, Tuple, Any
from app.services.auth_service import AuthService
from app.dtos.auth_dto import UserRegister, UserLogin, GenericMessage
from app.core.database import get_session

def register(body: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    with get_session() as session:
        auth_service = AuthService(session)
        
        # Validate and parse input
        request_dto = UserRegister(**body)
        
        auth_service.register_user(request_dto)
        
        # Create response
        response_dto = GenericMessage(message="User created successfully")
        return response_dto.model_dump(), 201

def login(body: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    with get_session() as session:
        auth_service = AuthService(session)
        
        # Validate and parse input
        request_dto = UserLogin(**body)
        
        response_dto = auth_service.login_user(request_dto)
        
        # Convert DTO -> Dict (Response Object)
        return response_dto.model_dump(), 200
