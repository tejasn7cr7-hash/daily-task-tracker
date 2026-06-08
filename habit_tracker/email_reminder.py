import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Task

# ── Gmail credentials ──
GMAIL_ADDRESS = "tejasn7cr7@gmail.com"
GMAIL_APP_PASSWORD = "gwqw phhi yrmd opka"

notified_today = set()

def send_email(to_email: str, user_name: str, task_title: str, reminder_time: str):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"⏰ Reminder: {task_title}"
        msg["From"] = f"Daily Task Tracker <{GMAIL_ADDRESS}>"
        msg["To"] = to_email

        html = f"""
        <html>
        <body style="margin:0;padding:0;background:#0e0e11;font-family:Arial,sans-serif;">
          <div style="max-width:500px;margin:30px auto;background:#16161a;border-radius:16px;overflow:hidden;border:1px solid #2a2a35;">
            <div style="background:#c8f135;padding:20px 30px;">
              <h1 style="margin:0;color:#000;font-size:22px;">⏰ Task Reminder</h1>
              <p style="margin:4px 0 0;color:#333;font-size:13px;">Daily Task Tracker — Sapthagiri NPS University</p>
            </div>
            <div style="padding:30px;">
              <p style="color:#aaa;font-size:15px;margin:0 0 10px;">Hi <b style="color:#f0f0f5;">{user_name}</b>!</p>
              <p style="color:#aaa;font-size:15px;margin:0 0 20px;">This is your reminder for:</p>
              <div style="background:#0e0e11;border-left:4px solid #c8f135;padding:16px 20px;border-radius:8px;margin-bottom:20px;">
                <h2 style="margin:0;color:#c8f135;font-size:20px;">{task_title}</h2>
                <p style="margin:6px 0 0;color:#666;font-size:13px;">Scheduled at {reminder_time}</p>
              </div>
              <p style="color:#555;font-size:12px;margin:0;">Open your app to mark it as done:</p>
              <a href="https://daily-task-tracker-z95v.onrender.com" 
                 style="display:inline-block;margin-top:10px;background:#c8f135;color:#000;padding:10px 24px;border-radius:8px;text-decoration:none;font-weight:bold;font-size:14px;">
                Open App →
              </a>
            </div>
            <div style="padding:16px 30px;border-top:1px solid #2a2a35;">
              <p style="margin:0;color:#444;font-size:11px;">Daily Task Tracker • Sapthagiri NPS University Mini Python Project</p>
            </div>
          </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())

        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Email sent to {to_email} for task: {task_title}")

    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Email error: {e}")

def check_and_send_reminders():
    today = datetime.now().date().isoformat()
    current_time = datetime.now().strftime("%H:%M")

    db: Session = SessionLocal()
    try:
        tasks = db.query(Task).filter(
            Task.is_done == False,
            Task.reminder_time == current_time,
            Task.user_email != None
        ).all()

        for task in tasks:
            task_key = f"{task.id}_{today}"
            if task_key in notified_today:
                continue

            print(f"[{current_time}] 🔔 Sending reminder for: {task.title} → {task.user_email}")
            threading.Thread(
                target=send_email,
                args=(task.user_email, task.user_name or "User", task.title, current_time),
                daemon=True
            ).start()
            notified_today.add(task_key)

    finally:
        db.close()
