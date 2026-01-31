import sys
import os

# Ensure root is in path
sys.path.append(os.getcwd())

try:
    from core.brain.agents.news_agent import NewsAgent
    print("✅ Import successful")
except ImportError:
    print("❌ Import failed: NewsAgent not found")
    sys.exit(1)

agent = NewsAgent()
headlines = agent.get_top_stories(limit=3)

print(f"Headlines: {headlines}")

if isinstance(headlines, list) and len(headlines) > 0:
    print("✅ Headlines fetched")
    sys.exit(0)
else:
    print("❌ No headlines returned")
    sys.exit(1)
