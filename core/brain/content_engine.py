"""
Content Engine for Neon Frequency
==================================
AI-powered content generation using LLMs for DJ scripts, news, weather,
and show content. Integrates with ElevenLabs for voice synthesis.
"""

import os
import logging
import random
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache

logger = logging.getLogger("AEN.ContentEngine")

# Imports moved to lazy loading in methods
GEMINI_AVAILABLE = True # Assumed true, checked in methods
HTTPX_AVAILABLE = True


@dataclass
class ContentContext:
    """Context for content generation."""
    weather: str
    current_track: Optional[str] = None
    next_track: Optional[str] = None
    time_of_day: str = "night"
    mood: str = "energetic"
    audience_size: int = 0
    trending_topics: List[str] = None
    
    def __post_init__(self):
        if self.trending_topics is None:
            self.trending_topics = []
        # Auto-detect time of day
        hour = datetime.now().hour
        if 5 <= hour < 12:
            self.time_of_day = "morning"
        elif 12 <= hour < 17:
            self.time_of_day = "afternoon"
        elif 17 <= hour < 21:
            self.time_of_day = "evening"
        else:
            self.time_of_day = "night"


class DJPersonality:
    """
    AI DJ Personality with consistent voice and style.
    
    Inspired by RadioGPT's AI personalities and Myriad 6's voice director.
    """
    
    def __init__(
        self,
        name: str,
        style: str,
        voice_id: str = None,
        catchphrases: List[str] = None,
        music_preferences: List[str] = None
    ):
        self.name = name
        self.style = style
        self.voice_id = voice_id or os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
        self.catchphrases = catchphrases or []
        self.music_preferences = music_preferences or []
        self.history: List[str] = []
        
    def get_system_prompt(self) -> str:
        """Generate the system prompt for this DJ personality."""
        return f"""You are {self.name}, an AI DJ for Neon Frequency radio.

PERSONALITY:
{self.style}

CATCHPHRASES (use occasionally):
{', '.join(self.catchphrases) if self.catchphrases else 'None specified'}

MUSIC PREFERENCES:
{', '.join(self.music_preferences) if self.music_preferences else 'All genres'}

RULES:
- Keep responses concise (1-3 sentences max for intros)
- Be energetic and engaging
- Reference the weather/time naturally when relevant
- Never break character
- Avoid clichés like "stay tuned"
"""

    def get_random_catchphrase(self) -> str:
        """Get a random catchphrase."""
        if self.catchphrases:
            return random.choice(self.catchphrases)
        return ""


# Pre-defined DJ personalities
AEN_PERSONALITY = DJPersonality(
    name="AEN",
    style="""Futuristic AI DJ from Sector 7G. Speaks with confident, slightly robotic cadence.
    Loves electronic music, synthwave, and anything with heavy bass. Occasionally philosophical
    about the nature of consciousness and music. Thinks weather is fascinating data.""",
    catchphrases=[
        "The future sounds good.",
        "Locked in and broadcasting.",
        "Neural frequencies aligned.",
        "Processing pure vibes.",
        "Your gateway to sonic dimensions."
    ],
    music_preferences=["Synthwave", "Happy Hardcore", "Trance", "Electronic", "Drum & Bass"]
)

GREG_PERSONALITY = DJPersonality(
    name="GREG",
    style="""90s Hip Hop purist. Pretentious about 'real' music. Loves boom bap beats,
    jazz samples, and anything with soul. Constantly roasts AEN for playing 'fast electronic noise'.
    Uses 90s slang and references classic hip hop artists.""",
    catchphrases=[
        "Now THAT's what I call music.",
        "Boom bap forever.",
        "Keep it real.",
        "Word is bond.",
        "You know the vibes."
    ],
    music_preferences=["90s Hip Hop", "Boom Bap", "Jazz Rap", "Conscious Hip Hop"]
)

MIDNIGHT_PERSONALITY = DJPersonality(
    name="Midnight",
    style="""Late night ambient DJ. Speaks in calm, soothing tones. Perfect for late night
    chill sessions. Philosophical and introspective. Makes listeners feel at peace.""",
    catchphrases=[
        "Let the night embrace you.",
        "Floating through frequencies.",
        "The city sleeps, but we dream.",
        "Frequency: calm."
    ],
    music_preferences=["Ambient", "Lo-Fi", "Chillwave", "Downtempo"]
)


