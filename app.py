from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

data = pd.read_csv("stress_data.csv")

X = data.drop("stress_level", axis=1)
y = data["stress_level"]

model = LogisticRegression(max_iter=1000)
model.fit(X, y)

stress_tips = {
    "Low": "Maintain your routine and stay positive.",
    "Medium": "Take breaks, exercise, and manage your time well.",
    "High": "Relax, reduce workload, and seek support if needed."
}

def generate_reason(sleep, work, screen, pressure, mood):
    reasons = []

    if sleep < 6:
        reasons.append("low sleep duration")
    if work > 8:
        reasons.append("high work or study load")
    if screen > 6:
        reasons.append("excessive screen time")
    if pressure >= 4:
        reasons.append("high pressure levels")
    if mood <= 2:
        reasons.append("low emotional well-being")

    if reasons:
        return "Stress may be caused due to " + ", ".join(reasons) + "."
    else:
        return "Your lifestyle indicators are well balanced."
    
def generate_suggestions(sleep, work, screen, pressure, mood):
    suggestions = []

    if sleep < 6:
        suggestions.append("Try to get at least 7–8 hours of sleep daily.")
    if work > 8:
        suggestions.append("Consider reducing workload and taking short breaks.")
    if screen > 6:
        suggestions.append("Limit screen time, especially before bedtime.")
    if pressure >= 4:
        suggestions.append("Practice relaxation techniques like meditation or deep breathing.")
    if mood <= 2:
        suggestions.append("Engage in activities you enjoy and talk to someone you trust.")

    if not suggestions:
        suggestions.append("Maintain your healthy lifestyle and positive habits.")

    return suggestions

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    tip = ""
    reason = ""
    suggestions = []

    if request.method == "POST":
        sleep = int(request.form["sleep"])
        work = int(request.form["work"])
        screen = int(request.form["screen"])
        pressure = int(request.form["pressure"])
        mood = int(request.form["mood"])

        
        input_data = pd.DataFrame([{
            "sleep_hours": sleep,
            "work_hours": work,
            "screen_time": screen,
            "pressure_level": pressure,
            "mood": mood
        }])

        result = model.predict(input_data)[0]
        tip = stress_tips[result]
        reason = generate_reason(sleep, work, screen, pressure, mood)
        suggestions = generate_suggestions(sleep, work, screen, pressure, mood)

    return render_template("index.html", result=result, tip=tip, reason=reason,suggestions=suggestions)

if __name__ == "__main__":
    app.run()
