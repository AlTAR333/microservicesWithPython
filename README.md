# GameHub — Your Microservices Capstone

> EPITA · Microservices with Python

You are going to build a real distributed system from scratch — one service at a time.

By the end of this course, you will have a running gamer social platform where:
- A user signs up, manages their profile, and tracks their game library
- Activity events flow through Kafka to a GDPR-compliant logging service
- Notifications are sent asynchronously via RabbitMQ
- Every request is traceable across services in a single dashboard
- The whole thing deploys with one command

**You build every piece of this yourself.** The modules give you the instructions and the concepts. The code is yours.

---

## How this works

Each module lives in `modules/module-XX/`. Open `exercise.md` to get started.

You will write your services inside the `services/` folder. It is empty on purpose.

**Modules 1–3 are local-first**: you run services directly with `uvicorn` and SQLite — no Docker needed. Infrastructure (Kafka, RabbitMQ, etc.) is introduced from Module 4 onward via `docker-compose.infra.yml`.

```
modules/
├── module-01/   ← Start here
├── module-02/
├── ...
└── module-10/

services/        ← You build this
```

---

## Prerequisites

- Python 3.12
- Node.js 20 (for notification-service)
- A working terminal
- Docker + Docker Compose (from Module 4 onward)

---

## Local development (Modules 1–3)

```bash
# Copy the environment config
cp .env.example .env

# Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows

# Run a service locally
cd services/user-service
uvicorn app.main:app --reload --port 8001
```

Each service uses a local SQLite file — no database server needed.

---

## Starting infrastructure (Module 4+)

```bash
# Start infrastructure services (Kafka, RabbitMQ, etc.)
docker compose -f docker-compose.infra.yml up -d
```

From Module 8 onward, services are containerized and added via overrides:

```bash
docker compose -f docker-compose.infra.yml \
               -f modules/module-08/docker-compose.override.yml \
               up --build
```

---

## What you will have built by Module 10

```
                    ┌─────────────┐
    HTTP ──────────▶│   Traefik   │  API Gateway
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   ┌────────────┐  ┌────────────┐  ┌────────────────┐
   │user-service│  │game-service│  │activity-service│
   │ PostgreSQL │  │ PostgreSQL │  │ PostgreSQL     │
   └────────────┘  │ + Redis    │  └───────┬────────┘
                   └────────────┘      RabbitMQ │ Kafka
                                   ┌───────────┴──────────────┐
                                   ▼                          ▼
                    ┌─────────────────────┐    ┌─────────────────────┐
                    │notification-service │    │  logging-service    │
                    │ Node.js + SQLite    │    │  PostgreSQL         │
                    │ RabbitMQ consumer   │    │  Kafka consumer     │
                    │ (always local)      │    │  GDPR consent       │
                    └─────────────────────┘    └─────────────────────┘
```

---

## Access points (once running)

| Service | URL |
|---|---|
| User Service | http://localhost:8001/docs |
| Game Service | http://localhost:8002/docs |
| Activity Service | http://localhost:8003/docs |
| Notification Service | http://localhost:8004 |
| Logging Service | http://localhost:8005/docs |
| Traefik dashboard | http://localhost:8088 |
| RabbitMQ UI | http://localhost:15672 |
| Grafana | http://localhost:3000 |
| Jaeger | http://localhost:16686 |
| Keycloak | http://localhost:8080 |

---

## Final checklist

You are done when you can demonstrate all six:

- [ ] All services running — local services via uvicorn, containerized services via docker compose
- [ ] Log in via Keycloak → log an activity → notification received → logging-service records event (with consent)
- [ ] Grafana shows RED metrics (Rate, Errors, Duration) for each service
- [ ] Jaeger shows a full distributed trace for one activity request
- [ ] Stop `logging-service` → circuit breaker opens → restart → circuit recovers
- [ ] Push a commit → GitHub Actions builds and tests automatically
