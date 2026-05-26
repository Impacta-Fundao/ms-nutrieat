import os
from datetime import datetime, timedelta, timezone

import jwt
from flask import request


class AuthTokenException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class AuthUtils:
    @staticmethod
    def _secret_key():
        secret_key = os.getenv("JWT_SECRET_KEY") or os.getenv("SECRET_KEY")
        if not secret_key:
            raise AuthTokenException("JWT_SECRET_KEY não configurada")
        return secret_key

    @staticmethod
    def _now():
        return datetime.now(timezone.utc)

    @staticmethod
    def _access_expiration_minutes():
        return int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", "15"))

    @staticmethod
    def _refresh_expiration_days():
        return int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", "7"))

    @staticmethod
    def _encode_token(admin, token_type, expires_delta):
        issued_at = AuthUtils._now()
        payload = {
            "sub": str(admin.id),
            "cpf": admin.cpf,
            "type": token_type,
            "iat": issued_at,
            "exp": issued_at + expires_delta,
        }
        return jwt.encode(payload, AuthUtils._secret_key(), algorithm="HS256")

    @staticmethod
    def create_access_token(admin):
        expiration = timedelta(minutes=AuthUtils._access_expiration_minutes())
        return AuthUtils._encode_token(admin, "access", expiration)

    @staticmethod
    def create_refresh_token(admin):
        expiration = timedelta(days=AuthUtils._refresh_expiration_days())
        return AuthUtils._encode_token(admin, "refresh", expiration)

    @staticmethod
    def decode_token(token, expected_type):
        try:
            payload = jwt.decode(
                token,
                AuthUtils._secret_key(),
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError as exc:
            raise AuthTokenException("Token expirado") from exc
        except jwt.InvalidTokenError as exc:
            raise AuthTokenException("Token inválido") from exc

        if payload.get("type") != expected_type:
            raise AuthTokenException("Tipo de token inválido")

        return payload

    @staticmethod
    def extract_bearer_token():
        authorization = request.headers.get("Authorization", "")
        if not authorization.startswith("Bearer "):
            raise AuthTokenException("Token não informado")
        return authorization.removeprefix("Bearer ").strip()

    @staticmethod
    def build_auth_payload(admin, admin_payload):
        return {
            "admin": admin_payload,
            "access_token": AuthUtils.create_access_token(admin),
            "refresh_token": AuthUtils.create_refresh_token(admin),
            "token_type": "Bearer",
            "access_token_expires_in": AuthUtils._access_expiration_minutes() * 60,
            "refresh_token_expires_in": AuthUtils._refresh_expiration_days() * 24 * 60 * 60,
        }