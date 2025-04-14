from fastapi import FastAPI, Request, HTTPException, status, Depends
from tasks.scraper_task import scrape_nba_task
from datetime import datetime
import os
from dotenv import load_dotenv
import secrets

app = FastAPI()

load_dotenv('./.env')

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "X-API-Key"

def verify_api_key(request: Request):
    client_key = request.headers.get(API_KEY_NAME)
    if not client_key or not secrets.compare_digest(client_key, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/scrape/{date}")
def scrape(date: str, _: None = Depends(verify_api_key)):
    try:
        # Validate format
        datetime.strptime(date, "%Y-%m-%d")
        games_json = scrape_nba_task(date)
        return games_json
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}
    except Exception as e:
        return {"error": str(e)}