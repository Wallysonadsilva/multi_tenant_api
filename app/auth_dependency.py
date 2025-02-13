from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from app.auth import decode_jwt_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    payload = decode_jwt_token(token)
    if not payload:
        raise credentials_exception
    return payload


