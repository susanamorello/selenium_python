# Scraping variables
BASE_URL = "https://news.ycombinator.com/"
PAGES_TO_SCRAPE = 2
data = []

HEADLESS = True
BROWSER = "firefox" # chrome | firefox | edge | safari

# User-agent by defect
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/139.0.0.0 Safari/537.36"
)