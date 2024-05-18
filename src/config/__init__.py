from pathlib import Path

from pydantic import BaseConfig, BaseModel, BaseSettings
import aiomysql
from pydantic import BaseSettings
import aiomysql
from dotenv import load_dotenv
import os

# Database Settings
load_dotenv(".env.local")

# API Settings


class APIUrlsSettings(BaseModel):
    """Configure public urls."""

    docs: str = "/docs"
    redoc: str = "/redoc"


class PublicApiSettings(BaseModel):
    """Configure public API settings."""

    name: str = "Backend"
    urls: APIUrlsSettings = APIUrlsSettings()


class DatabaseSettings(BaseSettings):
    name: str = os.getenv("MYSQL_DATABASE", "tts_db")
    host: str = os.getenv("MYSQL_HOST", "localhost")
    port: int = int(os.getenv("MYSQL_PORT", 3306))
    user: str = os.getenv("MYSQL_USER", "root")
    password: str = os.getenv("MYSQL_PASSWORD", "12345678")

    @property
    def url(self) -> str:
        return f"mysql+aiomysql://root:{self.password}@{self.host}:{self.port}/{self.name}"

    async def connect(self):
        return await aiomysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.name
        )


class KafkaSettings(BaseModel):
    bootstrap_servers: str = "localhost:9092"


# Logging Settings
class LoggingSettings(BaseModel):
    """Configure the logging engine."""

    # The time field can be formatted using more human-friendly tokens.
    # These constitute a subset of the one used by the Pendulum library
    # https://pendulum.eustace.io/docs/#tokens
    format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level: <5} | {message}"

    # The .log filename
    file: str = "backend"

    # The .log file Rotation
    rotation: str = "1MB"

    # The type of compression
    compression: str = "zip"


class AccessTokenSettings(BaseModel):
    secret_key: str = "your-secret-key"
    ttl: int = 100  # seconds


class RefreshTokenSettings(BaseModel):
    secret_key: str = "your-secret-key"
    ttl: int = 100  # seconds


class AuthenticationSettings(BaseModel):
    access_token: AccessTokenSettings = AccessTokenSettings()
    refresh_token: RefreshTokenSettings = RefreshTokenSettings()
    algorithm: str = "HS256"
    scheme: str = "Bearer"


# Settings are powered by pydantic
# https://pydantic-docs.helpmanual.io/usage/settings/
class Settings(BaseSettings):
    debug: bool = True

    # Project file system
    root_dir: Path
    src_dir: Path

    # Infrastructure settings
    database: DatabaseSettings = DatabaseSettings()

    # Application configuration
    public_api: PublicApiSettings = PublicApiSettings()
    logging: LoggingSettings = LoggingSettings()
    authentication: AuthenticationSettings = AuthenticationSettings()

    class Config(BaseConfig):
        env_nested_delimiter: str = "__"
        env_file: str = ".env"


# Define the root path
# --------------------------------------
ROOT_PATH = Path(__file__).parent.parent

# ======================================
# Load settings
# ======================================
settings = Settings(
    # NOTE: We would like to hard-code the root and applications directories
    #       to avoid overriding via environment variables
    root_dir=ROOT_PATH,
    src_dir=ROOT_PATH / "src",
)
