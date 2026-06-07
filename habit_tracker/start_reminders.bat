@echo off
echo Installing reminder dependencies...
pip install plyer requests
echo.
echo Starting Reminder Service...
echo Keep this window open to receive notifications!
echo.
python reminder.py
pause
