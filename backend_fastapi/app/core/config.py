import os


class Settings:
    app_name: str = os.getenv("EMOCHAT_APP_NAME", "EmoChat API")
    app_description: str = os.getenv(
        "EMOCHAT_APP_DESCRIPTION",
        "Emotion chat backend with layered architecture.",
    )
    cors_origins = ["*"]


settings = Settings()

