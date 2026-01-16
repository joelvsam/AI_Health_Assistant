import schedule
import time
from backend.database import get_connection

def check_medicines():
    medicines = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, time FROM medicines")
        medicines = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f"Error checking medicines: {e}")
        return

    current_time = time.strftime("%H:%M")
    for med in medicines:
        if med["time"] == current_time:
            print(f"Reminder: Take {med['name']}")

def start_scheduler():
    schedule.every(1).minutes.do(check_medicines)

    while True:
        schedule.run_pending()
        time.sleep(1)
