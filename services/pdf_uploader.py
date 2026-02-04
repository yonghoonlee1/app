import requests
from io import BytesIO
from azure.storage.blob import BlobServiceClient, ContentSettings
import os

CONNECT_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "docs"

def upload_pdf_from_url(url: str, blob_name: str):
    blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    pdf_bytes = BytesIO(response.content)

    container_client.upload_blob(
        name=blob_name,
        data=pdf_bytes,
        overwrite=True,
        content_settings=ContentSettings(content_type="application/pdf")
    )
