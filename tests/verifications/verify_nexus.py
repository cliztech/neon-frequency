import sys
import os

sys.path.append(os.getcwd())

try:
    from core.nexus.skill_loader import SkillLoader
    print("✅ Import successful")
except ImportError:
    print("❌ Import failed: SkillLoader not found")
    sys.exit(1)

loader = SkillLoader()
# specific test URL (a small markdown file from the target repo if possible, or a generic known raw file)
# Using a generic raw file for safety verification
test_url = "https://raw.githubusercontent.com/affaan-m/everything-claude-code/main/README.md"
success = loader.fetch_skill(test_url, "nexus_test_readme.md", category="skill")

if success and os.path.exists(os.path.join("skills", "nexus_test_readme.md")):
    print("✅ Skill fetch successful")
    # Clean up
    os.remove(os.path.join("skills", "nexus_test_readme.md"))
    sys.exit(0)
else:
    print("❌ Skill fetch failed")
    sys.exit(1)
