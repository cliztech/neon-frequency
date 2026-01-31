import plugin_manager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("Nexus.Installer")

PLUGINS = [
    # Internal Workflow Plugins
    "agent-sdk-dev",
    "code-review",
    "commit-commands",
    "feature-dev",
    "frontend-design",
    "plugin-dev",
    "pr-review-toolkit",
    "security-guidance",
    
    # External Service Plugins
    "github",
    "supabase",
    "playwright",
    "firebase",
    "stripe",
    "linear",
    "slack",
    "gitlab"
]

def install_all():
    print(f"Starting batch installation of {len(PLUGINS)} plugins...")
    success_count = 0
    failed = []

    for plugin in PLUGINS:
        print(f"\nProcessing '{plugin}'...")
        try:
            # install_plugin returns True/False
            if plugin_manager.install_plugin(plugin):
                success_count += 1
            else:
                failed.append(plugin)
        except Exception as e:
            print(f"Error installing {plugin}: {e}")
            failed.append(plugin)
            
    print("\n========================================")
    print(f"Installation Complete. Success: {success_count}/{len(PLUGINS)}")
    if failed:
        print(f"Failed plugins: {', '.join(failed)}")
    print("========================================")

if __name__ == "__main__":
    install_all()
