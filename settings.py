import os

class Settings:
    ENV_VARS = (
        "AWS_ENDPOINT_URL",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_DEFAULT_REGION",
        "AWS_S3_BUCKET_NAME",
        "AWS_S3_BUCKET_PATH",
        "LOG_LEVEL",
    )

    def __getattr__(self, name: str):
        if name in self.ENV_VARS:
            return os.environ.get(name)
        raise AttributeError(f"Environment variable {name} not found")

settings = Settings()