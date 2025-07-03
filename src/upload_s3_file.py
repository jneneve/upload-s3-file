import logging
import os

from settings import settings
from src.boto3_client import Boto3Client
from utils.get_timestamp import get_timestamp

logger = logging.getLogger(__name__)


def build_s3_key(file_name: str) -> str:
    return f"{settings.AWS_S3_BUCKET_PATH}/{get_timestamp()}/{file_name}"


def upload_s3_file(file_path: str):
    logger.info(f"Uploading {file_path}")
    file_name = os.path.basename(file_path)
    s3_key = build_s3_key(file_name)
    with Boto3Client("s3") as s3_client:
        s3_client.upload_file(
            Filename=file_path,
            Bucket=settings.AWS_S3_BUCKET_NAME,
            Key=s3_key,
        )
    logger.info(f"Uploaded {file_path}")
