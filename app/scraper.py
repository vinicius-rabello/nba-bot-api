from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

def get_nba_games(date: str) -> pd.DataFrame:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    
    # Your actual scraping logic here
    # This is dummy content for now:
    time.sleep(2)  # simulate slow scrape
    games = [{"home": "Lakers", "away": "Warriors", "date": date}]
    
    driver.quit()
    return pd.DataFrame(games)
