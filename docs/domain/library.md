# Library Domain

## Ingestion Flow

### Watch Folders
- The library service watches configured import directories for new audio assets.
- When a new file appears, the service stages it in a temporary ingest area and records an ingestion job for auditability.
- Files are validated for supported formats before being promoted into the library.
- Failures (unsupported format, corruption, missing permissions) are captured with an error state so operators can retry or re-route.

### Manual Import
- Operators can trigger a manual import by uploading files or providing a filesystem path.
- Manual imports use the same validation pipeline as watch folders to ensure consistent behavior.
- The system stores an import reason and operator metadata to aid traceability.

## Metadata Extraction and Enrichment

### ID3 and Embedded Tags
- During ingest, embedded metadata (ID3v2, Vorbis, MP4 atoms) is extracted into the library record.
- Core fields include title, artist, album, genre, release year, track number, BPM, and ISRC when present.
- Artwork is extracted and stored as a linked asset with a reference to the track record.

### External Metadata
- If a track has a stable identifier (ISRC, MusicBrainz ID, or internal fingerprint), the enrichment pipeline queries external sources to fill gaps.
- External metadata is merged conservatively: existing authoritative fields are preserved, while missing or low-confidence values are updated.
- Enrichment operations are logged with source attribution to support auditing and rollback.

## Loudness Normalization Strategy

- Each track is analyzed for integrated loudness and true peak prior to normalization.
- The system targets -16 LUFS integrated for general playback, with a configurable alternate target (e.g., -14 LUFS) for streaming profiles.
- Normalization applies gain changes only; it does not alter dynamics beyond the necessary gain adjustment.
- If the required gain would push true peak above -1.0 dBTP, the gain is clamped and the track is flagged for review.

## Duplicate Detection Logic

- The ingest pipeline computes an acoustic fingerprint and a content hash (PCM or decoded audio) for each track.
- Duplicates are detected by:
  - Exact match on content hash (bit-identical audio).
  - High-similarity fingerprint match above a configurable threshold (near-duplicates).
  - Metadata corroboration (same title/artist/album) to reduce false positives.
- When a duplicate is found, the system links the new asset to the existing library entry and records the relationship in the ingest log.

## Search and Filter API Endpoints

- `GET /api/library/tracks`
  - Query params: `q`, `artist`, `album`, `genre`, `year`, `bpm`, `lufs_min`, `lufs_max`, `duration_min`, `duration_max`, `has_artwork`, `source`.
  - Returns paginated results with sorting on `title`, `artist`, `created_at`, or `last_played`.
- `GET /api/library/tracks/{id}`
  - Fetches a single track by ID, including metadata, loudness analysis, and asset links.
- `GET /api/library/tracks/duplicates`
  - Returns potential duplicates with similarity scores and match rationale.
- `POST /api/library/search`
  - Accepts a complex filter object for advanced queries (AND/OR groups, ranges, and tags).
- `GET /api/library/artists`
  - Returns distinct artists with optional `q` and pagination to support filter UI.
