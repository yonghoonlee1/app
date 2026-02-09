import requests
from bs4 import BeautifulSoup
from io import BytesIO
from azure.storage.blob import BlobServiceClient, ContentSettings
import time
import re
import os

CONNECT_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "mahindra-pdf"

BASE_URL = "https://www.mahindrausa.com"
SERIES_LIST_URL = "https://www.mahindrausa.com/build-your-own/series/"

def run():
    blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

    series_urls = get_series_urls()
    print(f"발견된 시리즈 페이지 수: {len(series_urls)}")

    for series_url in series_urls:
        series_id = series_url.rstrip("/").split("/")[-1]

        try:
            pdf_urls = get_pdf_urls_from_series(series_url)
            if not pdf_urls:
                print(f"[{series_id}] PDF 없음")
                continue

            for pdf_url in pdf_urls:
                upload_pdf_to_blob(
                    pdf_url,
                    series_id,
                    container_client
                )
                time.sleep(1)

        except Exception as e:
            print(f"오류 ({series_id}): {e}")


def get_series_urls():
    html = requests.get(SERIES_LIST_URL, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")

    pattern = re.compile(r"^https://www\.mahindrausa\.com/series/[a-zA-Z0-9\-]+/$")
    urls = set()

    for a in soup.select("a[href]"):
        href = a["href"]
        if href.startswith("/"):
            href = BASE_URL + href
        if pattern.match(href):
            urls.add(href)

    return sorted(urls)


def get_pdf_urls_from_series(series_url):
    html = requests.get(series_url, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")
    return [a["href"] for a in soup.select("a[href$='.pdf']")]


def upload_pdf_to_blob(pdf_url, series_id, container_client):
    response = requests.get(pdf_url, timeout=20)
    response.raise_for_status()

    pdf_bytes = BytesIO(response.content)
    filename = pdf_url.split("/")[-1]

    container_client.upload_blob(
        name=filename,
        data=pdf_bytes,
        overwrite=True,
        content_settings=ContentSettings(content_type="application/pdf"),
        metadata={
            "brand": "mahindra",
            "series": series_id,
            "doc_type": "brochure"
        }
    )

    print(f"업로드 완료: {filename}")
