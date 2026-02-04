from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.pdf_uploader import upload_pdf_from_url

app = FastAPI(title="PDF to Azure Blob Uploader")

# 요청 Body 모델
class PdfUploadRequest(BaseModel):
    url: str
    blob_name: str


@app.post("/upload/pdf-from-url")
def upload_pdf(req: PdfUploadRequest):
    try:
        upload_pdf_from_url(req.url, req.blob_name)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