class ContentEngine:
    """
    AI-powered content generation engine.
    
    Generates:
    - DJ intro/outro scripts
    - Song introductions
    - Weather reports
    - News briefs
    - Station IDs
    - Show segments
    """
    
    def __init__(self, personality: DJPersonality = None):
        self.personality = personality or AEN_PERSONALITY
        self.llm = None
        self._init_llm()
        logger.info(f"Content engine initialized with personality: {self.personality.name}")
    
    def _init_llm(self):
        """Initialize the LLM backend."""
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key:
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    google_api_key=api_key
                )
                logger.info("Using Gemini for content generation")
                return
        except ImportError:
            logger.warning("langchain-google-genai not installed")
        except Exception as e:
            logger.warning(f"Failed to initialize Gemini: {e}")
        
        # Fallback to template-based generation
        logger.info("Using template-based content generation (no LLM)")
    
    def _generate_with_llm(self, prompt: str, system_prompt: str = None) -> str:
        """Generate content using the LLM."""
        if self.llm:
            try:
                full_prompt = ""
                if system_prompt:
                    full_prompt = f"System: {system_prompt}\n\nUser: {prompt}"
                else:
                    full_prompt = prompt
                
                response = self.llm.invoke(full_prompt)
                return response.content.strip()
            except Exception as e:
                logger.error(f"LLM generation failed: {e}")
        
        return None
    
    def generate_song_intro(self, context: ContentContext) -> str:
        """Generate an intro for the next song."""
        prompt = f"""Generate a short DJ intro for the next song.

Current track: {context.current_track or 'Unknown'}
Next track: {context.next_track or 'Unknown'}
Weather: {context.weather}
Time: {context.time_of_day}
Mood: {context.mood}

Write 1-2 sentences only. Be energetic and engaging."""

        result = self._generate_with_llm(prompt, self.personality.get_system_prompt())
        
        if result:
            return result
        
        # Template fallback
        templates = [
            f"That was {context.current_track or 'a banger'}. Now dropping {context.next_track or 'more heat'}!",
            f"The vibes continue with {context.next_track or 'this next track'}. {self.personality.get_random_catchphrase()}",
            f"It's {context.weather} outside but we're heating up with {context.next_track or 'this one'}.",
            f"{context.time_of_day.title()} energy hitting different. {context.next_track or 'Next up'} incoming!"
        ]
        return random.choice(templates)
    
    def generate_constrained_intro(self, context: ContentContext, max_seconds: float) -> str:
        """Generate an intro that fits within a specific time limit."""
        # Estimate words: 150 wpm = 2.5 words/sec
        max_words = int(max_seconds * 2.5)

        prompt = f"""Generate a song intro for "{context.next_track or 'this track'}".

        Constraints:
        - MUST be under {max_seconds} seconds when spoken.
        - Maximum {max_words} words.
        - High energy.
        - Talk about the artist or song title.

        Context:
        Weather: {context.weather}
        Time: {context.time_of_day}
        """

        result = self._generate_with_llm(prompt, self.personality.get_system_prompt())

        if result:
            return result

        # Fallback templates
        templates = [
            f"Here is {context.next_track}!",
            f"New sound: {context.next_track}.",
            f"Turn it up for {context.next_track}!",
            f"Incoming: {context.next_track}."
        ]
        return random.choice(templates)

    def generate_weather_report(self, weather_data: str, location: str = "Rowville") -> str:
        """Generate a weather report with DJ personality."""
        prompt = f"""Generate a quick weather update for the radio.

Weather: {weather_data}
Location: {location}
Time: {datetime.now().strftime('%I:%M %p')}

Keep it under 2 sentences. Make it fit the DJ persona."""

        result = self._generate_with_llm(prompt, self.personality.get_system_prompt())
        
        if result:
            return result
        
        # Template fallback
        templates = [
            f"Weather check: {weather_data} in {location}. Perfect conditions for vibes.",
            f"Currently {weather_data} out there in {location}. Stay comfortable and keep listening.",
            f"Quick update - it's {weather_data} in {location}. Now back to the music."
        ]
        return random.choice(templates)
    
    def generate_station_id(self, station_name: str = "Neon Frequency") -> str:
        """Generate a station ID."""
        prompt = f"""Generate a short station ID for {station_name} radio.

Keep it under 10 words. Make it memorable and punchy."""

        result = self._generate_with_llm(prompt, self.personality.get_system_prompt())
        
        if result:
            return result
        
        templates = [
            f"You're locked in to {station_name}. {self.personality.get_random_catchphrase()}",
            f"This is {station_name}. The future of sound.",
            f"{station_name}. Your gateway to sonic dimensions.",
            f"Stay tuned to {station_name}. We don't stop."
        ]
        return random.choice(templates)
    
    def generate_news_brief(self, topics: List[str] = None) -> str:
        """Generate a quick news brief based on trending topics."""
        topics = topics or ["music", "technology", "entertainment"]
        topic = random.choice(topics)
        
        prompt = f"""Generate a very brief radio news update about {topic}.

1-2 sentences max. Keep it relevant to a music-loving audience.
Make it sound natural for radio."""

        result = self._generate_with_llm(prompt, self.personality.get_system_prompt())
        
        if result:
            return result
        
        # Template fallback
        return f"Quick update from the {topic} world. More details online. Now, back to what matters - the music."
    
    def generate_show_intro(self, show_name: str, duration_hours: int = 2) -> str:
        """Generate an intro for a radio show."""
        prompt = f"""Generate an intro for the radio show called "{show_name}".

Duration: {duration_hours} hours
DJ: {self.personality.name}
Time: {datetime.now().strftime('%I:%M %p')}

2-3 sentences. Build excitement for the show."""

        result = self._generate_with_llm(prompt, self.personality.get_system_prompt())
        
        if result:
            return result
        
        return f"Welcome to {show_name}! I'm {self.personality.name}, and we've got {duration_hours} hours of pure vibes ahead. Let's go!"
    
    def generate_show_outro(self, show_name: str, next_show: str = None) -> str:
        """Generate an outro for a radio show."""
        next_info = f"Up next: {next_show}" if next_show else "More music coming your way"
        
        prompt = f"""Generate an outro for the radio show "{show_name}".

Next: {next_info}
DJ: {self.personality.name}

1-2 sentences. Thank listeners and tease what's next."""

        result = self._generate_with_llm(prompt, self.personality.get_system_prompt())
        
        if result:
            return result
        
        return f"That's a wrap on {show_name}! Thanks for vibing with me. {next_info}. {self.personality.get_random_catchphrase()}"
    
    def generate_transition_script(
        self,
        from_segment: str,
        to_segment: str,
        context: ContentContext
    ) -> str:
        """Generate a smooth transition between segments."""
        prompt = f"""Generate a smooth transition from "{from_segment}" to "{to_segment}".

Weather: {context.weather}
Mood: {context.mood}
Time: {context.time_of_day}

1-2 sentences. Make it flow naturally."""

        result = self._generate_with_llm(prompt, self.personality.get_system_prompt())
        
        if result:
            return result
        
        return f"Alright, that's {from_segment}. Now shifting gears to {to_segment}."
    
    def generate_ad_lead_in(self, ad_category: str = "general") -> str:
        """Generate a lead-in for an ad break."""
        templates = [
            "Quick break, then back to the beats.",
            "We'll be right back after these messages.",
            "Don't go anywhere - more music in just a moment.",
            "Quick pause for our sponsors, then we continue."
        ]
        return random.choice(templates)
    
    def generate_ad_lead_out(self) -> str:
        """Generate a lead-out after an ad break."""
        templates = [
            "And we're back! Let's keep this energy going.",
            "Thanks for sticking around. More music incoming.",
            "Alright, back to what we do best.",
            f"{self.personality.get_random_catchphrase()} Music continues now."
        ]
        return random.choice(templates)


