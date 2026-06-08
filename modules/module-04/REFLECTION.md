# Module 4 — Reflection

**Team name**: _______________
**Branch**: `module-04/<team-name>`
**Submitted**: before Module 5 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

In Module 3, services called each other directly over HTTP. Now activity-service drops a message into a broker and moves on — it never waits for a reply.

**What does the activity-service gain by not waiting? And what does the notification-service gain by consuming at its own pace?**

Think about what happens under load, or when notification-service is temporarily down.

> *Your answer:* The activity-service will just gain speed and more reliability, because it doesn't have to freeze and wait, so the user's request finishes instantly. The notification-service also gains stability. Lets say 1000 users log activities at the exact same second, the notification service won't crash from the big and huge traffic spike. It will just pull messages from the queue one by one at a pace it can handle.

---

## 2. Your choice

In Module 3 you already knew how to call another service directly over HTTP — you did it for user validation and game enrichment.

**Why not use the same approach for notifications? What does introducing a broker give you that a direct HTTP call doesn't?**

Think about what happens if notification-service is slow, or crashes mid-message.

> *Your answer:* If we used direct HTTP and the notification-service happened to be offline or restarting, the HTTP call would fail and be completly lost man, that notification would be lost fo-re-ver. It seem that the broker acts as like a safety net. If the notification-service crashes, the messages just wait safely inside the RabbitMQ queue until the service wakes back up and processes them all.

---

## 3. The tradeoff

With synchronous REST, you get an immediate answer: success or failure. With async messaging, the activity is saved and the message is sent — but you have no idea if the notification was ever delivered.

**How would a user know if their notification was never sent? How would you know as a developer?**

What visibility do you lose when you go async?

> *Your answer:* If this happened, the user wouldn't know at all, wich means their app would just say "Activity Saved!" and they would just wonder why their friend never got the alert. From our POV, the only way I would know is if I actively logged into the RabbitMQ dashboard to see if messages are stuck in the queue, or if I checked the error logs in the notification-service.

---

*Keep this file. You will refer back to it during the oral presentation.*