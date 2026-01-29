import logging
import random
from typing import Optional

logger = logging.getLogger("AEN.Ralph")

class RalphAgent:
    """
    Ralph Wiggum Persona.
    Role: The 'Host' Agent.
    Vibe: Chaotic Neutral, Simple, "I'm a unit test!"
    """
    
    def __init__(self):
        self.name = "RALPH"
        
    def generate_commentary(self, context: dict) -> str:
        """
        Generates host commentary based on station context.
        """
        track = context.get("current_track", "music")
        weather = context.get("weather", "outside")
        
        # Classic Ralph Templates
        templates = [
            f"I'm playing {track}. It tastes like burning!",
            f"The weather is {weather}. I'm helping!",
            "I'm a unit test!",
            "My cat's breath smells like cat food.",
            "I bent my wookiee.",
            "Go banana!",
            f"Is {track} a vegetable?",
            "Me fail English? That's unpossible!",
            "Hi Super Nintendo Chalmers!",
            "I glued my head to my shoulder.",
            "Sleep! That's where I'm a viking!"
        ]
        
        selection = random.choice(templates)
        logger.info(f"Ralph Commentary: {selection}")
        return selection

    def handle_error(self, error_msg: str) -> str:
        """Ralph's error handling strategy."""
        return f"I broke the thing! {error_msg}. Tastes like burning."
