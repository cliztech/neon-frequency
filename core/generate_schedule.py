#!/usr/bin/env python3
"""
Generate Daily AI Schedule
==========================
Run this script to generate a 24-hour radio schedule with AI voice tracks,
weather, news, and music.

Output:
    ./daily_schedule/hour_00.m3u
    ...
    ./daily_schedule/hour_23.m3u
    ./daily_schedule/generated_audio/
"""

import os
import sys
import logging
import argparse
from dotenv import load_dotenv

# Ensure we can import core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.brain.scheduler import RadioScheduler

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AEN.Generator")

def main():
    parser = argparse.ArgumentParser(description="Generate AI Radio Schedule")
    parser.add_argument("--output", type=str, default="./daily_schedule", help="Output directory for playlists")
    parser.add_argument("--library", type=str, default="/music", help="Path to music library")
    parser.add_argument("--mock-voice", action="store_true", help="Force mock voice generation (saves credits)")
    parser.add_argument("--hours", type=int, default=24, help="Number of hours to generate")

    args = parser.parse_args()

    load_dotenv()

    logger.info(f"Initializing Scheduler (Library: {args.library})...")

    # Optional: Force mock mode if requested
    if args.mock_voice:
        # We can hack the env var if the client checks it, or just rely on the client's internal fallback
        # The ElevenLabsClient checks ELEVENLABS_API_KEY. If missing, it mocks.
        if "ELEVENLABS_API_KEY" in os.environ:
            logger.info("Mock mode requested: Temporarily unsetting ELEVENLABS_API_KEY")
            del os.environ["ELEVENLABS_API_KEY"]

    scheduler = RadioScheduler(
        library_path=args.library,
        audio_output_dir=os.path.join(args.output, "generated_audio")
    )

    logger.info(f"Generating schedule for {args.hours} hours...")

    try:
        # We'll just loop here instead of calling generate_daily_schedule to respect args.hours
        os.makedirs(args.output, exist_ok=True)

        generated = []
        for h in range(args.hours):
            path = scheduler.generate_hour_block(h, args.output)
            generated.append(path)

        logger.info("Generation Complete!")
        logger.info(f"Generated {len(generated)} playlists in {args.output}")

    except Exception as e:
        logger.error(f"Failed to generate schedule: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
