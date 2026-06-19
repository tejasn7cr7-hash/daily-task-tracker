import time
import threading
from datetime import datetime
from plyer import notification
import winsound
import requests

from services.email_service import send_reminder_email
CHECK_INTERVAL = 30  # check every 30 seconds
API_URL = "http://localhost:8000/api/tasks/"
notified_today = set()  # track which tasks already notified today

def play_alarm():
    """Play beep sound for 10 seconds"""
    for _ in range(10):
        winsound.Beep(1000, 500)  # 1000Hz for 0.5s
        time.sleep(0.5)

def send_notification(task_title, due_time):
    notification.notify(
        title="⏰ Task Reminder — Daily Task Tracker",
        message=f"Time to: {task_title}\nScheduled at {due_time}",
        app_name="Daily Task Tracker",
        timeout=15
    )
    # Play alarm in separate thread so notification shows immediately
    threading.Thread(target=play_alarm, daemon=True).start()

def check_reminders():
    global notified_today

    today = datetime.now().date().isoformat()

    try:
        res = requests.get(API_URL, timeout=5)
        tasks = res.json()
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Could not reach app: {e}")
        return

    now = datetime.now()
    current_time = now.strftime("%H:%M")

    for task in tasks:
        if task.get("is_done"):
            continue

        reminder_time = task.get("reminder_time")

        if not reminder_time:
            continue

        task_key = f"{task['id']}_{today}_{reminder_time}"

        if task_key in notified_today:
            continue

        if current_time == reminder_time:
            print(f"[{current_time}] 🔔 Reminder: {task['title']}")

            send_notification(task['title'], reminder_time)

            if task.get("email"):
                print("Sending email to:", task["email"])

                send_reminder_email(
                    task["email"],
                    task["title"]
               )

           notified_today.add(task_key)
def main():
    print("=" * 50)
    print("  Daily Task Tracker — Reminder Service")
    print("  Running in background. Keep this open!")
    print("=" * 50)
    print(f"  Checking reminders every {CHECK_INTERVAL} seconds...")
    print("  Press Ctrl+C to stop.\n")

    while True:
        check_reminders()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
