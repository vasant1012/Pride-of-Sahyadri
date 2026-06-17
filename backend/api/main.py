from backend.api.routers import forts, recommend
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
sys.path.append("/home/vasant/projects/Pride-of-Sahyadri")

from backend.api.routers import search  # NOQA E402

app = FastAPI(title="Maharashtra Forts API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001", "*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def init_routes(app: FastAPI):
    app.include_router(forts.router, prefix="/forts", tags=["forts"])
    app.include_router(search.router, prefix="/search", tags=["search"])
    app.include_router(
        recommend.router, prefix="/recommend", tags=["recommend"])


init_routes(app)


@app.get("/")
def root():
    return {"msg": "Maharashtra Forts API — up and running"}
