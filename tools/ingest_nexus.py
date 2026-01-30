import sys
import os

sys.path.append(os.getcwd())
from core.nexus.skill_loader import SkillLoader

loader = SkillLoader()

# Map of High-Value Skills from affaan-m/everything-claude-code
# Note: Using raw.githubusercontent.com URLs
# Map of High-Value Assets from affaan-m/everything-claude-code
# Based on repository README file tree
REPO_BASE = "https://raw.githubusercontent.com/affaan-m/everything-claude-code/main"

ASSETS_TO_INGEST = {
    # Agents
    "agents/planner.md": f"{REPO_BASE}/agents/planner.md",
    "agents/architect.md": f"{REPO_BASE}/agents/architect.md",
    "agents/code-reviewer.md": f"{REPO_BASE}/agents/code-reviewer.md",
    "agents/tdd-guide.md": f"{REPO_BASE}/agents/tdd-guide.md",
    
    # Instinct / Skill Creator Commands
    "commands/skill-create.md": f"{REPO_BASE}/commands/skill-create.md",
    "commands/instinct-status.md": f"{REPO_BASE}/commands/instinct-status.md",
    "commands/instinct-import.md": f"{REPO_BASE}/commands/instinct-import.md",
    "commands/instinct-export.md": f"{REPO_BASE}/commands/instinct-export.md",
    "commands/evolve.md": f"{REPO_BASE}/commands/evolve.md",

    # Rules
    "rules/security.md": f"{REPO_BASE}/rules/security.md",
    "rules/coding-style.md": f"{REPO_BASE}/rules/coding-style.md",
    
    # MCP
    "mcp/mcp-servers.json": f"{REPO_BASE}/mcp-configs/mcp-servers.json"
}

print("Nexus: Initiating Ingestion Sequence...")
print("Nexus: Initiating Expanded Ingestion Sequence...")

# We need to be smart about categories for the loader
for local_path, url in ASSETS_TO_INGEST.items():
    filename = os.path.basename(local_path)
    category = "skill"
    
    if local_path.startswith("agents/"):
        category = "agent"
    elif local_path.startswith("commands/"):
        # Commands are just instructions, save as skill for now or dedicated dir
        category = "command" 
        # Loader needs to handle 'command', or we map to skill
    
    # Fetch
    success = loader.fetch_skill(url, filename, category=category)
    status = "[OK]" if success else "[FAIL]"
    print(f"{status} {local_path}")
