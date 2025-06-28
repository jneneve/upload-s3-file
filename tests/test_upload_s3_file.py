import io
import os
import tempfile
import pytest
import pandas as pd

from settings import settings
from src.boto3_client import Boto3Client
from src.upload_s3_file import upload_s3_file
from utils.get_timestamp import get_timestamp


@pytest.fixture
def create_tmp_csv_file(request) -> str:
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    tmp_path = tmp_file.name

    tmp_file.write(b"header1,header2\nvalue1,value2\n")
    tmp_file.close()

    def cleanup():
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    request.addfinalizer(cleanup)

    return tmp_path


@pytest.fixture
def create_client_provider():
    return Boto3Client("s3")


def test_upload_s3_file(create_client_provider, create_tmp_csv_file) -> None:
    s3_bucket_name = settings.AWS_S3_BUCKET_NAME
    s3_bucket_path = settings.AWS_S3_BUCKET_PATH
    region = settings.AWS_DEFAULT_REGION

    tmp_csv_path = create_tmp_csv_file
    file_name = os.path.basename(tmp_csv_path)
    s3_key = f"{s3_bucket_path}/{get_timestamp()}/{file_name}"

    client_provider = create_client_provider

    with client_provider as s3_client:
        s3_client.create_bucket(
            Bucket=s3_bucket_name,
            CreateBucketConfiguration={"LocationConstraint": region},
        )
        waiter = s3_client.get_waiter("bucket_exists")
        waiter.wait(Bucket=s3_bucket_name)

        response = s3_client.head_bucket(Bucket=s3_bucket_name)

        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    upload_s3_file(tmp_csv_path)

    with client_provider as s3_client:
        response = s3_client.get_object(Bucket=s3_bucket_name, Key=s3_key)
        data = io.BytesIO(response["Body"].read())
        df = pd.read_csv(data)

        assert df.shape == (1, 2)
        assert list(df.columns) == ["header1", "header2"]
        assert df.loc[0, "header1"] == "value1"
        assert df.loc[0, "header2"] == "value2"
