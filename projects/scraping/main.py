import logging
from datetime import datetime
from scraper import scrape_news
from utils import ensure_dir

# Configure logging for terminal output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)



def main():
    logging.info("=== Starting scraping of Hacker News ===")
    
    # Execute scraper
    df, screenshot_folder = scrape_news()

    # Create outputs folder
    ensure_dir("outputs")

    # Set timestamp for excel 
    ts_file = datetime.now().strftime("%y%m%d_%H%M") 
    output_path = f"outputs/news_{ts_file}.xlsx"

    # Save excel file
    df.to_excel(output_path, index=False)
    logging.info(f"Data saved in {output_path}")
    logging.info(f"Screenshots saved in {screenshot_folder}")
    logging.info("=== Process completed ===")

if __name__ == "__main__":
    main()