import io
import os
import tempfile

import pytest
import pandas as pd

from settings import settings
from src.boto3_client import Boto3Client
from src.upload_s3_file import upload_s3_file
from utils.get_timestamp import get_timestamp


@pytest.fixture(scope="module", autouse=True)
def set_up(localstack_container):
    with Boto3Client("s3") as s3_client:
        s3_client.create_bucket(
            Bucket=settings.AWS_S3_BUCKET_NAME,
            CreateBucketConfiguration={
                "LocationConstraint": settings.AWS_DEFAULT_REGION
            },
        )
        waiter = s3_client.get_waiter("bucket_exists")
        waiter.wait(Bucket=settings.AWS_S3_BUCKET_NAME)


@pytest.fixture
def create_temp_csv_file(request) -> str:
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    temp_file.write(b"header1,header2\nvalue1,value2\n")
    temp_file.close()
    temp_path = temp_file.name

    def cleanup():
        if os.path.exists(temp_path):
            os.remove(temp_path)

    request.addfinalizer(cleanup)

    return temp_path


def test_upload_s3_file(create_temp_csv_file):
    temp_file_path = create_temp_csv_file

    upload_s3_file(temp_file_path)

    with Boto3Client("s3") as s3_client:
        file_name = os.path.basename(temp_file_path)
        s3_key = f"{settings.AWS_S3_BUCKET_PATH}/{get_timestamp()}/{file_name}"
        response = s3_client.get_object(Bucket=settings.AWS_S3_BUCKET_NAME, Key=s3_key)
        body = response["Body"].read()
        data = io.BytesIO(body)
        df = pd.read_csv(data)
        assert df.shape == (1, 2)
        assert list(df.columns) == ["header1", "header2"]
        assert df.loc[0, "header1"] == "value1"
        assert df.loc[0, "header2"] == "value2"
