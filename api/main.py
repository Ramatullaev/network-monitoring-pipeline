from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class MeasurementIn(BaseModel):
    source_host: str
    target_host: str
    metric: str
    values_ms: list[float]


@app.get("/health")
def health():
    return {"status": "UP"}

@app.post('/measurements')
def submit_measurements(body: MeasurementIn):
    return {'received': body}
    