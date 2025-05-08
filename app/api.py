from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from app.db import get_all_data, get_data_by_id, ScrapedItemDB
from app.scraper import scrape_cepea_soja
from app.export import export_to_json_str, export_to_csv_str
import io
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/data", response_model=List[ScrapedItemDB])
async def read_all_data():
    """Returns all collected data."""
    return get_all_data()

@router.get("/data/{item_id}", response_model=ScrapedItemDB)
async def read_data_item(item_id: str):
    """Returns a specific item by ID."""
    item = get_data_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/scrape", status_code=202)
async def trigger_scrape(background_tasks: BackgroundTasks):
    """Triggers a manual scrape. Runs in the background."""
    logger.info("Manual scrape endpoint triggered.")
    
    # It's better to run the actual scraping in a background task
    # to avoid blocking the API response, especially if scraping takes time.
    # However, for simplicity with the current scraper, direct call might be okay
    # but a robust solution would use background_tasks.add_task(scrape_cepea_soja)
    # For now, let's keep it simple and call directly, then improve if needed.
    
    # Note: The current scrape_cepea_soja() saves to DB directly.
    # For an API, it might be better if it returned the data, and then API saves it.
    # But let's stick to current structure for now.
    
    # For a truly async operation that doesn't block, you'd typically use 
    # background_tasks.add_task(scrape_cepea_soja)
    # But since scrape_cepea_soja is synchronous and might take time, 
    # this will still block the worker until it completes.
    # A more advanced setup would use Celery or FastAPI's built-in background tasks properly.
    
    # For now, we will run it in a background task so the API returns immediately.
    background_tasks.add_task(scrape_cepea_soja)
    return {"message": "Scraping process initiated in the background."}


@router.get("/export/json")
async def export_json():
    """Downloads all data as a JSON file."""
    json_str = export_to_json_str()
    return JSONResponse(
        content=json_str,  # Pass the string directly
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=data.json"}
    )

@router.get("/export/csv")
async def export_csv():
    """Downloads all data as a CSV file."""
    csv_str = export_to_csv_str()
    return StreamingResponse(
        io.StringIO(csv_str),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=data.csv"}
    ) 