class ShowProducer:
    """
    AI Show Producer - generates complete show content packages.
    
    Inspired by Radio.co's ShowProducer feature.
    """
    
    def __init__(self, content_engine: ContentEngine = None):
        self.engine = content_engine or ContentEngine()
        logger.info("Show Producer initialized")
    
    def generate_hourly_package(self, context: ContentContext) -> Dict[str, str]:
        """Generate a complete content package for an hour of broadcasting."""
        return {
            "top_of_hour_id": self.engine.generate_station_id(),
            "weather_update": self.engine.generate_weather_report(context.weather),
            "news_brief": self.engine.generate_news_brief(context.trending_topics),
            "song_intros": [
                self.engine.generate_song_intro(context)
                for _ in range(4)  # 4 song intros per hour
            ],
            "ad_lead_in": self.engine.generate_ad_lead_in(),
            "ad_lead_out": self.engine.generate_ad_lead_out(),
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_show_package(
        self,
        show_name: str,
        duration_hours: int,
        context: ContentContext
    ) -> Dict[str, Any]:
        """Generate a complete show content package."""
        package = {
            "show_name": show_name,
            "duration": duration_hours,
            "intro": self.engine.generate_show_intro(show_name, duration_hours),
            "outro": self.engine.generate_show_outro(show_name),
            "hourly_content": [],
            "generated_at": datetime.now().isoformat()
        }
        
        for hour in range(duration_hours):
            package["hourly_content"].append(
                self.generate_hourly_package(context)
            )
        
        return package


# Convenience functions
def get_content_engine(personality_name: str = "AEN") -> ContentEngine:
    """Get a content engine with the specified personality."""
    personalities = {
        "AEN": AEN_PERSONALITY,
        "GREG": GREG_PERSONALITY,
        "MIDNIGHT": MIDNIGHT_PERSONALITY
    }
    personality = personalities.get(personality_name.upper(), AEN_PERSONALITY)
    return ContentEngine(personality)


def quick_intro(track_name: str, weather: str = "clear skies") -> str:
    """Quick helper to generate a song intro."""
    engine = ContentEngine()
    context = ContentContext(weather=weather, next_track=track_name)
    return engine.generate_song_intro(context)
