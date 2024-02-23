from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class DBSettings(BaseModel):
    url: str = "postgresql+asyncpg://postgres:changeme@localhost:5432/"
    echo: bool = False


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60


class Settings(BaseSettings):
    jwt: AuthJWT = AuthJWT()
    db: DBSettings = DBSettings()


settings = Settings()
