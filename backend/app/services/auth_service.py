from sqlalchemy.orm import Session
from werkzeug.exceptions import BadRequest, Unauthorized
from app.dtos.auth_dto import UserRegister, UserLogin, AuthResponse
from app.models.user import User
from app.repo.user_repository import UserRepository
from app.core.security import hash_password, check_password, create_access_token
from app.core.config import Config

import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, session: Session):
        self.user_repo = UserRepository(session)

    def register_user(self, dto: UserRegister) -> None:
        if self.user_repo.get_by_username(dto.username):
            raise BadRequest(description="Username already exists")
        
        hashed = hash_password(dto.password)
        new_user = User(username=dto.username, password_hash=hashed)
        self.user_repo.create(new_user)

    def login_user(self, dto: UserLogin) -> AuthResponse:
        user = self.user_repo.get_by_username(dto.username)
        if not user or not check_password(dto.password, user.password_hash):
            logger.warning(f"Failed login attempt for username: {dto.username}")
            raise Unauthorized(description="Invalid credentials")
        
        # Create Token
        token = create_access_token(user_id=user.id)
        logger.info(f"Successful login for user_id={user.id}")
        return AuthResponse(
            access_token=token,
            token_type="Bearer",
            expires_in=Config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
