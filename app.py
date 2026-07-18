from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
import json, os
from difflib import SequenceMatcher

app = Flask(__name__)
app.secret_key = "supersecret"

FILE = "complaints.json"
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def load_data():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def urgency_score(item):
    created = datetime.fromisoformat(item["created_at"])
    age_hours = (datetime.now() - created).total_seconds() / 3600
    age_hours = max(age_hours, 1)
    return round(item["votes"] / age_hours, 2)

@app.route("/")
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", username=session["username"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            session["username"] = username
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/get_complaints")
def get_complaints():
    data = load_data()
    one_hour_ago = datetime.now() - timedelta(hours=1)

    for item in data:
        item["urgency"] = urgency_score(item)
        recent_votes = sum(1 for v in item["vote_times"] if datetime.fromisoformat(v) > one_hour_ago)
        item["trending"] = recent_votes >= 3

    data.sort(key=lambda x: x["urgency"], reverse=True)
    return jsonify(data)

@app.route("/add_complaint", methods=["POST"])
def add_complaint():
    if "username" not in session:
        return jsonify({"error": "Login required"}), 403

    title = request.form.get("title")
    category = request.form.get("category")
    photo = request.files.get("photo")

    data = load_data()


    # Check for duplicate complaints
    for item in data:
        similarity = SequenceMatcher(
            None,
            item["title"].lower(),
            title.lower()
        ).ratio()

        if similarity >= 0.8 and item["category"].lower() == category.lower():
            item["votes"] += 1
            item["vote_times"].append(datetime.now().isoformat())
            save_data(data)

            return jsonify({
                "success": True,
                "duplicate": True,
                "message": "Complaint already exists. Your vote has been added."
            })

    complaint = {
        "id": len(data) + 1,
        "title": title,
        "category": category,
        "author": session["username"],
        "votes": 0,
        "created_at": datetime.now().isoformat(),
        "vote_times": [],
        "resolved": False,
        "photo": None
    }

    if photo:
        filename = f"{complaint['id']}_{photo.filename}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        photo.save(filepath)
        complaint["photo"] = f"/static/uploads/{filename}"

    data.append(complaint)
    save_data(data)
    return jsonify({"success": True})

@app.route("/vote/<int:id>", methods=["POST"])
def vote(id):
    if "username" not in session:
        return jsonify({"error": "Login required"}), 403

    data = load_data()
    for item in data:
        if item["id"] == id:
            item["votes"] += 1
            item["vote_times"].append(datetime.now().isoformat())
    save_data(data)
    return jsonify({"success": True})

@app.route("/resolve/<int:id>", methods=["POST"])
def resolve(id):
    data = load_data()
    for item in data:
        if item["id"] == id:
            item["resolved"] = True
    save_data(data)
    return jsonify({"success": True})

@app.route("/analytics")
def analytics():
    data = load_data()
    total = len(data)
    resolved = sum(1 for d in data if d["resolved"])
    open_count = total - resolved

    categories = {}
    for d in data:
        categories[d["category"]] = categories.get(d["category"], 0) + 1

    return jsonify({
        "total": total,
        "resolved": resolved,
        "open": open_count,
        "categories": categories
    })

@app.route("/search")
def search():
    query = request.args.get("q", "").strip().lower()

    data = load_data()

    results = []

    for item in data:
        if (
            query in item["title"].lower()
            or query in item["category"].lower()
        ):
            item["urgency"] = urgency_score(item)
            results.append(item)

    results.sort(key=lambda x: x["urgency"], reverse=True)

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)