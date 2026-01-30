import sys
import os

# Add root to path
sys.path.append(os.getcwd())

try:
    from core.brain.voice_generator import ElevenLabsClient
    print("✅ Import successful")
except ImportError:
    print("❌ Import failed: ElevenLabsClient not found")
    sys.exit(1)

client = ElevenLabsClient()
output = client.generate("Ralph says hi", "mock_output.mp3")

if output and os.path.exists("mock_output.mp3"):
    print("✅ Generation successful")
    os.remove("mock_output.mp3")
    sys.exit(0)
else:
    print("❌ Generation failed")
    sys.exit(1)
