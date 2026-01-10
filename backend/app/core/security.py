
from typing import Dict, Any

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
    # TODO: Implement JWT decoding with PyJWT
    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    #     return payload
    # except jwt.ExpiredSignatureError:
    #     raise OAuthProblem('Token expired')
    # except jwt.InvalidTokenError:
    #     raise OAuthProblem('Invalid token')
    
    return {'sub': 'stub_user_id', 'scope': ''}

def hash_password(password: str) -> str:
    # TODO: Implement hashing (e.g. argon2)
    return "hashed_stub"

def check_password(password: str, hashed: str) -> bool:
    # TODO: Verify password
    return True
