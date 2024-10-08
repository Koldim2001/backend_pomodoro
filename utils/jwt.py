from settings import Settings
from fastapi import security, Security, HTTPException
from datetime import datetime as dt, timedelta
from jose import jwt, JWTError

class TokenExpired(Exception):
    detail = "Token has expired"

class TokenNotCorrect(Exception):
    detail = "Token is not correct"

settings_jwt = Settings()
reusable_oauth2 = security.HTTPBearer()

class JWTUtils:
    @staticmethod
    def generate_access_token(user_id: str):
        payload = {"user_id": user_id, "expire": (dt.utcnow() + timedelta(days=7)).timestamp()}
        encoded_jwt = jwt.encode(
            payload, settings_jwt.JWT_SECRET_KEY, algorithm=settings_jwt.JWT_ENCODE_ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def get_user_id_from_access_token(token: str) -> int:
        try:
            payload = jwt.decode(
                token, settings_jwt.JWT_SECRET_KEY, algorithms=[settings_jwt.JWT_ENCODE_ALGORITHM]
            )
        except JWTError:
            raise TokenNotCorrect
        if payload["expire"] < dt.utcnow().timestamp():
            raise TokenExpired
        return payload["user_id"]


def get_request_user_id(
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> int:
    try:
        user_id = JWTUtils.get_user_id_from_access_token(token.credentials)

    except TokenExpired as e:
        raise HTTPException(status_code=401, detail=e.detail)
    except TokenNotCorrect as e:
        raise HTTPException(status_code=401, detail=e.detail)
    return user_id
