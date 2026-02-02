import csv
import os
from datetime import datetime

# Emotion Keywords
EMOTION_KEYWORDS = {
    "anger": ["angry", "anger", "furious", "mad", "punch", "rage"],
    "sad": ["sad", "cry", "crying", "lonely", "down"],
    "disappointment": ["disappointed", "missed", "failed"],
    "embarrassed": ["embarrassed", "embarrassing", "ashamed"],
    "stress": ["stressed", "overwhelmed", "burnout", "tired"],
    "joy": ["happy", "joy", "excited", "great", "awesome"]
}

# Task Suggestions
TASK_RECOMMENDATIONS = {
    "anger": [
        "Take a short break",
        "Do deep breathing",
        "Avoid critical meetings"
    ],
    "sad": [
        "Talk to a teammate",
        "Do light tasks",
        "Take a short walk"
    ],
    "stress": [
        "Prioritize tasks",
        "Take a break",
        "Avoid multitasking"
    ],
    "disappointment": [
        "Review what went wrong calmly",
        "Plan next steps",
        "Seek guidance"
    ],
    "embarrassed": [
        "Take time to reflect",
        "Avoid public discussions",
        "Focus on solo work"
    ],
    "joy": [
        "Work on creative tasks",
        "Take on challenging work",
        "Collaborate with team"
    ],
    "neutral": [
        "Continue regular tasks",
        "Review pending work"
    ]
}
CSV_FILE = "mood_history.csv"

# Detect emotions
def detect_emotions(text):
    text = text.lower()
    detected = []
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for word in keywords:
            if word in text:
                detected.append(emotion)
                break
    if not detected:
        detected.append("neutral")
    return detected

# Suggest tasks
def suggest_tasks(emotions):
    suggested = set()
    for emotion in emotions:
        tasks = TASK_RECOMMENDATIONS.get(emotion, [])
        for task in tasks:
            suggested.add(task)
    return list(suggested)

# Save mood history
def save_to_csv(timestamp, sentence, emotions):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "sentence", "emotions"])
        writer.writerow([
            timestamp,
            sentence,
            ",".join(emotions)
        ])

# Stress Alert System
def stress_alert():
    if not os.path.exists(CSV_FILE):
        return
    with open(CSV_FILE, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
    if len(rows) <= 1:
        return
    recent_rows = rows[1:][-5:]
    negative_count = 0
    for row in recent_rows:
        if len(row) < 3:
            continue
        emotions = row[2].split(",")
        if any(e in ["sad", "anger", "stress", "disappointment"] for e in emotions):
            negative_count += 1
    if negative_count >= 3:
        print("\n⚠️ STRESS ALERT")
        print("➡ HR / Manager should be notified\n")

# Main Program
def main():
    print("=== Emotion Detection System ===")
    print("Type 'exit' to quit\n")
    while True:
        sentence = input("Enter a sentence to analyze emotions:\n").strip()
        if sentence.lower() == "exit":
            print("Exiting system, Have a great day😊.")
            break

        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
        emotions = detect_emotions(sentence)
        tasks = suggest_tasks(emotions)
        save_to_csv(timestamp, sentence, emotions)
        print("\nPredicted Emotions:")
        print("- " + ", ".join(emotions))
        print("\nSuggested Tasks:")
        for task in tasks:
            print("- " + task)

        stress_alert()

        print("\n" + "=" * 50 + "\n")
if __name__ == "__main__":
    main()
