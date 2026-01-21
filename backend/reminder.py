import schedule
import time
from backend.database import get_connection

def check_medicines():
    medicines = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, time FROM medicines")
        medicines = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f"Error checking medicines: {e}")
        return

    current_time = time.strftime("%H:%M")
    for med in medicines:
        if med["time"] == current_time:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO notifications (user_id, message) VALUES (?, ?)",
                    (med["user_id"], f"Time to take your medicine: {med['name']}")
                )
                conn.commit()
                conn.close()
                print(f"Reminder for user {med['user_id']}: Take {med['name']}")
            except Exception as e:
                print(f"Error creating notification: {e}")

def start_scheduler():
    schedule.every(1).minutes.do(check_medicines)

    while True:
        schedule.run_pending()
        time.sleep(1)
