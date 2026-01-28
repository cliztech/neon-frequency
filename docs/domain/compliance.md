# Compliance Logging and Audit Requirements

## Required Logs
- Song plays
- Ad impressions and skips
- All changes (creations, updates, deletions) to metadata (track, artist, album, licensing, rights)
- Time stamps for all logged events (UTC)

## Retention and Export
- Retain compliance logs for a minimum of 2 years, with the ability to extend to 7 years for regulatory holds.
- Support export in CSV and JSON formats for all log query results.

## Audit Trail Requirements
- Maintain an immutable audit trail for log creation, updates, and exports.
- Record actor identity, action type, source system, and time stamp for each audit event.
- Provide traceability from exported records back to original log entries.

## API Endpoints
- `GET /api/compliance/logs` for querying logs with filters (date range, event type, track/artist, ad campaign).
- `POST /api/compliance/logs/export` for requesting exports. The format (CSV or JSON) and log filters should be specified in the request body.
- `GET /api/compliance/logs/exports/{exportId}` for retrieving export status and download links.
