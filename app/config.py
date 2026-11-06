import os
APP_NAME = "Avito Clone"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./avito.db")
CORS_ORIGINS = ["*"]
