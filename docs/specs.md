# Tech Stack

On the Python side for the microservices, you've got FastAPI for the API framework, SQLAlchemy for the database relationship mapping, Pydantic for schema validation, and Keycloak for managing authentication and identity. Kafka handles real-time event streaming, and RabbitMQ handles background task messaging. The databases include PostgreSQL for relational storage (from Module 8) and Redis for caching. SQLite is used for local development in Modules 1–7.

The notification-service runs on Node.js with SQLite — always local, never containerized. GitHub Actions manages Docker deployments and the CI/CD pipeline.

## Logging Service

The logging-service is a GDPR-compliant service that gathers data with respect for user preferences. It stores opt-in status for activity tracking. If a user chooses not to opt in, their actions are not recorded, but they may lose specific features like personalized recommendations or some social elements.

On the legal side, having detailed, structured logs that tie actions to a user allows you to trace activity and respect information requests if something illegal happens. These logs are managed as append-only JSONL files.

In Modules 1–7, the logging-service uses SQLite for consent storage. From Module 8 onward, it switches to PostgreSQL.

## Stack Overview

The stack is a combination of microservices, Kafka, RabbitMQ, PostgreSQL, Redis, SQLite, Node.js, and Docker.

- Microservices: FastAPI, SQLAlchemy, Pydantic, Keycloak
- Kafka: Real-time event streaming (activity → logging)
- RabbitMQ: Background tasks (activity → notification)
- PostgreSQL: Relational storage (production, from Module 8)
- SQLite: Local development storage (Modules 1–7), notification-service (always)
- Redis: Caching
- Node.js: notification-service (local, never containerized)
- Docker: Containerization (infrastructure from Module 4, services from Module 8)
- GitHub Actions: CI/CD
