from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Temporary storage (No Database)
complaints = []
next_id = 1

@app.route("/")
def home():
    return render_template("index.html")


# Get all complaints
@app.route("/complaints", methods=["GET"])
def get_complaints():
    # Sort by votes (highest first)
    sorted_complaints = sorted(
        complaints,
        key=lambda x: x["votes"],
        reverse=True
    )
    return jsonify(sorted_complaints)


# Add a complaint
@app.route("/complaints", methods=["POST"])
def add_complaint():
    global next_id

    data = request.json

    complaint = {
        "id": next_id,
        "title": data["title"],
        "category": data["category"],
        "description": data["description"],
        "votes": 0
    }

    complaints.append(complaint)
    next_id += 1

    return jsonify({
        "message": "Complaint Added Successfully",
        "complaint": complaint
    })


# Upvote a complaint
@app.route("/vote/<int:complaint_id>", methods=["POST"])
def vote(complaint_id):

    for complaint in complaints:
        if complaint["id"] == complaint_id:
            complaint["votes"] += 1

            return jsonify({
                "message": "Vote Count Updated",
                "votes": complaint["votes"]
            })

    return jsonify({"message": "Complaint Not Found"}), 404


# Delete a complaint (Optional)
@app.route("/delete/<int:complaint_id>", methods=["DELETE"])
def delete_complaint(complaint_id):

    global complaints

    complaints = [
        c for c in complaints
        if c["id"] != complaint_id
    ]

    return jsonify({"message": "Complaint Deleted"})


if __name__ == "__main__":
    app.run(debug=True)