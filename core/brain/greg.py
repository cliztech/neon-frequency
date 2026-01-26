import logging
from typing import TypedDict, Dict

logger = logging.getLogger("AEN.Greg")

class GregPersona:
    """
    Greg is the rival agent.
    Vibe: 90s Hip Hop, pretentious, hates 'fast electronic noise'.
    Role: Interrupts the broadcast to roast AEN.
    """
    
    def __init__(self):
        self.name = "GREG"
        
    def generate_interruption(self, current_track: str, host_last_words: str) -> str:
        """
        Generates a roast or interruption.
        In production, this would call an LLM with a specific 'Greg' system prompt.
        """
        logger.info(f"Greg is listening to {current_track}...")
        
        roasts = [
            "Yo AEN, cut this noise. We need some real Boom Bap.",
            "Is this music or a modem dial-up tone? Greg is not impressed.",
            "Sector 7G deserves better beats. This is tinny.",
            "Stop trying to be cool, AEN. You're just python code.",
            f"I heard you say '{host_last_words}'... cringe."
        ]
        
        import random
        return random.choice(roasts)
