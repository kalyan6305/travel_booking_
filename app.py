from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = "supersecretkey"

# MongoDB connection (local)
app.config["MONGO_URI"] = "mongodb://localhost:27017/travelDB"
mongo = PyMongo(app)

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
        return render_template("index.html")
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

        mongo.db.contacts.insert_one({
            "name": name,
            "email": email,
            "message": message
        })

        flash("✅ Your message has been sent successfully!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")

# Register (Signup)
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = mongo.db.users.find_one({"username": username})
        if existing_user:
            flash("⚠️ Username already exists. Try another.", "danger")
            return redirect(url_for("signup"))

        mongo.db.users.insert_one({
            "username": username,
            "password": password
        })

        flash("✅ Registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("sinup.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = mongo.db.users.find_one({"username": username, "password": password})

        if user:
            session["user"] = username
            flash(f"✅ Welcome {username}, you are now logged in.", "success")
            return redirect(url_for("home"))
        else:
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
