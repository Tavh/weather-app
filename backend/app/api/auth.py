from typing import Dict, Tuple, Any
import logging
from app.services.auth_service import AuthService
from app.dtos.auth_dto import UserRegister, UserLogin, GenericMessage
from app.core.database import get_session

logger = logging.getLogger(__name__)

def register(body: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    with get_session() as session:
        auth_service = AuthService(session)
        request_dto = UserRegister(**body)
        
        logger.info(f"Attempting to register user: {request_dto.username}")
        auth_service.register_user(request_dto)
        logger.info(f"User registered successfully: {request_dto.username}")
        
        response_dto = GenericMessage(message="User created successfully")
        return response_dto.model_dump(), 201

def login(body: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    with get_session() as session:
        auth_service = AuthService(session)
        request_dto = UserLogin(**body)
        
        logger.info(f"Login attempt for user: {request_dto.username}")
        response_dto = auth_service.login_user(request_dto)
        logger.info(f"User logged in successfully: {request_dto.username}")
        
        return response_dto.model_dump(), 200
