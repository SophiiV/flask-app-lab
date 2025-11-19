import os


class Config:
    """Base configuration class."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///data.sqlite",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Configuration for development mode."""

    DEBUG = True


class TestingConfig(Config):
    """Configuration for running tests."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Configuration for production deployment."""

    DEBUG = False


config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
