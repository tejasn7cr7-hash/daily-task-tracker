import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

SENDER_EMAIL = os.getenv("EMAIL_USER")
APP_PASSWORD = os.getenv("EMAIL_PASSWORD")
def send_reminder_email(to_email, task_title):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = "⏰ Daily Task Tracker Reminder"

        body = f"""
Task Reminder

Don't forget:

{task_title}
        """

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(
            SENDER_EMAIL,
            APP_PASSWORD
        )

        result = server.sendmail(
            SENDER_EMAIL,
            to_email,
            msg.as_string()
        )

        print("SMTP Result:", result)

        server.quit()

        print(f"Email sent to {to_email}")
        return True

    except Exception as e:
        print("Email Error:", e)
        return False