from settings import Settings
from datetime import datetime as dt, timedelta
from jose import jwt, JWTError

settings_jwt = Settings()

class JWTUtils:
    @staticmethod
    def generate_access_token(user_id: str):
        payload = {
            "user_id": user_id,
            "expire": (dt.utcnow() + timedelta(days=7)).timestamp()
        }
        encoded_jwt = jwt.encode(payload, settings_jwt.JWT_SECRET_KEY, algorithm=settings_jwt.JWT_ENCODE_ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def get_user_id_from_access_token(token: str) -> int:
        try:
            payload = jwt.decode(token, settings_jwt.JWT_SECRET_KEY, algorithms=[settings_jwt.JWT_ENCODE_ALGORITHM])
        except JWTError:
            raise "JWTError"
        if payload["expire"] < dt.utcnow().timestamp():
            raise "TokenExpired"
        return payload["user_id"]