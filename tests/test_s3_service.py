import pytest
from unittest.mock import patch
from chainlit_graphql.service.s3_service import S3Service


@pytest.fixture
def s3_service():
    with patch("boto3.client"):
        yield S3Service()


@pytest.mark.asyncio
@patch("chainlit_graphql.service.s3_service.S3Service.sync_generate_presigned_post")
async def test_generate_presigned_post(mock_sync, s3_service):
    # Setup
    bucket_name = "my-bucket"
    object_key = "my-object"
    content_type = "application/octet-stream"
    expected_result = {"url": "http://example.com", "fields": {}}
    mock_sync.return_value = expected_result

    # Exercise
    result = await s3_service.generate_presigned_post(
        bucket_name, object_key, content_type
    )

    # Verify
    assert result == expected_result
    mock_sync.assert_called_once_with(bucket_name, object_key, content_type)


@pytest.mark.asyncio
@patch("chainlit_graphql.service.s3_service.S3Service.sync_generate_presigned_url")
async def test_generate_presigned_url(mock_sync, s3_service):
    # Setup
    bucket_name = "my-bucket"
    object_key = "my-object"
    expected_result = "http://example.com"
    mock_sync.return_value = expected_result

    # Exercise
    result = await s3_service.generate_presigned_url(bucket_name, object_key)

    # Verify
    assert result == expected_result
    mock_sync.assert_called_once_with(bucket_name, object_key)
