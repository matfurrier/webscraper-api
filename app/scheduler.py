import os
import logging
import asyncio # Added for asyncio.run if needed, but direct await should work with FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from app.scraper import scrape_cepea_soja
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler(daemon=True)

async def schedule_job(): # Changed to async
    """Schedules the scraping job."""
    scrape_interval_hours = int(os.getenv("SCRAPE_INTERVAL_HOURS", "12"))
    logger.info(f"Scheduling scrape job to run every {scrape_interval_hours} hours.")
    
    logger.info("Attempting initial scrape job...")
    try:
        await scrape_cepea_soja() # Changed to await
    except Exception as e:
        logger.error(f"Initial scrape job failed: {e}", exc_info=True)

    # APScheduler should handle the async function scrape_cepea_soja directly
    scheduler.add_job(scrape_cepea_soja, 'interval', hours=scrape_interval_hours, id="cepea_soja_scraper", replace_existing=True)
    
    if not scheduler.running:
        try:
            scheduler.start()
            logger.info("Scheduler started.")
        except (KeyboardInterrupt, SystemExit):
            logger.info("Scheduler stopped on interrupt.")
            if scheduler.running:
                 scheduler.shutdown()
        except Exception as e:
            logger.error(f"Error starting scheduler: {e}", exc_info=True)

def stop_scheduler():
    if scheduler.running:
        try:
            scheduler.shutdown()
            logger.info("Scheduler shutdown successfully.")
        except Exception as e:
            logger.error(f"Error during scheduler shutdown: {e}", exc_info=True)
    else:
        logger.info("Scheduler was not running.") 