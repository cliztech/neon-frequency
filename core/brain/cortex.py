print("DEBUG: STARTING CORTEX...")
import asyncio
import hashlib
import telnetlib3
import logging
import os
import sys
import random
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END

# --- PATH SETUP ---
# Allow importing from the same directory when run from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- IMPORTS ---
from skills import TrendWatcher, GoogleWorkspace
from greg import GregPersona
from content_engine import ContentEngine, ContentContext, ShowProducer
from radio_automation import AzuraCastClient, PlaylistOptimizer, Track

# New Ralph Loop Clients
from core.brain.weather_client import WeatherClient
from core.brain.agents.news_agent import NewsAgent
from core.brain.voice_generator import ElevenLabsClient

# Agent Imports
print("DEBUG: Importing Agents...")
from core.brain.agents.music import CrateDigger, FlowMaster
from core.brain.agents.operations import SRE_Sentinel
from core.brain.agents.development import CodeChemist
from core.brain.agents.content import ShowRunner, TalentParams
from core.brain.agents.engineering import DeckMaster
print("DEBUG: Agents Imported.")

# --- SETUP ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - AEN - %(message)s')
logger = logging.getLogger("AEN.Cortex")

trend_watcher = TrendWatcher()
content_engine = ContentEngine()
show_producer = ShowProducer(content_engine)
workspace_skill = GoogleWorkspace()

# Initialize Real Clients
weather_client = WeatherClient()
news_agent = NewsAgent()
voice_client = ElevenLabsClient()

# Initialize Persona with tools
greg_agent = GregPersona(weather_client=weather_client, news_agent=news_agent)

# Initialize Specialized Agents
crate_digger = CrateDigger()
flow_master = FlowMaster()
sre_sentinel = SRE_Sentinel()
code_chemist = CodeChemist()
talent_params = TalentParams()
deck_master = DeckMaster()

# Global clients (lazy loaded)
azuracast = None
def get_azuracast():
    global azuracast
    if azuracast is None:
        try:
            azuracast = AzuraCastClient()
        except Exception as e:
            logger.warning(f"AzuraCast init failed: {e}")
    return azuracast

class RadioState(TypedDict):
    current_track: str
    next_track: str
    weather: str
    mood: str
    news_headline: str  # Added news
    history: List[str]
    greg_interruption: str
    voice_script: str  # Generated DJ script
    voice_audio_path: Optional[str]  # Path to generated audio
    schedule: str

# --- NODES ---

async def monitor_deck(state: RadioState):
    """Checks station heartbeat and gathers context."""
    logging.info("Scanning frequencies... Deck is active.")
    
    # Try to get real now playing from AzuraCast
    ac = get_azuracast()
    if ac:
        now_playing = await asyncio.to_thread(ac.get_now_playing)
        if now_playing:
            state["current_track"] = f"{now_playing.track.artist} - {now_playing.track.title}"
            logging.info(f"Now Playing (AzuraCast): {state['current_track']}")
    
    # Update Context in Parallel
    # weather_client.get_weather and workspace_skill.get_schedule are blocking IO calls
    # trend_watcher and news_agent are currently fast/mocked but we run them in parallel for consistency
    results = await asyncio.gather(
        asyncio.to_thread(weather_client.get_weather),
        asyncio.to_thread(workspace_skill.get_schedule),
        asyncio.to_thread(trend_watcher.get_current_trends),
        asyncio.to_thread(news_agent.get_top_stories, 1)
    )
    
    state["weather"] = results[0]
    state["schedule"] = results[1]
    trend = results[2]
    headlines = results[3]

    state["mood"] = f"Hype ({trend})"
    state["news_headline"] = headlines[0] if headlines else "No news is good news."
    
    return state


async def select_track(state: RadioState):
    """The Crate Digger."""
    # Logic: Prefer Happy Hardcore, avoid repeats
    candidates = ["happy_hardcore_anthem.mp3", "trance_uplift.mp3", "cheeky_prints_jingle.mp3"]
    recent = set(state.get("history", []))
    available = [track for track in candidates if track not in recent]
    selection = random.choice(available or candidates)
    
    state["next_track"] = selection
    logging.info(f"Selected Track: {selection}")
    return state

