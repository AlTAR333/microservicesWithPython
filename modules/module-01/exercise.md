# Module 1 — Service Decomposition

**Duration**: 2h in class
**Branch to submit**: `module-01/armand`

---

## Objective

Before writing a single line of code, you need to design the system on paper. Every decision you make here: where to draw service boundaries, who owns what data, how services talk to each other, is hard to reverse once you start coding.

This module is about slowing down and thinking like an architect, not a developer.

Read these two documents before doing anything else:

- `docs/domain.md` — what GameHub is and who uses it
- `docs/specs.md` — the tech stack and key architectural decisions

> The CTO has already laid out the `services/` folder structure. Use it as a starting point, but your job is to **justify** why each folder deserves to be its own service — not just accept it.

---

## Task 1 — Identify bounded contexts _(~40 min)_

A bounded context is a part of the system that has a clear responsibility and owns its data exclusively. No other service should reach into its database.

| Bounded Context      | Responsibilities                                                                      | Owned Entities                  | Team         |
| -------------------- | ------------------------------------------------------------------------------------- | ------------------------------- | ------------ |
| Identity             | Manages who users are, handles registration, login, and profiles                      | User, Session                   | Platform     |
| Auth                 | Issues and validates JWT tokens; decoupled from identity so token logic can evolve independently | Token, Secret                   | Platform     |
| Game Library         | Manages the catalogue of games, metadata, and each user's personal game collection   | Game, UserGame, Genre           | Catalog      |
| Activity             | Records what users do (play sessions, achievements, events); source of truth for behavior data | Activity, Event                 | Data         |
| Notification         | Delivers real-time and async notifications to users across channels (email, push)     | Notification, NotificationPrefs | Engagement   |
| Logging / Audit      | Stores an immutable, GDPR-compliant audit trail of all significant system events      | LogEntry, ConsentRecord         | Compliance   |

---

## Task 2 — Define service contracts _(~30 min)_

### Contract 1 — User registration triggers an activity seed

```
user-service → activity-service
Trigger: a new user completes registration
Protocol: RabbitMQ message (async)
Payload: { user_id, registered_at }
Why async: user-service must not wait on activity-service to confirm the registration response. A slow or crashed activity-service should never block sign-up.
```

### Contract 2 — Activity recorded, logging and notification fan-out

```
activity-service → logging-service
Trigger: any activity event is persisted
Protocol: RabbitMQ message (async)
Payload: { activity_id, user_id, action, game_id, timestamp }
Why async: logging is fire-and-forget from the activity service's perspective. Synchronous coupling would mean a GDPR consent failure blocks the user's action.

activity-service → notification-service
Trigger: activity qualifies for a user notification (e.g. achievement unlocked)
Protocol: RabbitMQ message (async)
Payload: { user_id, notification_type, context: { game_id, achievement_id } }
Why async: notification delivery latency (email, push) must not stall the activity write path.
```

### Contract 3 — Gateway authenticates every inbound request

```
gateway → auth-service
Trigger: every inbound HTTP request carrying a Bearer token
Protocol: REST (synchronous — the gateway must know if the token is valid before forwarding)
Payload (request): { token }
Payload (response): { valid: bool, user_id, roles }
Why sync: authentication is a prerequisite for routing. An async check here would require the gateway to buffer requests, which adds latency and complexity with no benefit.
```

### Contract 4 — Gateway routes to downstream services

```
gateway → user-service / game-service / activity-service
Trigger: authenticated request arrives for a resource
Protocol: REST (synchronous HTTP proxy)
Payload: forwarded request with injected user context header (X-User-Id, X-User-Roles)
Note: downstream services trust the gateway's injected headers and never re-validate tokens themselves.
```

---

## Task 3 — Service map _(~20 min)_

Drawn on paper, then sent to Gemini to turn into Ascii :
```
                        ┌──────────────────────────┐
   Client (HTTP) ─────▶│         gateway          │  port 8000
                        │   JWT validation         │
                        │   request routing        │
                        └──────┬───────┬──────┬────┘
                               │ REST  │ REST │ REST
              ┌────────────────┘       │      └──────────────────┐
              ▼     SQLite Postgres    ▼                         ▼
     ┌─────────────────┐    ┌──────────────────┐    ┌───────────────────────┐
     │  user-service   │    │  game-service    │    │   activity-service    │
     │  port 8001      │    │  port 8002       │    │   port 8003           │
     └────────┬────────┘    └──────────────────┘    └────────┬──────────────┘
              │                                              │
              │ - - - RabbitMQ (async) - - - - - - - - - - - ┤
              │                                              │
              │                        ┌─────────────────────┼──────────────────────┐
              │                        ▼ (async)             ▼ (async)              │
              │             ┌──────────────────────┐  ┌──────────────────────┐      │
              │             │  notification-service│  │   logging-service    │      │
              │             │  port 8004           │  │   port 8006          │      │
              │             │  Node.js             │  │   GDPR consent check │      │
              │             └──────────────────────┘  └──────────────────────┘      │
              │                                                                     │
              └─────────────────── - - - RabbitMQ (async) - - ──────────────────────┘

     ┌──────────────────┐
     │   auth-service   │◀── REST (sync) ── gateway
     │   port 8005      │
     │   issues JWT     │
     └──────────────────┘
```

---

## Discussion _(~15 min)_

Three questions discussed as a team:

1. **Why Node.js for notification-service?**
   Notification-service has many multiply open connections like WebSocket or SSE that are waiting for events to deliver. the non-blocking event of Node.js loop handles this far more cheaply than spawning a Python thread per each connection. This choice is only possible because it's a microservice. It has a single responsibility and communicates with RabbitMQ, so there is no language boundary for everyone.

2. **Why async between activity-service and logging-service?**
   If the call was synchronous then a slow GDPR consent check or also a crashed logging-service would make failure happen back up to the user's action (for exemple recording a game session). Async decouples the availability of two very different SLAs: the activity write path must be fast and reliable; the compliance log can tolerate a short delay.

3. **Why does logging-service need a GDPR consent check?**
   Recording user behaviour without consent is illegal for the GDPR. The logging service is the only place where all of the audit data passes, wich puts the consent check here and means no other service needs to know about it. If consent is revoked, only logging service needs to change.

---

## Minimum to submit this branch

- [X] Bounded context table filled in (6 services justified)
- [X] 4 service contracts defined
- [X] Service map committed (ASCII)
- [X] `REFLECTION.md` completed and committed
