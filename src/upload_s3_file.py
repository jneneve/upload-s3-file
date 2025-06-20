import logging
import os

from settings import settings
from src.boto3_client import Boto3Client
from utils.get_timestamp import get_timestamp

logger = logging.getLogger(__name__)

def upload_s3_file(file_path: str) -> None:
    logger.info(f"Uploading {file_path}")
    s3_bucket_name = settings.AWS_S3_BUCKET_NAME
    s3_bucket_path = settings.AWS_S3_BUCKET_PATH
    file_name = os.path.basename(file_path)
    s3_key = build_s3_key(s3_bucket_path, file_name)
    with Boto3Client("s3") as s3_client:
        s3_client.upload_file(
            Filename=file_path,
            Bucket=s3_bucket_name,
            Key=s3_key,
        )
    logger.info(f"Uploaded {file_path}")

def build_s3_key(s3_bucket_path: str, file_name: str) -> str:
    return f"{s3_bucket_path}/{get_timestamp()}/{file_name}"