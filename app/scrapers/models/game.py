from pydantic import BaseModel
from typing import Optional

class Game(BaseModel):
    game_id: str  # Hashed ID
    full_date: str  # String field for the full date (YYYY-MM-DD)
    game_time: str  # Game time as a string
    broadcaster: Optional[str]  # Broadcaster name as a string
    home_team: str  # Home team name as a string
    away_team: str  # Away team name as a string
    home_team_score: Optional[int]  # Home team score as an int
    away_team_score: Optional[int]  # Away team score as an int
    arena: str  # Arena name as a string
    city: str  # City name as a string
    state: str  # State name as a string