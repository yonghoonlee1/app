from services.pdf_uploader import upload_pdf_from_url
from datetime import datetime

PDF_LIST = [
    "https://www.mahindrausa.com/wp-content/uploads/2025/10/MAH-1100-Series-Brochure-Rev-2024-09-17.pdf"
]

def main():
    print("Batch job started")

    for url in PDF_LIST:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        blob_name = f"Mahindra_Brochure_{timestamp}.pdf"
        upload_pdf_from_url(url, blob_name)

    print("Batch job finished")


if __name__ == "__main__":
    main()
