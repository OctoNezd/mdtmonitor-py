# MDTMonitor

1. Copy settings: `cp settings.example.py settings.py`

2. Install FastAPI dependencies: `poetry install` (install poetry if you don't have it)

3. Switch into frontend folder, install npm project for frontend: `cd frontend && npm install`

4. Build frontend: `npm run build`

5. Launch server using `poetry run python3 -m uvicorn main:app --host 0.0.0.0`
