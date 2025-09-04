from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

USERS_FILE = "users.json"
CONTACTS_FILE = "contacts.json"

# ✅ Load data from JSON file
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

# ✅ Save data to JSON file
def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Load users & contacts from file
users = load_data(USERS_FILE)
contacts = load_data(CONTACTS_FILE)

# Default route - Show login first
@app.route("/")
def root():
    if "user" in session:
        return redirect(url_for("home"))
    return redirect(url_for("login"))

# Homepage (after login)
@app.route("/home")
def home():
    if "user" in session:
        return render_template("index.html", user=session["user"])
    else:
        flash("⚠️ Please login first!", "warning")
        return redirect(url_for("login"))

# About page
@app.route("/about")
def about():
    if "user" in session:
        return render_template("about.html")
    else:
        flash("⚠️ Please login first!", "warning")
        return redirect(url_for("login"))

# Contact page
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if "user" not in session:
        flash("⚠️ Please login first!", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        contacts.append({
            "name": name,
            "email": email,
            "message": message
        })
        save_data(CONTACTS_FILE, contacts)

        flash("✅ Your message has been sent successfully!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")

# Register (Signup)
# Register (Signup)
@app.route("/signup", methods=["GET", "POST"])
def signup():
    global users  # ensure we use the updated list
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        # Check if username already exists
        for user in users:
            if user["username"] == username:
                flash("⚠️ Username already exists. Try another.", "danger")
                return redirect(url_for("signup"))

        # Save new user
        new_user = {"username": username, "password": password}
        users.append(new_user)
        save_data(USERS_FILE, users)

        # Auto-login
        session["user"] = username
        flash(f"✅ Welcome {username}, your account has been created!", "success")
        return redirect(url_for("home"))

    return render_template("sinup.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    global users  # always check from memory list
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        # Reload users each time to ensure file changes are reflected
        users = load_data(USERS_FILE)

        for user in users:
            if user["username"] == username and user["password"] == password:
                session["user"] = username
                flash(f"✅ Welcome {username}, you are now logged in.", "success")
                return redirect(url_for("home"))

        flash("❌ Invalid username or password.", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")
# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("✅ You have been logged out.", "success")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
