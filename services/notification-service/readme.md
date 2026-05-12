# Notification Service

```
notification-service/
  ├── src/
  │   ├── index.ts       ← starts HTTP server + consumer
  │   ├── consumer.ts    ← RabbitMQ consumer → SQLite
  │   ├── db.ts          ← SQLite init
  │   └── routes.ts      ← GET /notifications, GET /notifications/:user_id
  ├── package.json
  ├── tsconfig.json
  └── .env.example
```
