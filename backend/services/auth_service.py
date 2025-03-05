from datetime import datetime, timedelta, UTC
from jose import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from settings import get_settings
from database import get_db
from sqlalchemy.orm import Session

from models.user import User

settings = get_settings()
security = HTTPBearer()

class AuthService:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.token_expire_minutes = settings.TOKEN_EXPIRE_MINUTES

    def create_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(minutes=self.token_expire_minutes)
        to_encode.update({
            "exp": expire,
            "iat": datetime.now(UTC),
            "jti": os.urandom(8).hex(),
        })

        return jwt.encode(
            to_encode,
            self.secret_key,
            algorithm="HS256"
        )
    
    def verify_token(self, token: str):
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=["HS256"],
                options={"verify_exp": True}
            )

            if not all(key in payload for key in ["sub", "exp", "iat", "jti"]):
                raise HTTPException(status_code=403, detail="Invalid token")

            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.JWTError as e:
            print(e)
            raise HTTPException(status_code=403, detail="Error while decoding token")
    
    def verify_user(
        self, HTTPAuthorizationCredentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
    ):
        token = HTTPAuthorizationCredentials.credentials
        payload = self.verify_token(token)
        user_id = int(payload.get("sub"))
        user = User.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=403, detail="User logged out")
        return user


