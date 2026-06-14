# Module 5 — Reflection

**Team name**: Armand
**Branch**: `module-05/armand`
**Submitted**: before Module 6 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

The game-service now has two models for the same data: SQLite for writes, Redis for reads. They store the same games in two different shapes.

**Why go through the trouble of maintaining two representations of the same data?**

Think about what kind of queries each model is optimised for, and what would happen if you tried to use the write model for high-traffic read operations.

> *Your answer:* SQLite is very safe for saving data, but it can be slow. Redis is super fast, which makes it perfect for reading. We keep both so saving games is secure, but reading them is instant for the user. If we only used SQLite, our app would slow down or crash when thousands of people try to read a game summary at the same time.

---

## 2. Your choice

The logging-service checks GDPR consent before recording any activity. If a user has not opted in, the log is silently dropped.

**What does this consent check force you to accept about your data?** It is incomplete by design — some activities will never be recorded.

From a system design perspective: where is the right place to enforce this rule — in the logging-service, in the activity-service, or at the gateway? Why?

> *Your answer:* It forces us to accept that our data will never be 100% complete. We will always be missing some user activity. The right place to check this is in the logging service itself. The gateway's only job is to route traffic, so putting complex rules there is a bad idea. The logging service should be the boss of its own privacy rules.

---

## 3. The tradeoff

With CQRS, your write model and read model can drift out of sync — a game is updated in SQLite but the Redis projection still shows the old data.

**In what scenario does this inconsistency matter to the user? In what scenario is it completely acceptable?**

Is there a class of applications where eventual consistency is never acceptable? What are they?

> *Your answer:* It matters when a user pays for a game or changes their password—they expect that to work instantly. It is completely acceptable for things like a game's total views or its summary, where being a few seconds late doesn't hurt anyone. Eventual consistency is never acceptable in banking or healthcare apps, because old or wrong data can cause huge real-world problems.

---

*Keep this file. You will refer back to it during the oral presentation.*
