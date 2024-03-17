from fastapi import APIRouter, HTTPException
from chainlit_graphql.schema.upload_file_request import UploadFileRequest
from chainlit_graphql.service.s3_service import S3Service
from chainlit_graphql.core.config import settings
import uuid
from botocore.exceptions import BotoCoreError

router = APIRouter(prefix="/upload", tags=["uploads"])


@router.post("/file")
async def generate_upload_url(upload_request: UploadFileRequest):
    s3_service = S3Service()  # Instantiate the S3Service
    bucket_name = settings.AWS_BUCKET_NAME
    object_key = f"{upload_request.threadId}/files/{uuid.uuid4()}"

    try:
        presigned_post = await s3_service.generate_presigned_post(
            bucket_name, object_key, upload_request.contentType
        )

        response = {
            "post": {
                "url": presigned_post["url"],
                "fields": presigned_post["fields"],
                "uploadType": "multipart",
            },
            "signedUrl": presigned_post["url"],
        }

        response["post"]["fields"]["bucket"] = bucket_name
        response["post"]["fields"]["Content-Type"] = upload_request.contentType

        return response
    except BotoCoreError as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating presigned URL: {str(e)}"
        )
