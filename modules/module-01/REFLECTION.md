## YOU NEED TO COMMIT THIS FILE BEFORE MOVING ON TO THE NEXT MODULE ! 🚨

**feel free to delete this comment**

# Module 1 — Reflection

**Team name**: **\*\***\_\_\_**\*\***
**Branch**: `module-01/<team-name>`
**Submitted**: before Module 2 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

You started from a painful monolith. Now you're splitting it into separate services.

**What concrete problem does that split solve: and for whom?**

Think about it from three angles: the developer who has to change code, the team that has to deploy it, and the user who has to live with its failures. You don't need to cover all three, pick the one that felt most real to you today.

> _Your answer:_ From the developer POV, the split solves the problem the mistake that causes the trouble. When we had one system making a change to how a game is added to a users library meant changing the same code that handles logging in sending notifications and keeping track of what people do. One bad merge or even one untested edge case means everything goes down together. If we split into services then a bug in the game service stays in game service. The developer working on it can read the entire service in one, test it isolated, and deploy it without coordinating with all other teams.

---

## 2. Your choice

Look at your service map. Every arrow between two services is a decision someone made.

**Pick one boundary, one place where you decided service A should not be part of service B. Explain why that line exists.**

What would break, slow down, or become harder to manage if you merged those two services back together?

> _Your answer:_ The line I'm most confident about is the one between activity service and logging service.

I could have merged them, because activity service already knows what happened, so why not just write to the audit log directly ? This is because they have completely different jobs, different stakeholders, and also different failure modes.
Activity service is a business service. It must be fast, available, and focused on recording what players do. Logging service is a compliance service wich means it's owned by the legal / data team and it must check GDPR consent before writing anything, also it needs to be the single authoritative audit trail for the whole system (not just activity events, but eventually auth events, admin actions...).
If we merged them then the GDPR consent check would be inside the hot path of every game session. If we change the data retention rules, it would require redeploying the whole service that records gameplay. The compliance team would need to coordinate every deploy with the product team. So the boundary exists to protect both sides from each other's concerns.

---

## 3. The tradeoff

Microservices solve the monolith's problems. But they create new ones.

**Name one thing that was simpler in the monolith and is now harder in your distributed design.**

No need to solve it: just name it honestly. This is exactly the tension the rest of the course is about.

> _Your answer:_ The thing that was simplest in the monolith and is now hardest is tracing a single user action from start to end.
In the monolith, if something went wrong when a user recorded a game session, you can just open one log file and read a single error or stack trace. In the distributed design, that same action goes through a lot of services: activity, logging, notification, while auth have already handled the front half of the request. Each service has its own logs, its own database, and its own error states, wish is much more harder to track and follow.

---

_Keep this file. You will refer back to it during the oral presentation._
