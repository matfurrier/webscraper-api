import asyncio
import os
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from app.db import ScrapedItemCreate, save_data
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TARGET_URL = os.getenv("TARGET_URL", "https://www.cepea.esalq.usp.br/br/indicador/soja.aspx")

async def scrape_cepea_soja() -> str | None:
    """Scrapes soybean data from CEPEA website using Playwright."""
    logger.info(f"Starting Playwright scrape for {TARGET_URL}")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            logger.info(f"Navigating to {TARGET_URL}")
            await page.goto(TARGET_URL, timeout=60000) # Increased timeout for page load
            logger.info(f"Page content fetching for {TARGET_URL}")
            html = await page.content()
            await browser.close()
            logger.info(f"Browser closed for {TARGET_URL}")

            soup = BeautifulSoup(html, "html.parser")
            # The user suggested soup.find("table"). This might be too generic.
            # For CEPEA Soja, a more specific selector might be needed if the first table isn't the correct one.
            # Example: table = soup.find("table", id="IFT_ISP") or based on some other unique attribute.
            # Using the generic one for now as per user's code structure.
            table = soup.find("table") 

            if not table:
                logger.error("Data table not found on the page.")
                return None

            rows = table.find_all("tr")
            if len(rows) < 2: # Expecting at least one header and one data row
                 logger.warning("Table found, but it does not have enough rows (header + data).")
                 return None
            
            # The user's example extracts all rows after the header into a list of lists.
            # Previous scraper extracted specific fields from the first data row.
            # Adopting the new structure: a list of all cell data per row.
            extracted_table_data = []
            for row in rows[1:]: # Skip header row (index 0)
                cols = [col.get_text(strip=True) for col in row.find_all("td")]
                if cols: # Only add if there are columns
                    extracted_table_data.append(cols)

            if extracted_table_data:
                # Create ScrapedItem instance
                item_to_save = ScrapedItemCreate(
                    fonte=TARGET_URL,
                    dados={"tabela_completa": extracted_table_data}, # Storing the whole table as requested
                    # data_coleta is handled by default_factory in ScrapedItemCreate model
                )
                item_id = save_data(item_to_save)
                logger.info(f"Successfully scraped data using Playwright and saved with id: {item_id}. Rows found: {len(extracted_table_data)}")
                return item_id
            else:
                logger.warning("No data extracted from the table rows.")
                return None
    except Exception as e:
        logger.error(f"Error during Playwright scraping for {TARGET_URL}: {e}", exc_info=True)
        return None

if __name__ == "__main__":
    # For testing the scraper directly
    async def main_test():
        result_id = await scrape_cepea_soja()
        if result_id:
            logger.info(f"Test scrape successful, ID: {result_id}")
        else:
            logger.error("Test scrape failed.")
    asyncio.run(main_test()) 