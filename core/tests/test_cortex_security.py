
import asyncio
import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import sys
import os

# MOCK BROKEN IMPORTS to allow importing cortex without dependencies that might be missing or broken
sys.modules['core.brain.agents.content'] = MagicMock()
sys.modules['core.brain.agents.content'].ShowRunner = MagicMock()
sys.modules['core.brain.agents.content'].TalentParams = MagicMock()

# Import the function under test
from core.brain.cortex import push_to_deck

class TestCortexSecurity(unittest.TestCase):
    def test_command_injection_prevented(self):
        # Setup mock for telnetlib3
        mock_reader = AsyncMock()
        mock_writer = MagicMock()
        mock_writer.drain = AsyncMock()

        async def mock_open_connection(host, port):
            return mock_reader, mock_writer

        with patch('telnetlib3.open_connection', side_effect=mock_open_connection):
            # malicious payload
            malicious_track = "song.mp3\nadmin.hack_system"
            state = {
                "next_track": malicious_track,
                "history": [],
                "greg_interruption": ""
            }

            # Run the function
            asyncio.run(push_to_deck(state))

            # Check what was written
            calls = mock_writer.write.call_args_list
            self.assertTrue(len(calls) > 0)

            sent_cmd = calls[0][0][0]

            # Verify that the newline injection is GONE
            self.assertNotIn("\nadmin.hack_system", sent_cmd)

            # Verify that the payload was sanitized (newlines removed)
            self.assertIn("/music/song.mp3admin.hack_system", sent_cmd)

if __name__ == '__main__':
    unittest.main()
