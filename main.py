from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests
from io import BytesIO
from azure.storage.blob import BlobServiceClient, ContentSettings

app = FastAPI(title="PDF to Azure Blob Uploader")


print("AZURE_STORAGE_CONNECTION_STRING =", os.getenv("AZURE_STORAGE_CONNECTION_STRING"))

# Blob Storage 설정 (실서비스에선 환경변수로 빼는 걸 권장)
CONNECT_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")


CONTAINER_NAME = "docs"

blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)


# 요청 Body 모델
class PdfUploadRequest(BaseModel):
    url: str
    blob_name: str


@app.post("/upload/pdf-from-url")
def upload_pdf_from_url(req: PdfUploadRequest):
    try:
        # 1. PDF 다운로드
        response = requests.get(req.url, timeout=30)
        response.raise_for_status()

        pdf_bytes = BytesIO(response.content)

        # 2. Blob 업로드
        container_client.upload_blob(
            name=req.blob_name,
            data=pdf_bytes,
            overwrite=True,
            content_settings=ContentSettings(content_type="application/pdf")
        )

        return {
            "status": "success",
            "message": "PDF uploaded to Blob Storage",
            "blob_name": req.blob_name
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"PDF download failed: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
