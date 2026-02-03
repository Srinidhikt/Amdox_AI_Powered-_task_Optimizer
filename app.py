from flask import Flask, render_template, request, redirect, url_for, session, send_file
import csv
import os
from io import BytesIO
import matplotlib.pyplot as plt
from datetime import datetime
from main import detect_emotions, suggest_tasks, save_to_csv  # main.py functions

app = Flask(__name__)
app.secret_key = "secret123"
EMPLOYEE_CSV = "employees.csv"
HR_CSV = "hr_accounts.csv"
MOOD_CSV = "mood_history.csv"  # stores empid + latest emotions
EMP_MOOD_HISTORY_CSV = "employee_mood_history.csv"  # stores all sentences
def load_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_csv(filename, fieldnames, data_list):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)

def append_csv(filename, fieldnames, row):
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

#emp routes
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/emp_create", methods=["GET", "POST"])
def emp_create():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        empid = request.form["empid"]
        password = request.form["password"]
        employees = load_csv(EMPLOYEE_CSV)
        if any(emp['empid'] == empid for emp in employees):
            error = "Employee ID already exists"
            return render_template("emp_create.html", error=error)
        employees.append({"username": username, "empid": empid, "password": password})
        save_csv(EMPLOYEE_CSV, ["username", "empid", "password"], employees)
        append_csv(MOOD_CSV, ["empid", "mood"], {"empid": empid, "mood": ""})
        return redirect(url_for("emp_login"))
    return render_template("emp_create.html", error=error)

#emp_login route
@app.route("/emp_login", methods=["GET", "POST"])
def emp_login():
    error = None
    if request.method == "POST":
        empid = request.form["empid"]
        password = request.form["password"]
        employees = load_csv(EMPLOYEE_CSV)
        emp = next((e for e in employees if e["empid"] == empid and e["password"] == password), None)
        if emp:
            session["empid"] = empid
            session["empname"] = emp["username"]
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid Employee ID or Password"
    return render_template("emp_login.html", error=error)
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "empid" not in session:
        return redirect(url_for("emp_login"))
    empid = session["empid"]
    empname = session["empname"]
    mood_history = load_csv(EMP_MOOD_HISTORY_CSV)      # loading employee moods from employee_mood_history.csv
    emp_moods = []
    for row in mood_history:
        if row["emp_id"] == empid:
            emotions = row["emotions"].split(",")
            tasks = suggest_tasks(emotions)
            emp_moods.append({
                "emotions": ", ".join(emotions),
                "tasks": tasks,
                "timestamp": row["timestamp"]
            })
    if request.method == "POST":
        sentence = request.form["mood"]
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
        emotions = detect_emotions(sentence)
        tasks = suggest_tasks(emotions)
        save_to_csv(timestamp, empid, empname, sentence, emotions)
        append_csv(MOOD_CSV, ["empid", "mood"], {"empid": empid, "mood": ",".join(emotions)})
        emp_moods.append({
            "emotions": ", ".join(emotions),
            "tasks": tasks,
            "timestamp": timestamp
        })
    return render_template("dashboard.html", empid=empid, empname=empname, moods=emp_moods)
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# create_hr route
@app.route("/create_hr", methods=["GET", "POST"])
def create_hr():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hrs = load_csv(HR_CSV)
        if any(hr["username"] == username for hr in hrs):
            error = "HR username already exists"
            return render_template("create_hr.html", error=error)
        hrs.append({"username": username, "password": password})
        save_csv(HR_CSV, ["username", "password"], hrs)
        return redirect(url_for("hr_login"))
    return render_template("create_hr.html", error=error)
@app.route("/hr_login", methods=["GET", "POST"])
def hr_login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hrs = load_csv(HR_CSV)
        hr = next((h for h in hrs if h["username"] == username and h["password"] == password), None)
        if hr:
            session["hr"] = username
            return redirect(url_for("hr_dashboard"))
        else:
            error = "Invalid HR Credentials"
    return render_template("hr_login.html", error=error)
@app.route("/hr_dashboard")
def hr_dashboard():
    if "hr" not in session:
        return redirect(url_for("hr_login"))
    mood_data = load_csv(EMP_MOOD_HISTORY_CSV)
    employees = load_csv(EMPLOYEE_CSV)
    emp_dict = {e["empid"]: e["username"] for e in employees}
    full_history = {}
    alerts = {}
    for row in mood_data:
        empid = row["emp_id"]
        emotions = row["emotions"].split(",")
        tasks = suggest_tasks(emotions)
        timestamp = row["timestamp"]
        if empid not in full_history:
            full_history[empid] = {"name": emp_dict.get(empid, "Unknown"), "entries": []}
        full_history[empid]["entries"].append({
            "timestamp": timestamp,
            "emotions": ", ".join(emotions),
            "tasks": tasks
        })
        if any(e in ["sad", "anger", "stress", "disappointment"] for e in emotions):
            alerts[empid] = True
    return render_template("hr_dashboard.html", history=full_history, alerts=alerts)
@app.route("/hr_graph.png")
def hr_graph():
    plt.figure(figsize=(8, 4))
    mood_data = load_csv(EMP_MOOD_HISTORY_CSV)
    employees = load_csv(EMPLOYEE_CSV)
    emp_dict = {e["empid"]: e["username"] for e in employees}
    for empid in emp_dict:
        emp_moods = []
        for row in mood_data:
            if row["emp_id"] == empid:
                count = row["emotions"].count("sad") + row["emotions"].count("stress") + row["emotions"].count("anger")
                emp_moods.append(count)
        if emp_moods:
            plt.plot(range(len(emp_moods)), emp_moods, marker="o", label=emp_dict[empid])
    plt.title("Employee Negative Mood Trend")
    plt.xlabel("Entries")
    plt.ylabel("Negative Mood Count")
    plt.legend()
    plt.tight_layout()
    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()
    return send_file(img, mimetype="image/png")
if __name__ == "__main__":
    app.run(debug=True)
