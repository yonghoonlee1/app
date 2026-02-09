from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, BackgroundTasks
from services.pdf_uploader import run

app = FastAPI()

@app.post("/jobs/mahindra/brochures")
def run_brochure_job(background_tasks: BackgroundTasks):
    background_tasks.add_task(run)
    return {
        "status": "accepted",
        "message": "Mahindra brochure job started"
    }


