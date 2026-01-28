# Scheduling Domain

## Entities

### StationClock
A **StationClock** represents a reusable blueprint for a full hour of programming.
It is composed of **HourTemplates** and resolved into concrete **Rules** at runtime.

### HourTemplate
An **HourTemplate** is a 60-minute layout that specifies the intended placement of
**RotationCategories**, **Breaks**, and **Sweepers** within the hour. Templates are
parameterized (e.g., with dayparts or rotation weights) so that rules can shift
content without rewriting the full clock.

### RotationCategory
A **RotationCategory** groups audio or content items (e.g., Power Recurrent, Gold,
Local Weather). It defines how frequently items rotate and which inventory feeds
the **Rules** that schedule items into a **StationClock**.

### Rule
A **Rule** is the directive that resolves inventory into a scheduled slot. Rules
can express constraints (e.g., "no back-to-back artists"), fallback behavior, and
priority ordering when conflicts arise.

### Daypart
A **Daypart** represents a slice of the day (e.g., Morning Drive 06:00–10:00) used
to apply different **HourTemplates** and **Rules**.

### Break
A **Break** is a collection of spots or content within a clock. Breaks define fixed
boundaries (start times, duration, and position) to ensure commercial inventory
is placed consistently.

### Sweeper
A **Sweeper** is a short branding element scheduled between songs or segments.
Sweepers can be treated as their own category or as a sub-slot within a break.

### ID
An **ID** is the stable identifier used across scheduling components to resolve
relationships between **RotationCategories**, **Rules**, and inventory items.

## Examples

### Example: 60-minute clock
The following example shows a 60-minute **StationClock** broken into segments.
The times are offsets within the hour, and each segment is linked to a category
or break.

| Offset | Duration | Segment | Notes |
| --- | --- | --- | --- |
| 00:00 | 00:30 | Sweeper | Hour open ID + branding |
| 00:30 | 03:30 | RotationCategory: Power | Music slot |
| 04:00 | 04:00 | Break A | Spots + promo |
| 08:00 | 03:30 | RotationCategory: Recurrent | Music slot |
| 11:30 | 00:30 | Sweeper | Voice ID |
| 12:00 | 04:00 | Break B | Spots |
| 16:00 | 03:30 | RotationCategory: Gold | Music slot |
| 19:30 | 00:30 | Sweeper | Branding |
| 20:00 | 04:00 | Break C | Spots |
| 24:00 | 03:30 | RotationCategory: Power | Music slot |
| 27:30 | 00:30 | Sweeper | Voice ID |
| 28:00 | 04:00 | Break D | Spots |
| 32:00 | 03:30 | RotationCategory: Recurrent | Music slot |
| 35:30 | 00:30 | Sweeper | Branding |
| 36:00 | 04:00 | Break E | Spots |
| 40:00 | 03:30 | RotationCategory: Gold | Music slot |
| 43:30 | 00:30 | Sweeper | Voice ID |
| 44:00 | 04:00 | Break F | Spots |
| 48:00 | 03:30 | RotationCategory: Power | Music slot |
| 51:30 | 00:30 | Sweeper | Branding |
| 52:00 | 04:00 | Break G | Spots |
| 56:00 | 04:00 | RotationCategory: Recurrent | Music slot |

### Conflict resolution rules
When multiple rules apply to a slot, resolve in the following order:

1. **Hard constraints** (compliance, "no adjacent artist", legal IDs). Slots that
   fail hard constraints are rejected immediately.
2. **Priority ordering** by rule priority (e.g., higher-priority rules reserve
   inventory first).
3. **Balancing logic** (e.g., weight or recurrence) to select among remaining
   candidates.
4. **Fallback rule** if no candidates remain (e.g., use a filler bed or secondary
   category).

Example conflict resolution:

- Slot requires RotationCategory "Power".
- Rule A: "no same artist within 45 minutes" (hard constraint).
- Rule B: "prefer new releases" (priority 90).
- Rule C: "balance tempo" (priority 60).

If the latest available Power item is a repeat artist, Rule A rejects it and Rule B
selects the next eligible new release. If no eligible items remain, fallback to a
"Power Secondary" category.

## Potential database schema

### station_clocks
- **id** (PK, UUID)
- **name** (string)
- **description** (string)
- **duration_seconds** (integer, typically 3600)
- **created_at** (timestamp)
- **updated_at** (timestamp)

### hour_templates
- **id** (PK, UUID)
- **station_clock_id** (FK → station_clocks.id)
- **daypart_id** (FK → dayparts.id, nullable)
- **name** (string)
- **version** (integer)
- **effective_at** (timestamp)

### rotation_categories
- **id** (PK, UUID)
- **name** (string)
- **code** (string)
- **rotation_minutes** (integer)
- **weight** (integer)
- **active** (boolean)

### rules
- **id** (PK, UUID)
- **rotation_category_id** (FK → rotation_categories.id)
- **priority** (integer)
- **rule_type** (enum: hard, soft, fallback)
- **definition** (jsonb)
- **active** (boolean)

### dayparts
- **id** (PK, UUID)
- **name** (string)
- **start_time** (time)
- **end_time** (time)
- **timezone** (string)

### breaks
- **id** (PK, UUID)
- **hour_template_id** (FK → hour_templates.id)
- **offset_seconds** (integer)
- **duration_seconds** (integer)
- **name** (string)
- **position** (integer)

### sweepers
- **id** (PK, UUID)
- **name** (string)
- **duration_seconds** (integer)
- **rotation_category_id** (FK → rotation_categories.id, nullable)

### schedule_slots
- **id** (PK, UUID)
- **hour_template_id** (FK → hour_templates.id)
- **offset_seconds** (integer)
- **duration_seconds** (integer)
- **slot_type** (enum: rotation, break, sweeper)
- **rotation_category_id** (FK → rotation_categories.id, nullable)
- **break_id** (FK → breaks.id, nullable)
- **sweeper_id** (FK → sweepers.id, nullable)

### ids
- **id** (PK, UUID)
- **entity_type** (string)
- **entity_id** (UUID)
- **external_id** (string)
- **source** (string)

## API endpoints

### Create schedule
**POST** `/api/v1/schedules`

Request body:
```json
{
  "station_clock_id": "uuid",
  "daypart_id": "uuid",
  "start_date": "2024-10-01",
  "end_date": "2024-10-07",
  "timezone": "America/New_York"
}
```

Response:
```json
{
  "schedule_id": "uuid",
  "status": "queued",
  "created_at": "2024-10-01T00:00:00Z"
}
```

### Export schedule
**GET** `/api/v1/schedules/{schedule_id}/export`

Query params:
- **format**: `json` | `csv` | `xml`
- **timezone**: `America/New_York`

Response:
```json
{
  "schedule_id": "uuid",
  "format": "json",
  "exported_at": "2024-10-08T12:00:00Z",
  "items": [
    {
      "offset_seconds": 0,
      "duration_seconds": 30,
      "slot_type": "sweeper",
      "rotation_category_id": "uuid",
      "asset_id": "uuid"
    }
  ]
}
```
