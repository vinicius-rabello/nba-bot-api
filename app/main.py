from fastapi import FastAPI
from tasks.scraper_task import scrape_nba_task
from datetime import datetime

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/scrape/{date}")
def scrape(date: str):
    try:
        # Validate format
        datetime.strptime(date, "%Y-%m-%d")
        games_df = scrape_nba_task(date)
        return games_df.to_dict(orient="records")
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}
    except Exception as e:
        return {"error": str(e)}