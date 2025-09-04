**webiste link: https://travel-booking-8sor.onrender.com**
```markdown
# 🌍 Travel Booking Portal

A simple **Flask-based Travel Booking Website** with user authentication (login/signup), contact form, and basic travel service links (train, bus, car, flight).  

This project uses **Flask + JSON storage** (no database required) and can be deployed easily on **Render/Heroku**.

---

## 🚀 Features
- 🔐 **User Authentication** (Signup, Login, Logout)
- 📩 **Contact Form** (messages stored in JSON file)
- 🏠 **Pages**:
  - Home
  - About
  - Contact
- ✈️ **Travel Services**:
  - Car booking
  - Train booking
  - Bus booking
  - Flight booking
- ⚡ Simple and lightweight (no external DB)

---

## 📂 Project Structure
```

travel-app/
│── app.py                # Main Flask application
│── requirements.txt      # Python dependencies
│── render.yaml           # Deployment config (Render)
│── users.json            # Stores registered users
│── contacts.json         # Stores contact messages
│── templates/            # HTML templates (Jinja2)
│    ├── index.html
│    ├── about.html
│    ├── contact.html
│    ├── login.html
│    ├── signup.html
│── static/               # Static files (CSS, images)
└── style.css

````

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/travel-app.git
cd travel-app
````

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # On Mac/Linux
venv\Scripts\activate       # On Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run App Locally

```bash
python app.py
```

App will be available at:
👉 [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 🌐 Deployment on Render

1. Push code to GitHub.
2. Connect repo to **Render**.
3. Use `render.yaml` (already included).
4. Render will build & deploy automatically.

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Frontend:** HTML, CSS (Jinja2 Templates)
* **Storage:** JSON files (users & contacts)
* **Deployment:** Render

---

## 👨‍💻 Author

Developed by **\[Your Name]** ✨
📧 Contact: [your-email@example.com](mailto:your-email@example.com)

```

---

Do you want me to also add **screenshots & demo usage section** in the README so it looks professional on GitHub?
```
