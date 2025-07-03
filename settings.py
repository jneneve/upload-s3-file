class Settings:
    AWS_ENDPOINT_URL: str = "http://localhost:4566"
    AWS_DEFAULT_REGION: str = "us-east-1"
    AWS_S3_BUCKET_NAME: str = "localstack-bucket"
    AWS_S3_BUCKET_PATH: str = "localstack/output"


settings = Settings()
