from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import logging
from core.brain.music_library import MusicLibrary, Track, TrackMetadata, Energy
from core.brain.radio_automation import PlaylistOptimizer

logger = logging.getLogger(__name__)

@dataclass
class CrateDigger:
    """
    The Music Director Agent.
    Responsible for ingesting music, managing the library, and finding tracks.
    """
    library_path: str = "./music_library.json"
    library: MusicLibrary = field(default_factory=lambda: MusicLibrary())

    def __post_init__(self):
        # In a real scenario, we might load from disk here
        # self.library.load(self.library_path)
        pass

    def ingest_directory(self, directory: str) -> int:
        """Scans a directory for new music and adds it to the library."""
        logger.info(f"CrateDigger scanning: {directory}")
        return self.library.scan_directory(directory)

    def search(self, query: str) -> List[Track]:
        """Finds tracks matching a query (artist, title, genre)."""
        return self.library.search_tracks(query)

    def get_rotation_candidate(self, category: str = "general") -> Optional[Track]:
        """
        Pulls a track for a specific rotation category.
        TODO: Implement complex rotation logic (Hot, Recurrent, Gold).
        """
        # For now, just return a random track
        import random
        if not self.library.tracks:
            return None
        return random.choice(list(self.library.tracks.values()))

@dataclass
class FlowMaster:
    """
    The Sequencing Engine Agent.
    Responsible for transitions, segregation, and creating smooth sets.
    """
    optimizer: PlaylistOptimizer = field(default_factory=PlaylistOptimizer)

    def analyze_segue(self, track_a: Track, track_b: Track) -> Dict[str, Any]:
        """Calculates the best transition between two tracks."""
        score = self.optimizer.calculate_transition_score(track_a, track_b)
        crossfade = self.optimizer.suggest_crossfade(track_a, track_b)
        
        return {
            "score": score,
            "crossfade_duration": crossfade,
            "energy_change": track_b.metadata.energy.value - track_a.metadata.energy.value if track_a.metadata.energy and track_b.metadata.energy else 0,
            "bpm_diff": abs(track_a.metadata.bpm - track_b.metadata.bpm) if track_a.metadata.bpm and track_b.metadata.bpm else 0
        }

    def craft_set(self, seed_track: Track, length_minutes: int, library: MusicLibrary) -> List[Track]:
        """
        Builds a coherent set of music starting from a seed track.
        """
        playlist = [seed_track]
        current_duration = seed_track.metadata.duration or 180
        target_duration = length_minutes * 60
        
        current_track = seed_track
        
        # Simple greedy selection for now
        # In a full implementation, this would use beam search or similar
        attempts = 0
        while current_duration < target_duration and attempts < 100:
            attempts += 1
            # Find candidates (naive: random for now, but should use CrateDigger logic)
            # This shows the need for collaboration between agents
            
            # Using internal logic for now to demonstrate FlowMaster responsibility
            candidates = list(library.tracks.values())
            best_next = None
            best_score = -1
            
            import random
            random.shuffle(candidates) # randomize check order
            
            for candidate in candidates[:20]: # Check 20 random candidates
                if candidate in playlist:
                    continue
                
                score = self.optimizer.calculate_transition_score(current_track, candidate)
                if score > best_score:
                    best_score = score
                    best_next = candidate
            
            if best_next and best_score > 0.6: # Quality threshold
                playlist.append(best_next)
                current_track = best_next
                current_duration += best_next.metadata.duration or 180
                attempts = 0 # Reset attempts on success
            elif attempts > 50:
                 # Fallback if no good match found quickly
                 if candidates:
                     fallback = random.choice(candidates)
                     if fallback not in playlist:
                         playlist.append(fallback)
                         current_track = fallback
                         current_duration += fallback.metadata.duration or 180

        return playlist
