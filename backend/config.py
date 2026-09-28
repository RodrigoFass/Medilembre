import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-in-production")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///medilembre.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Comma-separated list of frontend origins allowed by CORS
    CORS_ORIGINS = [
        o.strip()
        for o in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
        if o.strip()
    ]

    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "")


# Built-in fallbacks plus the placeholders from .env.example / README
DEFAULT_SECRETS = {
    "dev-secret-change-in-production",
    "dev-jwt-change-in-production",
    "troque-por-uma-chave-secreta-forte-minimo-32-chars",
    "troque-por-outra-chave-secreta-minimo-32-chars",
    "sua-chave-secreta-minimo-32-chars",
    "outra-chave-secreta-minimo-32-chars",
}
MIN_SECRET_LENGTH = 32


def validate_production_secrets(cfg) -> None:
    """Refuse to run in production with missing, default or short secrets."""
    problems = []
    for name in ("SECRET_KEY", "JWT_SECRET_KEY"):
        value = cfg.get(name) or ""
        if value in DEFAULT_SECRETS or len(value) < MIN_SECRET_LENGTH:
            problems.append(name)
    if problems:
        raise RuntimeError(
            "Configuração insegura para produção: defina "
            + " e ".join(problems)
            + f" no .env com pelo menos {MIN_SECRET_LENGTH} caracteres aleatórios."
        )


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "test-secret-key-at-least-32-chars-long!!"
    MAIL_SUPPRESS_SEND = True


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
