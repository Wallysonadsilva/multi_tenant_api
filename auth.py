import os
import jwt
from datetime import datetime,timedelta
from passlib.context import CryptContext
from dotenv import load_dotenv
from sqlalchemy.util import deprecated

load_dotenv()

token_secret = os.getenv("TOKEN_SECRET","default_secret")

default_expiration = int(os.getenv("TOKEN_EXPIRATION_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_jwt_token(data: dict, expire_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expire_delta if expire_delta else timedelta(minutes=default_expiration))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, token_secret, algorithm="HS256")

def decode_jwt_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, token_secret, algorithms=["HS256"])
        return decoded_token if decoded_token["exp"] >= datetime.utcnow().timestamp() else None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
