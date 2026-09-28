import pytest

from config import Config, validate_production_secrets

STRONG = "x" * 40


def test_production_rejects_default_secrets():
    cfg = {"SECRET_KEY": Config.SECRET_KEY, "JWT_SECRET_KEY": Config.JWT_SECRET_KEY}
    with pytest.raises(RuntimeError, match="SECRET_KEY e JWT_SECRET_KEY"):
        validate_production_secrets(cfg)


def test_production_rejects_short_or_missing_secret():
    with pytest.raises(RuntimeError, match="JWT_SECRET_KEY"):
        validate_production_secrets({"SECRET_KEY": STRONG, "JWT_SECRET_KEY": "curta"})
    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        validate_production_secrets({"JWT_SECRET_KEY": STRONG})


def test_production_accepts_strong_secrets():
    validate_production_secrets({"SECRET_KEY": STRONG, "JWT_SECRET_KEY": STRONG + "y"})


def test_cors_origins_default(app):
    assert app.config["CORS_ORIGINS"] == ["http://localhost:3000"]


def test_production_rejects_env_example_placeholders():
    cfg = {
        "SECRET_KEY": "troque-por-uma-chave-secreta-forte-minimo-32-chars",
        "JWT_SECRET_KEY": "troque-por-outra-chave-secreta-minimo-32-chars",
    }
    with pytest.raises(RuntimeError):
        validate_production_secrets(cfg)
