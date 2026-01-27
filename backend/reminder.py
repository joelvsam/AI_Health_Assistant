# backend/reminder.py

import schedule
import time
from backend.database import get_connection

def check_medicines():
    """
    Checks for medicines that need a reminder at the current time
    and creates a notification for the user.
    """
    medicines = []
    try:
        # Get all medicines from the database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, time FROM medicines")
        medicines = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f"Error checking medicines: {e}")
        return

    # Get the current time in HH:MM format
    current_time = time.strftime("%H:%M")
    for med in medicines:
        # If the medicine time matches the current time, create a notification
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
    """
    Starts a scheduler that runs the check_medicines function every minute.
    """
    schedule.every(1).minutes.do(check_medicines)

    while True:
        schedule.run_pending()
        time.sleep(1)