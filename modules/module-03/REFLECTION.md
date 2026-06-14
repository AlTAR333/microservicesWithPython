# Module 3 — Reflection

**Team name**: armand
**Branch**: `module-03/armand`
**Submitted**: before Module 4 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

All client requests now go through the gateway. No client ever calls a service directly.

**Why does that single entry point exist? What would the client's life look like without it?**

Think about what the client would need to know and manage if it talked to each service on its own port.

> *Your answer:* Without the gateway, the client would have to know or even sometime memorize the exact IP address and the port of every single microservice. If we also changed a port or moved a service, the frontend would break because the info would be wrong. With the gateway, The client only needs to know one address with the port 8000, and the gateway just handles figuring out where the request should actually go in the background.

---

## 2. Your choice

The activity-service makes two outbound calls: one to validate the user (with retry logic), one to fetch game data (with a null fallback if it fails).

**Why are these two calls treated differently? Why does one retry and the other just give up gracefully?**

What is the consequence for the user in each case if the downstream service is unavailable?

> *Your answer:* If the user doesn't exist, we cannot save the activity for them, so it could crash. We retry to be sure 100% that the user service isn't just having a small temporary problem. However, fetching the game data is just an extra feature, it is optionnal. If the game service is down, it's better to just let the user save their activity and just return something like "game": null rather than blocking them from using the app entirely.

---

## 3. The tradeoff

Every time a client creates an activity, three services are involved synchronously. They all have to be running, healthy, and fast.

**What is the systemic risk of chaining synchronous calls like this?**

What happens to the user experience if the slowest service in the chain takes 3 seconds to respond?

> *Your answer:* The risk is that the whole chain is getting slowed by the slowest link, reducing the maximum speed of the whole services. If the game service takes for example 3 seconds to respond, the activity service is stuck waiting for 3 seconds, which means that the user is just gonna be staring at a loading screen for 3 seconds, because of 1 small service. Also, if they are tied together synchronously like this, a crash in one service can cause a traffic jam that crashes the other services that is waiting on it. Not good.

---

*Keep this file. You will refer back to it during the oral presentation.*
