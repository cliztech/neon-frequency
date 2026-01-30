"""
ElevenLabs Voice Client
=======================
Handles text-to-speech generation for station personalities.
"""

import os
import logging
import httpx
from typing import Optional

logger = logging.getLogger("AEN.Voice")

class ElevenLabsClient:
    """
    Client for ElevenLabs API.
    Auto-detects API key or switches to Mock Mode.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        self.base_url = "https://api.elevenlabs.io/v1"
        self.default_voice = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM") # Rachel
        
        if not self.api_key:
            logger.warning("ElevenLabsClient: No API Key found. Switching to MOCK mode.")
            self.mock_mode = True
        else:
            self.mock_mode = False
            self.client = httpx.Client(
                base_url=self.base_url,
                headers={"xi-api-key": self.api_key},
                timeout=30.0
            )

    def generate(self, text: str, output_path: str = None) -> Optional[bytes]:
        """
        Generate audio from text.
        """
        logger.info(f"Generating voice for: '{text}'")
        
        if self.mock_mode:
            return self._mock_generate(text, output_path)
            
        try:
            # Call actual API
            response = self.client.post(
                f"/text-to-speech/{self.default_voice}",
                json={
                    "text": text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
                }
            )
            response.raise_for_status()
            audio_data = response.content
            
            if output_path:
                with open(output_path, "wb") as f:
                    f.write(audio_data)
                
            return audio_data
            
        except Exception as e:
            logger.error(f"ElevenLabs API successful generation failed: {e}")
            logger.info("Falling back to mock generation due to error.")
            return self._mock_generate(text, output_path)

    def _mock_generate(self, text: str, output_path: str = None) -> bytes:
        """Create a dummy MP3 file for testing."""
        logger.info("[MOCK] Generating silent MP3...")
        # A minimal valid MP3 frame (1 frame of silence)
        # This is just a placeholder sequence of bytes
        mock_mp3 = b'\xFF\xE3\x18\xC4\x00\x00\x00\x03\x48\x00\x00\x00\x00'
        
        if output_path:
            with open(output_path, "wb") as f:
                f.write(mock_mp3)
                
        return mock_mp3
