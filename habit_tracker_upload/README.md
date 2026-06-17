# DayFlow — Habit & Task Tracker
## How to Run & Deploy (No Coding Experience Needed!)

---

## 🖥️ Run on Your Computer (Test Locally)

### Step 1 — Install Python
1. Go to https://www.python.org/downloads/
2. Click the big yellow "Download Python" button
3. Run the installer — **check the box "Add Python to PATH"** before clicking Install

### Step 2 — Open Terminal (Command Prompt)
1. Press `Windows key + R`
2. Type `cmd` and press Enter

### Step 3 — Go to the project folder
Type this and press Enter (change the path to where you saved the folder):
```
cd C:\Users\YourName\Downloads\habit_tracker
```

### Step 4 — Install dependencies
```
pip install -r requirements.txt
```

### Step 5 — Run the app
```
uvicorn main:app --reload
```

### Step 6 — Open in browser
Go to: **http://localhost:8000**

Your app is running! 🎉

---

## 🌐 Put It Online (Free) with Render

### Step 1 — Create a GitHub account
Go to https://github.com and sign up for free.

### Step 2 — Upload your project
1. Click the `+` button → "New repository"
2. Name it `dayflow-tracker`, click "Create repository"
3. Upload all the files from the `habit_tracker` folder

### Step 3 — Deploy on Render
1. Go to https://render.com and sign up (free)
2. Click "New" → "Web Service"
3. Connect your GitHub account and select your repository
4. Render will auto-detect the `render.yaml` file
5. Click **Deploy** — wait ~2 minutes

### Step 4 — Your app is live! 🚀
Render gives you a URL like `https://dayflow-tracker.onrender.com`
Share it with anyone!

---

## 📱 Features
- **Habits** — Track daily habits, see streaks, mark complete each day
- **Tasks** — Add tasks with priority (low/medium/high) and due dates
- **Stats** — See your completion rate and best streak

---

## ❓ Need Help?
If anything doesn't work, just ask Claude for help!
