import time
from backend.database import get_connection

def run_reminders():
    while True:
        now = time.strftime("%H:%M")
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM medicines WHERE time = ?", (now,))
        for row in cur.fetchall():
            print(f"Reminder: Take {row['name']}")
        conn.close()
        time.sleep(60)
