# Module 2 — Reflection

**Team name**: armand
**Branch**: `module-02/<team-name>`
**Submitted**: before Module 3 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You built a service with distinct layers: models, schemas, repository, service, and routes — each with a single responsibility.

**Why not just put everything in one file and call it done?**

Think about what happens six months later when someone new joins the team, or when you need to swap SQLite for PostgreSQL. What does the layered structure protect you from?

> *Your answer:* Putting everything in one file is bad pratrice, makes a huge mess, and is just hard to read. If a new developer joins, they won't know where to look to fix a bug and might break the routing while trying to fix a database issue for example. The layers protect us by keeping each things isolated. For example, if we swap SQLite for PostgreSQL, we only have to change the repository and database files. The routes and service files don't even need to know the database changed, so we don't risk breaking the whole API.

---

## 2. Your choice

Each service owns its data exclusively — no other service is allowed to touch its database directly.

**Pick one entity your service owns (e.g. `User`, `Game`). What would go wrong if another service could write to that table directly?**

Give a concrete scenario, not a general principle.
> *Your answer:* I'm picking the Game entity. If the user-service could write directly onto the game database table, it could completely bypass the business rules. For example, lets say the user-service wants to insert a new game but forget to provide a mandatory field like platform, or saves it without running the logic we put in service.py. If only the game-service can touch that database, we can guarantee that all our validation rules are always respected.

---

## 3. The tradeoff

You now have models, schemas, a repository, a service, and routes — five layers for what is essentially a CRUD service.

**For a system this small, what is the cost of all this structure?**

And at what point does the complexity start to pay off? Where is the tipping point?

> *Your answer:* The cost is time and writing a lot of extra code. We had to create and link five different files just to make a simple service that adds and lists games, which seems to be like a lot right now. It it gonna pay off when the app actually starts growing, and scaling. When we need to add complex validation, some more API calls, or even some custom search rules, having this structure means we know exactly where the code goes, and how to do it. It also makes testing way easier because we can test the business logic alone without needing to run the database.


---

*Keep this file. You will refer back to it during the oral presentation.*
