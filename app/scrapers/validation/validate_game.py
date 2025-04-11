from pydantic import ValidationError
from typing import Optional
from scrapers.models.game import Game

# Validate game function
def validate_game(game_data: dict) -> Optional[Game]:
    """
    Validates the game data against the Game Pydantic model.
    Returns a validated Game object if successful, otherwise returns None.
    """
    try:
        # Validate the game data using the Pydantic model
        game = Game(**game_data)
        return game
    except ValidationError as e:
        # Handle validation errors
        print(f"Validation error: {e}")
        return None