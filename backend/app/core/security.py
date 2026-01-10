
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
import jwt
from passlib.context import CryptContext
from connexion.exceptions import OAuthProblem
from app.core.config import Config

# Password context setup
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def decode_token(token: str) -> Dict[str, Any]:
    """
    Decodes the JWT token.
    Called by Connexion's security handler (x-bearerInfoFunc).
    
    Args:
        token (str): The Bearer token from the Authorization header.
    
    Returns:
        Dict[str, Any]: The decoded token payload if valid.
        
    Raises:
        OAuthProblem: If token is invalid or expired (Connexion handles the 401).
    """
    try:
        payload = jwt.decode(
            token, 
            Config.SECRET_KEY, 
            algorithms=[Config.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise OAuthProblem(description='Token expired')
    except jwt.InvalidTokenError:
        raise OAuthProblem(description='Invalid token')

def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a new JWT access token.
    
    Args:
        user_id (int): The subject of the token.
        expires_delta (timedelta, optional): Custom expiration time.
    
    Returns:
        str: Encoded JWT token.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=Config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "sub": str(user_id),
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    return encoded_jwt

def hash_password(password: str) -> str:
    """
    Hashes a plaintext password.
    """
    return pwd_context.hash(password)

def check_password(password: str, hashed: str) -> bool:
    """
    Verifies a password against a hash.
    """
    return pwd_context.verify(password, hashed)
