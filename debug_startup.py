import sys
print("Starting debug...")
try:
    print("Importing logging...")
    import logging
    print("Importing os...")
    import os
    print("Importing content_engine...")
    from core.brain.content_engine import ContentEngine
    print("Importing radio_automation...")
    from core.brain.radio_automation import AzuraCastClient
    print("Importing agents...")
    from core.brain.agents.music import CrateDigger
    from core.brain.agents.operations import SRE_Sentinel
    print("All imports successful.")
except Exception as e:
    print(f"Import failed: {e}")
except KeyboardInterrupt:
    print("Interrupted")
