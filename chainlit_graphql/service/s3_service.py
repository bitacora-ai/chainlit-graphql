import boto3
from tenacity import retry, stop_after_attempt, wait_fixed
from chainlit_graphql.core.config import settings


class S3Service:
    def __init__(self):
        self.s3_client = boto3.client("s3", region_name=settings.AWS_DEFAULT_REGION)

    def sync_generate_presigned_post(self, bucket_name, object_key, content_type):
        return self.s3_client.generate_presigned_post(
            bucket_name,
            object_key,
            Fields={"Content-Type": content_type},
            Conditions=[{"Content-Type": content_type}],
            ExpiresIn=3600,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
    async def generate_presigned_post(self, bucket_name, object_key, content_type):
        return self.sync_generate_presigned_post(bucket_name, object_key, content_type)

    def sync_generate_presigned_url(self, bucket_name, object_key):
        return self.s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=3600,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
    async def generate_presigned_url(self, bucket_name, object_key):
        return self.sync_generate_presigned_url(bucket_name, object_key)
