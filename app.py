from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "mysecretkey"

# ====== MongoDB Connection ======
client = MongoClient("mongodb://localhost:27017/")  # Use your MongoDB Atlas URI if needed
db = client["travel_booking"]
users_collection = db["users"]
messages_collection = db["messages"]   # ✅ Added for contact messages

bcrypt = Bcrypt(app)

# ====== ROUTES ======

@app.route("/")
def index():
    """ Show login/signup page if not logged in """
    if "user" in session:
        return redirect(url_for("home"))
    return render_template("login.html")  

@app.route("/login", methods=["POST"])
def login():
    """ Login user """
    username = request.form["username"]
    password = request.form["password"]

    user = users_collection.find_one({"username": username})
    if user and bcrypt.check_password_hash(user["password"], password):
        session["user"] = username
        flash("Login successful!", "success")
        return redirect(url_for("home"))
    else:
        flash("Invalid username or password", "danger")
        return redirect(url_for("index"))

@app.route("/signup", methods=["POST"])
def signup():
    """ Register new user """
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    existing_user = users_collection.find_one({"username": username})
    if existing_user:
        flash("⚠️ Username already exists, choose another!", "warning")
        return redirect(url_for("index"))
    else:
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        users_collection.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password
        })
        flash("✅ Signup successful! Please login.", "success")
        return redirect(url_for("index"))

@app.route("/home")
def home():
    """ Main booking page """
    if "user" not in session:
        flash("⚠️ Please login first!", "danger")
        return redirect(url_for("index"))
    return render_template("index.html", username=session["user"])

@app.route("/about")
def about():
    """ About page """
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    """ Contact page with MongoDB storage """
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # ✅ Save the message in MongoDB
        messages_collection.insert_one({
            "name": name,
            "email": email,
            "message": message
        })

        flash("✅ Your message has been submitted successfully!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")

@app.route("/logout")
def logout():
    """ Logout user """
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))

# ====== MAIN ======
if __name__ == "__main__":
    app.run(debug=True)
