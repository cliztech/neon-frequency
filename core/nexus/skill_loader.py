"""
The Nexus: Dynamic Skill Loader
===============================
"I know Kung Fu." - Neo (and Ralph)

Fetches capabilities from the Grid (GitHub) and installs them into the Brain.
"""

import os
import logging
import httpx
from typing import List, Optional

logger = logging.getLogger("AEN.Nexus")

class SkillLoader:
    """
    Downloads and installs external skills/agents.
    """
    
    def __init__(self):
        self.skills_dir = os.path.join(os.getcwd(), "skills")
        self.agents_dir = os.path.join(os.getcwd(), "core", "brain", "agents")
        
        # Ensure directories exist
        os.makedirs(self.skills_dir, exist_ok=True)
        os.makedirs(self.agents_dir, exist_ok=True)

    def fetch_skill(self, url: str, name: str, category: str = "skill") -> bool:
        """
        Fetches a file from a URL and saves it to the appropriate directory.
        
        Args:
            url: Raw content URL (e.g. raw.githubusercontent.com...)
            name: Local filename (e.g. 'coding_agent.md')
            category: 'skill', 'agent', or 'command'
        """
        if category == "agent":
            target_dir = self.agents_dir
        else:
            target_dir = self.skills_dir

        target_path = os.path.join(target_dir, name)
        
        logger.info(f"Nexus: Downloading {name} from {url}...")
        
        try:
            response = httpx.get(url, timeout=10.0)
            response.raise_for_status()
            
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(response.text)
                
            logger.info(f"Nexus: Installed {name} to {target_path}")
            return True
            
        except Exception as e:
            logger.error(f"Nexus: Failed to download {name}: {e}")
            return False

    def install_from_repo(self, repo_map: dict):
        """
        Batch install from a dictionary of {name: url}.
        """
        results = {}
        for name, url in repo_map.items():
            success = self.fetch_skill(url, name)
            results[name] = success
        return results
