from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api import router as api_router
from app.scheduler import schedule_job, stop_scheduler, scheduler
import logging
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv() # Load .env variables

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="WebScraper API",
    description="API for collecting and serving scraped web data.",
    version="0.1.0"
)

# Setup for templates
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup...")
    try:
        await schedule_job() # Start the background scheduler and run initial scrape
        logger.info("Scheduler initialized and first job triggered.")
    except Exception as e:
        logger.error(f"Error during scheduler startup: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown...")
    stop_scheduler()
    logger.info("Scheduler stopped.")

app.include_router(api_router, prefix="/api") # Prefix all api routes with /api

@app.get("/dashboard", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    """Serves the simple data dashboard."""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/")
async def root():
    return {"message": "Welcome to the WebScraper API. Visit /docs for API documentation."}

if __name__ == "__main__":
    # This is for local development and testing directly with uvicorn
    # For Docker, gunicorn via uvicorn worker is often used (defined in Dockerfile CMD)
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port) 