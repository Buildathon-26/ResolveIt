# Community Complaint Prioritizer

## Overview

Community Complaint Prioritizer is a web application developed to help communities report and prioritize local issues more effectively. Instead of complaints getting buried in long lists, the platform ranks them based on community voting and how recently they were reported, helping important issues receive attention sooner.

The project was built as a lightweight prototype for a hackathon under the theme **Open Innovation**. It does not require a database and stores data locally using a JSON file, making it simple to set up and demonstrate.

---

## Problem Statement

In many communities, people report issues such as broken streetlights, potholes, garbage accumulation, or water leakage, but there is often no easy way to identify which problems should be addressed first.

Our solution allows citizens to:
- Report issues.
- Support existing complaints by voting.
- Automatically prioritize complaints based on urgency.
- View community statistics in one place.

---

## Features

### User Login
- Simple username-based login.
- Session management using Flask.
- Login required before accessing the application.

### Complaint Submission
Users can:
- Add a complaint title.
- Select a category.
- Upload an image as proof (optional).

Each complaint stores:
- Complaint ID
- Title
- Category
- Author
- Date and time created
- Vote count
- Resolution status

---

### Community Voting

Users can vote for complaints they believe are important.

Every vote is recorded along with its timestamp.

---

### Smart Urgency Score

Instead of showing complaints only by vote count, the application calculates an urgency score using:

Urgency Score = Votes ÷ Age of Complaint

This ensures that:
- Highly voted recent complaints receive higher priority.
- Older complaints gradually move down unless they continue receiving community support.

---

### Trending Complaints

A complaint is automatically marked as **Trending** if it receives three or more votes within one hour.

This helps identify issues that suddenly become important.

---

### Complaint Prioritization

All complaints are automatically sorted according to their urgency score before being displayed.

The most urgent issues always appear at the top.

---

### Photo Upload

Users can attach an image while reporting an issue.

Images are stored locally inside the project and displayed with the complaint.

---

### Mark as Resolved

Complaints can be marked as resolved once the issue has been addressed.

This keeps the complaint list updated.

---

### Analytics Dashboard

The application provides basic analytics, including:

- Total complaints
- Open complaints
- Resolved complaints
- Category-wise complaint distribution

These statistics give a quick overview of community issues.

---

### Local Data Storage

Instead of using a database, all complaint data is stored in a JSON file.

This keeps the project lightweight and easy to run without additional setup.

---

## Technology Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask

### Data Storage
- JSON

---

## Project Structure

```
CommunityComplaintPrioritizer/
│
├── app.py
├── complaints.json
├── templates/
│   ├── index.html
│   └── login.html
│
├── static/
│   ├── style.css
│   ├── script.js
│   └── uploads/
│
└── README.md
```

---

## How to Run

1. Clone the repository.

```
git clone <repository-url>
```

2. Open the project folder.

3. Install Flask.

```
pip install flask
```

4. Run the application.

```
python app.py
```

5. Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## Future Improvements

Some ideas that could be added in future versions include:

- Location-based complaint mapping
- Admin dashboard
- Email or SMS notifications
- Duplicate complaint detection
- AI-based complaint categorization
- User reputation system
- Government department integration

---

## Team

Developed as a hackathon project under the theme **Open Innovation**.

Our aim was to create a simple, practical solution that encourages community participation and helps bring attention to issues that matter the most.
