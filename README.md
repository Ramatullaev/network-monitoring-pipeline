# Network Monitoring Pipeline

A learning project: a small system that receives network measurements
(ping latency between hosts) and processes them step by step.

## What works now

- `GET /health` — check that the API is running
- `POST /measurements` — submit a measurement, get a job id back
- `GET /jobs/{job_id}` — check the job status

Jobs are stored in Redis, so they survive an API restart.

## How to run

1. Start Redis:

```
docker run -d --name redis -p 6379:6379 -v redis-data:/data redis:7 redis-server --appendonly yes
```

2. Install dependencies:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Start the API:

```
uvicorn api.main:app --reload
```

4. Open http://127.0.0.1:8000/docs

## Example request

```
curl -X POST http://127.0.0.1:8000/measurements -H "Content-Type: application/json" -d @examples/measurement.json
```