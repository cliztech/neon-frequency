import logging
import random
import os
# import requests  <-- Moved to lazy import
from functools import lru_cache
from typing import List, Dict
import datetime

# Google Workspace Imports
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    GOOGLE_LIBS_AVAILABLE = True
except ImportError:
    GOOGLE_LIBS_AVAILABLE = False

# In a real scenario, we would use:
# from langchain_community.tools import GoogleSearchRun

logger = logging.getLogger("AEN.Skills")

class TrendWatcher:
    """The eyes and ears of the station."""
    
    def __init__(self):
        self.trends = [
            "Hyper-Pop revival",
            "AI-generated Jazz",
            "Cyberpunk aesthetics in UI design",
            "The weather in Sector 7G",
            "Retro-gaming soundtracks"
        ]

    @lru_cache(maxsize=128)
    def get_current_trends(self) -> str:
        """Simulates fetching real-time trends."""
        # TODO: Implement real Perplexity/Google Search here
        trend = random.choice(self.trends)
        logger.info(f"Trend detected: {trend}")
        return trend

    def search_music(self, query: str) -> List[str]:
        """Simulates finding music based on a query."""
        logger.info(f"Searching for: {query}")
        return [f"{query}_remix.mp3", f"{query}_speed_up.mp3"]

class WeatherStation:
    """Real-time weather data."""
    
    @staticmethod
    def get_weather(location: str = "Rowville") -> str:
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")

        if api_key:
            try:
                import requests
                # 5 second timeout to prevent hanging
                response = requests.get(
                    f"https://api.openweathermap.org/data/2.5/weather",
                    params={"q": location, "appid": api_key, "units": "metric"},
                    timeout=5
                )
                response.raise_for_status()
                data = response.json()

                temp = data["main"]["temp"]
                # Capitalize first letter of description for better readability
                description = data["weather"][0]["description"].capitalize()

                return f"{temp}°C, {description}"

            except Exception as e:
                logger.error(f"Failed to fetch weather data: {e}")
        else:
            logger.warning("OPENWEATHERMAP_API_KEY not found. Using random fallback data.")

        # Fallback to random data
        temp = random.randint(30, 42)
        conditions = ["Sunny", "Heatwave", "Stormy", "Neon Rain"]
        return f"{temp}°C, {random.choice(conditions)}"

class GoogleWorkspace:
    """Interface for Google Workspace (Calendar, Drive, Docs)."""

    def __init__(self):
        self.creds = None
        self.service_drive = None
        self.service_calendar = None
        self.service_docs = None

        self.creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

        if GOOGLE_LIBS_AVAILABLE and self.creds_path and os.path.exists(self.creds_path):
            try:
                self.creds = service_account.Credentials.from_service_account_file(
                    self.creds_path,
                    scopes=[
                        'https://www.googleapis.com/auth/calendar.readonly',
                        'https://www.googleapis.com/auth/drive',
                        'https://www.googleapis.com/auth/documents'
                    ]
                )
                self.service_drive = build('drive', 'v3', credentials=self.creds)
                self.service_calendar = build('calendar', 'v3', credentials=self.creds)
                self.service_docs = build('docs', 'v1', credentials=self.creds)
                logger.info("Google Workspace services initialized.")
            except Exception as e:
                logger.error(f"Failed to initialize Google Workspace services: {e}")
        else:
            logger.warning("Google Workspace credentials not found or libs missing. Using simulation mode.")

    def get_schedule(self, date: str = None) -> str:
        """Fetches calendar events or simulates them."""
        if self.service_calendar:
            try:
                # Basic implementation: Fetch upcoming 10 events
                events_result = self.service_calendar.events().list(
                    calendarId='primary', maxResults=10, singleEvents=True,
                    orderBy='startTime'
                ).execute()
                events = events_result.get('items', [])
                if not events:
                    return "No upcoming events found."

                event_strings = []
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    summary = event['summary']
                    event_strings.append(f"{start} - {summary}")
                return "\n".join(event_strings)
            except Exception as e:
                logger.error(f"Failed to fetch calendar: {e}")
                return f"Error fetching schedule: {e}"
        else:
            # Simulation
            logger.info(f"Simulating schedule for {date or 'today'}")
            events = [
                "10:00 AM - Interview with DJ Sombra",
                "02:00 PM - Station Maintenance",
                "08:00 PM - Live Broadcast 'Neon Nights'"
            ]
            return "\n".join(events)

    def search_drive(self, query: str) -> List[str]:
        """Searches Drive or returns simulated files."""
        if self.service_drive:
            try:
                # Sanitize query to prevent injection
                sanitized_query = query.replace("'", "\\'")
                results = self.service_drive.files().list(
                    q=f"name contains '{sanitized_query}'", pageSize=10, fields="nextPageToken, files(id, name)"
                ).execute()
                items = results.get('files', [])
                return [f"{item['name']} ({item['id']})" for item in items]
            except Exception as e:
                logger.error(f"Drive search failed: {e}")
                return []
        else:
            # Simulation
            logger.info(f"Simulating Drive search for '{query}'")
            return [
                f"{query}_brief.docx",
                f"{query}_contract.pdf",
                f"guest_list_{query}.xlsx"
            ]

    def create_doc(self, title: str, content: str) -> str:
        """Creates a Google Doc or simulates it."""
        if self.service_docs and self.service_drive:
            try:
                # Create empty doc
                doc_metadata = {'name': title, 'mimeType': 'application/vnd.google-apps.document'}
                doc = self.service_drive.files().create(body=doc_metadata, fields='documentId').execute()
                doc_id = doc.get('documentId')

                # Write content
                requests = [
                    {
                        'insertText': {
                            'location': {'index': 1},
                            'text': content
                        }
                    }
                ]
                self.service_docs.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
                logger.info(f"Created doc: {title} ({doc_id})")
                return f"Created document: {title} (ID: {doc_id})"
            except Exception as e:
                logger.error(f"Failed to create doc: {e}")
                return f"Error creating document: {e}"
        else:
            # Simulation
            logger.info(f"Simulating Doc creation: {title}")
            return f"Created (Simulated) Document: {title}"
