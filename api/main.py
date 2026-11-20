import uuid
import json
import pika
import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

QUEUE_NAME = 'measurement.created'

def publish(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=json.dumps(message))
    connection.close()
    
class MeasurementIn(BaseModel):
    source_host: str
    target_host: str
    metric: str
    values_ms: list[float]

@app.get("/health")
def health():
    return {"status": "UP"}

@app.get('/jobs/{job_id}')
def get_job(job_id: str):
    job = r.hgetall('job:' + job_id)
    if not job:
        raise HTTPException(status_code = 404, detail='job not found')
    return job

@app.post('/measurements', status_code = 202)
def submit_measurements(body: MeasurementIn):
    job_id = 'job-' + uuid.uuid4().hex[:8]
    measurement_id = 'm-' + uuid.uuid4().hex[:8]

    job = {
        'job_id': job_id,
        'measurement_id': measurement_id,
        'status': 'queued',
    }
    r.hset('job:' + job_id, mapping=job)

    message = {
        'job_id': job_id,
        'measurement_id': measurement_id,
        'measurement': body.model_dump(),
    }
    publish(message)

    return job