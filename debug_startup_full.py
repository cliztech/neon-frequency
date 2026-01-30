import sys
import time

def log(msg):
    print(msg)
    sys.stdout.flush()

log("Starting debug trace...")
try:
    log("Importing logging...")
    import logging
    
    log("Importing telnetlib3...")
    import telnetlib3
    log("Telnetlib3 imported.")
    
    log("Importing os...")
    import os
    
    log("Importing content_engine...")
    from core.brain.content_engine import ContentEngine
    log("ContentEngine imported.")
    
    log("Importing radio_automation...")
    from core.brain.radio_automation import AzuraCastClient
    log("RadioAutomation imported.")

    log("Importing skills...")
    from core.brain.skills import TrendWatcher
    log("Skills imported.")
    
    log("Importing greg...")
    from core.brain.greg import GregPersona
    log("Greg imported.")

    log("Importing agents/music...")
    from core.brain.agents.music import CrateDigger
    log("Agents/Music imported.")

    log("Importing agents/operations...")
    from core.brain.agents.operations import SRE_Sentinel
    log("Agents/Operations imported.")

    log("Importing agents/development...")
    from core.brain.agents.development import CodeChemist
    log("Agents/Dev imported.")

    log("Importing agents/content...")
    from core.brain.agents.content import ShowRunner
    log("Agents/Content imported.")
    
    log("Importing langgraph...")
    from langgraph.graph import StateGraph
    log("LangGraph imported.")
    
    log("Importing agents/engineering...")
    from core.brain.agents.engineering import DeckMaster
    log("Agents/Engineering imported.")
    
    log("ALL IMPORTS SUCCESSFUL.")
    
except ImportError as e:
    log(f"IMPORT ERROR: {e}")
except Exception as e:
    log(f"GENERAL ERROR: {e}")
