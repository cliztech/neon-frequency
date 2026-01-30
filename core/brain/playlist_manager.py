"""
Playlist Manager
================
Handles import and export of standard playlist formats (.m3u, .pls).
Compatible with RadioDJ, StationPlaylist, and other automation software.
"""

import os
import logging
from typing import List, Optional
from pathlib import Path
import configparser

# Import TrackMetadata to map data
from core.brain.music_library import TrackMetadata, Genre

logger = logging.getLogger("AEN.PlaylistManager")

class PlaylistManager:
    """
    Manager for reading and writing playlist files.
    """

    @staticmethod
    def export_m3u(tracks: List[TrackMetadata], output_path: str, relative_paths: bool = False):
        """
        Export tracks to an Extended M3U (.m3u8) file.

        Args:
            tracks: List of TrackMetadata objects.
            output_path: Path to write the file.
            relative_paths: If True, uses paths relative to the playlist file.
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("#EXTM3U\n")

                for track in tracks:
                    # Duration should be in seconds. Default to -1 if unknown (stream) or 0
                    duration = track.duration_seconds if track.duration_seconds else -1

                    # EXTINF:duration,Artist - Title
                    # Or just Title if Artist is missing
                    if track.artist and track.title:
                        info = f"{track.artist} - {track.title}"
                    else:
                        info = track.title or "Unknown Track"

                    f.write(f"#EXTINF:{duration},{info}\n")

                    # Resolve path
                    file_path = track.file_path
                    if relative_paths:
                        try:
                            playlist_dir = os.path.dirname(os.path.abspath(output_path))
                            file_path = os.path.relpath(file_path, playlist_dir)
                        except ValueError:
                            # Path is on different drive or invalid relative calculation
                            pass

                    f.write(f"{file_path}\n")

            logger.info(f"Exported M3U playlist to {output_path} ({len(tracks)} tracks)")
            return True
        except Exception as e:
            logger.error(f"Failed to export M3U: {e}")
            return False

    @staticmethod
    def parse_m3u(file_path: str) -> List[TrackMetadata]:
        """
        Parse an M3U file into TrackMetadata objects.
        """
        tracks = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            current_info = None
            current_duration = 0

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                if line.startswith("#EXTINF:"):
                    # Parse metadata: #EXTINF:123,Artist - Title
                    try:
                        meta_part = line[8:]
                        if "," in meta_part:
                            dur_str, title_str = meta_part.split(",", 1)
                            current_duration = int(float(dur_str))
                            current_info = title_str
                        else:
                            current_info = meta_part
                    except Exception:
                        current_info = "Unknown"

                elif not line.startswith("#"):
                    # It's a file path
                    path = line
                    # Attempt to parse Artist - Title from info string
                    artist = "Unknown"
                    title = "Unknown"

                    if current_info:
                        if " - " in current_info:
                            parts = current_info.split(" - ", 1)
                            artist = parts[0].strip()
                            title = parts[1].strip()
                        else:
                            title = current_info.strip()
                    else:
                        # Fallback to filename
                        p = Path(path)
                        title = p.stem

                    tracks.append(TrackMetadata(
                        file_path=path,
                        title=title,
                        artist=artist,
                        duration_seconds=current_duration
                    ))

                    # Reset for next entry
                    current_info = None
                    current_duration = 0

            logger.info(f"Parsed M3U playlist from {file_path} ({len(tracks)} tracks)")
            return tracks

        except Exception as e:
            logger.error(f"Failed to parse M3U: {e}")
            return []

    @staticmethod
    def export_pls(tracks: List[TrackMetadata], output_path: str):
        """
        Export tracks to a PLS file.
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("[playlist]\n")
                f.write(f"NumberOfEntries={len(tracks)}\n")

                for i, track in enumerate(tracks, 1):
                    f.write(f"File{i}={track.file_path}\n")

                    title_str = track.title
                    if track.artist:
                        title_str = f"{track.artist} - {track.title}"

                    f.write(f"Title{i}={title_str}\n")
                    f.write(f"Length{i}={track.duration_seconds or -1}\n")

                f.write("Version=2\n")

            logger.info(f"Exported PLS playlist to {output_path} ({len(tracks)} tracks)")
            return True
        except Exception as e:
            logger.error(f"Failed to export PLS: {e}")
            return False

    @staticmethod
    def parse_pls(file_path: str) -> List[TrackMetadata]:
        """
        Parse a PLS file using configparser (since it's INI-like).
        """
        tracks = []
        try:
            # PLS is technically INI but without sections sometimes, or with [playlist]
            # We use a trick to make sure it reads correctly if header is missing, though standard is [playlist]
            parser = configparser.ConfigParser()
            parser.read(file_path)

            if not parser.has_section("playlist"):
                logger.error("Invalid PLS file: Missing [playlist] section")
                return []

            count = parser.getint("playlist", "NumberOfEntries", fallback=0)

            for i in range(1, count + 1):
                file_key = f"File{i}"
                title_key = f"Title{i}"
                length_key = f"Length{i}"

                if parser.has_option("playlist", file_key):
                    path = parser.get("playlist", file_key)
                    title_raw = parser.get("playlist", title_key, fallback="Unknown")
                    length = parser.getint("playlist", length_key, fallback=0)

                    artist = "Unknown"
                    title = title_raw

                    if " - " in title_raw:
                        parts = title_raw.split(" - ", 1)
                        artist = parts[0].strip()
                        title = parts[1].strip()

                    tracks.append(TrackMetadata(
                        file_path=path,
                        title=title,
                        artist=artist,
                        duration_seconds=length
                    ))

            logger.info(f"Parsed PLS playlist from {file_path} ({len(tracks)} tracks)")
            return tracks

        except Exception as e:
            logger.error(f"Failed to parse PLS: {e}")
            return []
