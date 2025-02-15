import os
import jwt
from datetime import datetime,timedelta
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

token_secret = os.getenv("TOKEN_SECRET","default_secret")
refresh_token_secret = os.getenv("REFRESH_TOKEN_SECRET","default_refresh_secret")

# Expiring time for the tokens
ACCESS_TOKEN_EXPIRATION_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRATION_MINUTES", 15))
REFRESH_TOKEN_EXPIRATION_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRATION_DAYS", 7))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password,hashed_password)

# Create access token
def create_jwt_token(data: dict, expire_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expire_delta if expire_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MIN))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, token_secret, algorithm="HS256")

# Create a refresh token
def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRATION_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, refresh_token_secret, algorithm="HS256")

# Decode the access token
def decode_jwt_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, token_secret, algorithms=["HS256"])
        return decoded_token if decoded_token["exp"] >= int(datetime.utcnow().timestamp()) else None
    # Token expired
    except jwt.ExpiredSignatureError:
        return None
    # Token invalid
    except jwt.InvalidTokenError:
        return None


def decode_refresh_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, refresh_token_secret, algorithms=["HS256"])
        return decoded_token if decoded_token["exp"] >= int(datetime.utcnow().timestamp()) else None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None