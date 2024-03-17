from pydantic import BaseModel


class UploadFileRequest(BaseModel):
    fileName: str
    contentType: str
    threadId: str
