"""
The Nexus: Instinct Engine
==========================
"I know Kung Fu." -> "Show me."

Manages 'Instincts': granular learned behaviors and patterns.
"""

import os
import json
import yaml
import logging
from typing import List, Dict, Optional

logger = logging.getLogger("AEN.Nexus.Instincts")

class InstinctEngine:
    def __init__(self):
        self.instincts_dir = os.path.join(os.getcwd(), "skills", "instincts")
        os.makedirs(self.instincts_dir, exist_ok=True)
        self.instincts = self._load_instincts()

    def _load_instincts(self) -> List[Dict]:
        """Load all YAML instincts from storage."""
        loaded = []
        for filename in os.listdir(self.instincts_dir):
            if filename.endswith((".yaml", ".yml")):
                try:
                    with open(os.path.join(self.instincts_dir, filename), "r") as f:
                        data = yaml.safe_load(f)
                        if data:
                            loaded.append(data)
                except Exception as e:
                    logger.error(f"Failed to load instinct {filename}: {e}")
        return loaded

    def status(self) -> str:
        """
        /instinct-status
        Returns a summary of learned instincts with confidence.
        """
        if not self.instincts:
            return "🧠 Nexus: No instincts learned yet."
        
        report = ["🧠 Nexus: Active Instincts"]
        for i in self.instincts:
            name = i.get('id', 'unknown')
            conf = i.get('confidence', 0.0)
            trigger = i.get('trigger', 'unknown')
            report.append(f"- {name} (Conf: {conf}) -> Triggers on: '{trigger}'")
        
        return "\n".join(report)

    def import_instinct(self, filepath: str) -> bool:
        """
        /instinct-import <file>
        """
        try:
            with open(filepath, "r") as f:
                data = yaml.safe_load(f)
            
            # Basic Validation
            if not data.get('id'):
                raise ValueError("Instinct missing ID")
            
            target = os.path.join(self.instincts_dir, f"{data['id']}.yaml")
            with open(target, "w") as f:
                yaml.dump(data, f)
            
            self.instincts = self._load_instincts() # Reload
            return True
        except Exception as e:
            logger.error(f"Import failed: {e}")
            return False

    def export_instincts(self, output_dir: str = "exported_instincts") -> str:
        """
        /instinct-export
        """
        os.makedirs(output_dir, exist_ok=True)
        count = 0
        for i in self.instincts:
            filename = f"{i.get('id', 'instinct')}.yaml"
            with open(os.path.join(output_dir, filename), "w") as f:
                yaml.dump(i, f)
            count += 1
        return f"Exported {count} instincts to {output_dir}/"

    def evolve(self) -> str:
        """
        /evolve
        Clusters instincts into a SKILL.md file.
        (Simplified implementation: Groups by domain)
        """
        domains = {}
        for i in self.instincts:
            domain = i.get('domain', 'general')
            if domain not in domains:
                domains[domain] = []
            domains[domain].append(i)
        
        generated = []
        for domain, items in domains.items():
            content = f"# Generated Skill: {domain}\n\n"
            for item in items:
                content += f"## {item.get('id')}\n"
                content += f"Trigger: {item.get('trigger')}\n"
                content += f"Action: {item.get('response') or 'See detailed instinct'}\n\n"
            
            filename = f"generated_skill_{domain}.md"
            with open(os.path.join(os.getcwd(), "skills", filename), "w") as f:
                f.write(content)
            generated.append(filename)
            
        return f"Evolved {len(generated)} skills: {', '.join(generated)}"
