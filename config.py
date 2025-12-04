

import os
from pathlib import Path


class Config:

    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-key")

    BASE_DIR: Path = Path(__file__).resolve().parent
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'app.db'}",
    )

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False