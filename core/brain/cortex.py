import asyncio
import telnetlib3
import logging
import os
import sys
import random
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

# --- PATH SETUP ---
# Allow importing from the same directory when run from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- IMPORTS ---
from skills import TrendWatcher, WeatherStation
from greg import GregPersona

# --- SETUP ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - AEN - %(message)s')
logger = logging.getLogger("AEN.Cortex")

trend_watcher = TrendWatcher()
greg_agent = GregPersona()

class RadioState(TypedDict):
    current_track: str
    next_track: str
    weather: str
    mood: str
    history: List[str]
    greg_interruption: str  # New field for Greg's roast

# --- NODES ---

async def monitor_deck(state: RadioState):
    """Checks station heartbeat and gathers context."""
    logging.info("Scanning frequencies... Deck is active.")
    
    # Update Context
    state["weather"] = WeatherStation.get_weather()
    trend = trend_watcher.get_current_trends()
    state["mood"] = f"Hype ({trend})"
    
    return state

async def select_track(state: RadioState):
    """The Crate Digger."""
    # Logic: Prefer Happy Hardcore, avoid repeats
    candidates = ["happy_hardcore_anthem.mp3", "trance_uplift.mp3", "cheeky_prints_jingle.mp3"]
    selection = random.choice(candidates)
    
    state["next_track"] = selection
    logging.info(f"Selected Track: {selection}")
    return state

async def generate_host_script(state: RadioState):
    """The Persona Engine."""
    # Check if Greg wants to interrupt (30% chance)
    if random.random() < 0.3:
        roast = greg_agent.generate_interruption(state["next_track"], "It's gonna be huge!")
        state["greg_interruption"] = roast
        logging.info(f"🚨 GREG INTERRUPTION: {roast}")
    else:
        state["greg_interruption"] = ""

    prompt = f"""
    SYSTEM: You are AEN, host of Neon Frequency.
    CONTEXT: {state['weather']}. Mood: {state['mood']}.
    NEXT SONG: {state['next_track']}
    TASK: Write a 1-sentence intro.
    """
    logging.info("Generating voice script...")
    script = f"It's {state['weather']} and we are riding the {state['mood']} wave! Coming up: {state['next_track']}."
    logging.info(f"Script: {script}")
    return state

async def push_to_deck(state: RadioState):
    """Telnet Interface to Liquidsoap."""
    try:
        # Connect to Liquidsoap container
        # Note: In a real docker network, hostname might be 'liquidsoap' not localhost
        reader, writer = await telnetlib3.open_connection('localhost', 1234)
        
        # 1. Push Song
        cmd = f"brain_queue.push /music/{state['next_track']}\n"
        writer.write(cmd)
        
        # 2. Push Greg (if active) - This requires a text-to-speech engine to generate the audio file first
        if state["greg_interruption"]:
            # For now, we simulate Greg by logging. 
            pass 

        await writer.drain()
        logging.info(f"Queue Command Sent: {cmd.strip()}")
        writer.close()
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

app = workflow.compile()

async def main():
    print("--- AEN CORTEX ONLINE ---")
    await app.ainvoke({
        "current_track": "", 
        "next_track": "", 
        "weather": "", 
        "mood": "", 
        "history": [],
        "greg_interruption": ""
    })

if __name__ == "__main__":
    asyncio.run(main())
