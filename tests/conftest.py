import os

import pytest
from testcontainers.localstack import LocalStackContainer

from settings import settings

localstack = LocalStackContainer(image="localstack/localstack:2.0.1")


@pytest.fixture(scope="session", autouse=True)
def set_envs():
    os.environ["AWS_ACCESS_KEY_ID"] = "testcontainers-localstack"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testcontainers-localstack"


@pytest.fixture(scope="session", autouse=True)
def set_settings():
    settings.AWS_S3_BUCKET_NAME = "test-bucket"
    settings.AWS_S3_BUCKET_PATH = "test/output"


@pytest.fixture(scope="module")
def localstack_container(request):
    localstack.start()

    settings.AWS_ENDPOINT_URL = localstack.get_url()
    settings.AWS_DEFAULT_REGION = localstack.region_name

    def remove_container():
        localstack.stop()

    request.addfinalizer(remove_container)
