from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.api import router
import os

app = FastAPI(title="IvyLeague Connect API")

# Path to templates
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    # Serves the demo UI with cache-busting headers
    response = FileResponse(os.path.join(TEMPLATES_DIR, "index.html"))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

app.include_router(router, prefix="/api")
