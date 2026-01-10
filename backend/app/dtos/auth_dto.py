from pydantic import BaseModel, Field

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, example="johndoe")
    password: str = Field(..., min_length=8, example="secret123")

class UserLogin(BaseModel):
    username: str = Field(..., example="johndoe")
    password: str = Field(..., example="secret123")

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = Field("Bearer", example="Bearer")
    expires_in: int = Field(..., description="Token expiration in seconds", example=3600)

class GenericMessage(BaseModel):
    message: str = Field(..., example="User created successfully")
