import os
import pytest
from testcontainers.localstack import LocalStackContainer

localstack = LocalStackContainer(image="localstack/localstack:2.0.1").with_services(
    "s3"
)


@pytest.fixture(autouse=True)
def localstack_container(request):
    localstack.start()

    os.environ["AWS_ENDPOINT_URL"] = localstack.get_url()
    os.environ["AWS_DEFAULT_REGION"] = localstack.region_name
    os.environ["AWS_ACCESS_KEY_ID"] = "testcontainers-localstack"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testcontainers-localstack"
    os.environ["AWS_S3_BUCKET_NAME"] = "test-bucket"
    os.environ["AWS_S3_BUCKET_PATH"] = "test/output"

    def remove_container():
        localstack.stop()

    request.addfinalizer(remove_container)
