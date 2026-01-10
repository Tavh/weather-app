from werkzeug.exceptions import BadRequest, Unauthorized
from app.dtos.auth_dto import UserRegister, UserLogin, AuthResponse
from app.models.user import User
from app.data.user_repository import UserRepository
from app.core.security import hash_password, check_password, create_access_token
from app.core.config import Config

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register_user(self, dto: UserRegister) -> None:
        try:
            if self.user_repo.get_by_username(dto.username):
                raise BadRequest(description="Username already exists")
            
            hashed = hash_password(dto.password)
            new_user = User(username=dto.username, password_hash=hashed)
            self.user_repo.create(new_user)
        finally:
            self.user_repo.close()

    def login_user(self, dto: UserLogin) -> AuthResponse:
        try:
            user = self.user_repo.get_by_username(dto.username)
            if not user or not check_password(dto.password, user.password_hash):
                raise Unauthorized(description="Invalid credentials")
            
            # Create Token
            token = create_access_token(user_id=user.id)
            return AuthResponse(
                access_token=token,
                token_type="Bearer",
                expires_in=Config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )
        finally:
            self.user_repo.close()
