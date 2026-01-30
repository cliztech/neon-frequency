"""
Nexus Tool: Plugin Manager
==========================
Usage: python tools/plugin_manager.py <plugin_name> [--external]

Installs plugins from anthropics/claude-plugins-official.
"""

import os
import sys
import argparse
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("Nexus.PluginManager")

REPO_BASE = "https://raw.githubusercontent.com/anthropics/claude-plugins-official/main"

# Minimal Registry for 3rd party plugins
REGISTRY = {
    "@EveryInc/every-marketplace/compound-engineering": "https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main",
    "compound-engineering": "https://raw.githubusercontent.com/EveryInc/compound-engineering-plugin/main",
    "@wshobson/claude-code-workflows/backend-development": "https://raw.githubusercontent.com/wshobson/agents/main/plugins/backend-development",
    "backend-development": "https://raw.githubusercontent.com/wshobson/agents/main/plugins/backend-development"
}

def fetch_file(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
    return None

def install_plugin(plugin_name, is_external=False):
    # Check Registry first
    custom_url = REGISTRY.get(plugin_name)
    
    if custom_url:
        logger.info(f"🔌 Nexus: Installing 3rd party plugin '{plugin_name}' from {custom_url}...")
        base_url = custom_url
        # For 3rd party repos, the repo root is often the plugin root
        # We need to check if it has a .claude-plugin dir or if it is the root
        manifest_url = f"{base_url}/.claude-plugin/plugin.json"
        target_name = plugin_name.split("/")[-1] # use last part as folder name
        
    else:
        # Default behavior (Official Repo)
        base_path = "external_plugins" if is_external else "plugins"
        base_url = f"{REPO_BASE}/{base_path}/{plugin_name}"
        manifest_url = f"{base_url}/.claude-plugin/plugin.json"
        target_name = plugin_name
        logger.info(f"🔌 Nexus: Locating plugin '{plugin_name}' in {base_path}...")
    
    # Check for plugin.json to confirm existence
    manifest = fetch_file(manifest_url)
    
    if not manifest:
        # For 3rd party, maybe plugin.json is at root?
        if custom_url:
             manifest_url_root = f"{base_url}/plugin.json"
             manifest = fetch_file(manifest_url_root)
             if manifest:
                 logger.info("   Found manifest at root.")
             else:
                 logger.error(f"❌ Plugin manifest not found at {manifest_url} or {manifest_url_root}")
                 return False
        # If checked internal and failed, try external automatically
        elif not is_external:
             logger.info(f"   Not found in Internal. Checking External...")
             return install_plugin(plugin_name, is_external=True)
        else:
            logger.error(f"❌ Plugin '{plugin_name}' not found.")
            return False

    logger.info(f"✅ Found '{target_name}'. Installing...")
    
    # 1. README
    readme = fetch_file(f"{base_url}/README.md")
    if readme:
        save_file(f"skills/docs/{target_name}_README.md", readme)

    # 2. Manifest
    save_file(f"skills/plugins/{target_name}/plugin.json", manifest)
    logger.info(f"   Installed manifest for {target_name}.")

    return True

def save_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/plugin_manager.py <plugin_name>")
        sys.exit(1)
        
    plugin_name = sys.argv[1]
    install_plugin(plugin_name)

if __name__ == "__main__":
    main()
