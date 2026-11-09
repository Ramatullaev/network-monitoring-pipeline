import uuid

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# "Память" сервера job_id -> данные задачи 
jobs = {}

class MeasurementIn(BaseModel):
    source_host: str
    target_host: str
    metric: str
    values_ms: list[float]


@app.get("/health")
def health():
    return {"status": "UP"}

@app.post('/measurements', status_code = 202)
def submit_measurements(body: MeasurementIn):
    job_id = 'job-' + uuid.uuid4().hex[:8]
    measurement_id = 'm-' + uuid.uuid4().hex[:8]

    job = {
        'job_id': job_id,
        'measurement_id': measurement_id,
        'status': 'queued',
    }
    jobs[job_id] = job

    return job
    
    