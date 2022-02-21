from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import mdt
app = FastAPI()

app.include_router(mdt.router, prefix="/MDTMonitorEvent")

app.mount(
    "/", StaticFiles(directory="./frontend/dist/", html=True), name="static")
