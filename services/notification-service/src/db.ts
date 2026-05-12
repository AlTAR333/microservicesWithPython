import Database from "better-sqlite3";

const db = new Database("notifications.db");

db.exec(`
  CREATE TABLE IF NOT EXISTS notifications (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id   TEXT    NOT NULL,
    message   TEXT    NOT NULL,
    received_at TEXT  NOT NULL DEFAULT (datetime('now'))
  )
`);

export default db;