async def generate_host_script(state: RadioState):
    """The Persona Engine - now powered by Content Engine."""
    # Check if Greg wants to interrupt (30% chance)
    if random.random() < 0.3:
        roast = greg_agent.generate_interruption(state["next_track"], "It's gonna be huge!")
        state["greg_interruption"] = roast
        logging.info(f"🚨 GREG INTERRUPTION: {roast}")
    else:
        state["greg_interruption"] = ""

    # Use Content Engine for AI-powered script generation
    # We pass the news headline into the mood or context
    context = ContentContext(
        weather=state["weather"],
        current_track=state.get("current_track"),
        next_track=state["next_track"],
        mood=f"{state['mood']} | News: {state['news_headline']} | Schedule: {state['schedule']}"
    )
    
    script = await asyncio.to_thread(content_engine.generate_song_intro, context)
    state["voice_script"] = script
    logging.info(f"Generated Script: {script}")
    
    # Generate voice audio using ElevenLabs
    try:
        cache_dir = os.getenv("AUDIO_CACHE_DIR", "/tmp")
        script_hash = hashlib.sha256(script.encode("utf-8")).hexdigest()
        audio_path = os.path.join(cache_dir, f"voice_{script_hash}.mp3")
        audio = await asyncio.to_thread(voice_client.generate, script, output_path=audio_path)
        if audio:
            state["voice_audio_path"] = audio_path
            logging.info(f"Voice audio generated: {audio_path}")
        else:
            state["voice_audio_path"] = None
    except Exception as e:
        logging.warning(f"Voice generation failed: {e}")
        state["voice_audio_path"] = None
    
    return state


async def push_to_deck(state: RadioState):
    """Telnet Interface to Liquidsoap."""
    try:
        # Connect to Liquidsoap container
        # Note: In a real docker network, hostname might be 'liquidsoap' not localhost
        host = os.getenv("LIQUIDSOAP_HOST", "localhost")
        reader, writer = await asyncio.wait_for(
            telnetlib3.open_connection(host, 1234),
            timeout=5,
        )
        
        # 1. Push Song
        # Sanitize track name to prevent command injection
        clean_track = state['next_track'].replace('\n', '').replace('\r', '')
        if clean_track != state['next_track']:
            logging.warning(f"Sanitized track name containing newlines: {state['next_track']!r} -> {clean_track!r}")

        cmd = f"brain_queue.push /music/{clean_track}\n"
        writer.write(cmd)
        
        # 2. Push Greg (if active) - This requires a text-to-speech engine to generate the audio file first
        if state["greg_interruption"]:
            # For now, we simulate Greg by logging. 
            pass 

        await writer.drain()
        logging.info(f"Queue Command Sent: {cmd.strip()}")
        writer.close()
        await writer.wait_closed()
    except Exception as e:
        logging.warning(f"Deck connection failed (is Docker running?): {e}")
        
    state["history"].append(state["next_track"])
    return state

# --- GRAPH ---
workflow = StateGraph(RadioState)
workflow.add_node("monitor", monitor_deck)
workflow.add_node("selector", select_track)
workflow.add_node("host", generate_host_script)
workflow.add_node("pusher", push_to_deck)

workflow.set_entry_point("monitor")
workflow.add_edge("monitor", "selector")
workflow.add_edge("selector", "host")
workflow.add_edge("host", "pusher")
workflow.add_edge("pusher", END)

print("DEBUG: Compiling Graph...")
app = workflow.compile()
print("DEBUG: Graph Compiled.")

async def main():
    print("--- AEN CORTEX ONLINE ---")
    logger.info("Google Workspace Extension: ACTIVE")
    await app.ainvoke({
        "current_track": "", 
        "next_track": "", 
        "weather": "", 
        "mood": "", 
        "news_headline": "",
        "history": [],
        "greg_interruption": "",
        "voice_script": "",
        "voice_audio_path": None,
        "schedule": ""
    })


if __name__ == "__main__":
    asyncio.run(main())
