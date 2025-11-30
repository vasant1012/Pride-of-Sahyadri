from fastapi import FastAPI
import sys
sys.path.append("/home/vasant/projects/Pride-of-Sahyadri")

from src.api.routers import forts, search, clustering, recommend  # NOQA E402

app = FastAPI(title="Maharashtra Forts API")


def init_routes(app: FastAPI):
    app.include_router(forts.router, prefix="/forts", tags=["forts"])
    app.include_router(search.router, prefix="/search", tags=["search"])
    app.include_router(clustering.router,
                       prefix="/clusters", tags=["clustering"])
    app.include_router(
        recommend.router, prefix="/recommend", tags=["recommend"])


init_routes(app)


@app.get("/")
def root():
    return {"msg": "Maharashtra Forts API — up and running"}
