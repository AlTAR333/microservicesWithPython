GDPR-compliant logging-service:

> **Storage**: SQLite in Modules 1–7, PostgreSQL from Module 8 onward.

- Consent management — stores opt-in/opt-out status per user (the "decision" record)
- Kafka consumer — receives activity events from activity-service; if user opted in → writes a structured entry to an append-only JSONL audit log file (mounted volume); if opted out → skips
  silently - REST endpoints exposed to other services:
  - POST /consent/{user_id} — record consent decision
  - GET /consent/{user_id} — check status (used by activity-service, game-service before
    processing)
  - DELETE /logs/{user_id} — GDPR right to erasure - Feature gating — activity-service and game-service query consent before publishing events or  
    serving personalised content; no consent = no recommendations, no activity feed
- Log file format — JSONL: one line per event { timestamp, user_id, action, service, ip_hash } — IP is hashed (not stored raw, GDPR Art. 25 data minimisation)
