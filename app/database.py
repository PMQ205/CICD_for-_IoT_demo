import sqlite3

DB_NAME = "iot.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS device_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            command TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_event(device_id, command, status):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        """
        INSERT INTO device_events
        (device_id, command, status)
        VALUES (?, ?, ?)
        """,
        (device_id, command, status)
    )

    conn.commit()
    conn.close()


def get_latest_event(device_id):
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.execute(
        """
        SELECT device_id, command, status
        FROM device_events
        WHERE device_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (device_id,)
    )

    result = cursor.fetchone()

    conn.close()

    return result