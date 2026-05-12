import amqp from "amqplib";
import db from "./db";

const RABBITMQ_URL = process.env.RABBITMQ_URL ?? "amqp://guest:guest@localhost:5672";
const QUEUE = "gamehub.notifications";

export async function startConsumer(): Promise<void> {
  const connection = await amqp.connect(RABBITMQ_URL);
  const channel = await connection.createChannel();

  await channel.assertQueue(QUEUE, { durable: true });

  console.log(`[consumer] Waiting for messages on queue: ${QUEUE}`);

  channel.consume(QUEUE, (msg) => {
    if (!msg) return;

    try {
      const payload = JSON.parse(msg.content.toString()) as {
        user_id: string;
        message: string;
      };

      db.prepare(
        "INSERT INTO notifications (user_id, message) VALUES (?, ?)"
      ).run(payload.user_id, payload.message);

      console.log(`[consumer] Notification stored for user ${payload.user_id}: ${payload.message}`);
      channel.ack(msg);
    } catch (err) {
      console.error("[consumer] Failed to process message:", err);
      channel.nack(msg, false, false);
    }
  });
}
