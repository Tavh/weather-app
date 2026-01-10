from typing import Dict, Tuple, Any

# Stub controller for Auth

def register(body: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    return {"message": "Register stub"}, 201

def login(body: Dict[str, str]) -> Tuple[Dict[str, Any], int]:
    return {"access_token": "stub_token", "token_type": "Bearer", "expires_in": 3600}, 200
