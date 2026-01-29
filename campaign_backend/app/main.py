from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.core.database import Base, engine
from app.core.scheduler import start_scheduler
from app.models import campaign, audience, analytics
from app.api.routes import campaigns, analytics as analytics_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Marketing Campaign Backend")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files configuration
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.on_event("startup")
def startup_event():
    start_scheduler()

@app.get("/")
def root():
    return {"message": "Marketing Campaign API is running"}

app.include_router(campaigns.router)
app.include_router(analytics_routes.router)
