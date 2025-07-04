import boto3

from settings import settings


class Boto3Client:
    def __init__(self, service: str):
        self._client = boto3.client(
            service,
            endpoint_url=settings.AWS_ENDPOINT_URL,
            region_name=settings.AWS_DEFAULT_REGION,
        )

    def __enter__(self):
        return self._client

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        if exc_type:
            print(f"{exc_type}: {exc_value}")
        self._client.close()
        return False
