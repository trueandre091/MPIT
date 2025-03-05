from datetime import datetime, timedelta, UTC
import os
from dotenv import load_dotenv
from jose import jwt, JWTError
from typing import Optional, Dict, Any, Tuple

load_dotenv()

class TokenError:
    EXPIRED = "token_expired"
    INVALID_TYPE = "invalid_token_type"
    INVALID_SIGNATURE = "invalid_signature"
    MALFORMED = "malformed_token"

class TokenService:
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY")
        self.algorithm = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.refresh_token_expire_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Создать новый access token

        Args:
            data: Данные для включения в токен (например, {"sub": user.email})
            expires_delta: Срок действия токена (если не указан, берется из настроек)

        Returns:
            str: JWT токен
        """
        to_encode = data.copy()
        
        # Устанавливаем срок действия
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(minutes=self.access_token_expire_minutes)

        # Добавляем стандартные поля JWT
        to_encode.update({
            "exp": int(expire.timestamp()),  # Срок истечения в Unix timestamp
            "iat": int(datetime.now(UTC).timestamp()),  # Время создания в Unix timestamp
            "type": "access",  # Тип токена
            "jti": os.urandom(8).hex()  # Уникальный идентификатор токена
        })
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Создать новый refresh token

        Args:
            data: Данные для включения в токен (например, {"sub": user.email})
            expires_delta: Срок действия токена (если не указан, берется из настроек)

        Returns:
            str: JWT refresh токен
        """
        to_encode = data.copy()
        
        # Устанавливаем срок действия
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(days=self.refresh_token_expire_days)

        # Добавляем стандартные поля JWT
        to_encode.update({
            "exp": int(expire.timestamp()),  # Срок истечения в Unix timestamp
            "iat": int(datetime.now(UTC).timestamp()),  # Время создания в Unix timestamp
            "type": "refresh",  # Тип токена
            "jti": os.urandom(8).hex()  # Уникальный идентификатор токена
        })
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str, expected_type: Optional[str] = None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Проверить токен

        Args:
            token: JWT токен для проверки
            expected_type: Ожидаемый тип токена ("access" или "refresh")

        Returns:
            Tuple[Optional[Dict[str, Any]], Optional[str]]: (данные токена, код ошибки)
            Если токен валиден, код ошибки будет None
        """
        try:
            # Декодируем токен с проверкой срока действия
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm],
                options={"verify_exp": True}  # Явно включаем проверку срока действия
            )
            
            # Проверяем тип токена, если указан ожидаемый тип
            if expected_type and payload.get("type") != expected_type:
                return None, TokenError.INVALID_TYPE

            # Проверяем наличие обязательных полей
            if not all(key in payload for key in ["exp", "iat", "type", "jti"]):
                return None, TokenError.MALFORMED

            return payload, None

        except jwt.ExpiredSignatureError:
            return None, TokenError.EXPIRED
        except jwt.JWTError:
            return None, TokenError.INVALID_SIGNATURE

    def get_token_expiration(self, token: str) -> Optional[datetime]:
        """
        Получить время истечения токена

        Args:
            token: JWT токен

        Returns:
            Optional[datetime]: Время истечения токена или None, если токен недействителен
        """
        try:
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm],
                options={"verify_exp": False}  # Отключаем проверку срока действия
            )
            if "exp" in payload:
                return datetime.fromtimestamp(payload["exp"])
            return None
        except JWTError:
            return None

    def is_token_valid(self, token: str) -> Tuple[bool, Optional[str]]:
        """
        Проверить действительность токена

        Args:
            token: JWT токен

        Returns:
            Tuple[bool, Optional[str]]: (валидность токена, код ошибки если не валиден)
        """
        payload, error = self.verify_token(token)
        return payload is not None, error

# Создаем единственный экземпляр сервиса
token_service = TokenService() 