
# 🛡️ CyberIncidentShield

**A Django-based web dashboard for managing cybersecurity incident response, tracking detailed step-by-step handling procedures, and providing progress visibility.**

---

## 📌 Elevator Pitch

CyberIncidentShield empowers incident responders and administrators with a structured and intuitive dashboard to track cybersecurity incidents from detection to resolution using international best practices like ISO/IEC 27035.

---
 

### 🛠️ How It Was Built
- **Framework**: Django
- **Frontend**: HTML, Bootstrap (optional), CSS (native)
- **Backend**: Python
- **Database**: SQLite (for demo purposes)
- **Design Pattern**: MVC (Model-View-Controller)

---

## 💻 How to Run This Project Locally

Follow the steps below to set up **CyberIncidentShield** on your local machine:

### ✅ Prerequisites

Make sure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- Virtual environment (Venv) 

---

### 📦 Step-by-Step Setup

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/CyberIncidentShield.git
cd CyberIncidentShield

2.Create and Activate a Virtual Environment

# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

3.Install Dependencies

pip install -r requirements.txt

*If requirements.txt is not available, install Django manually:

pip install django

4.Run Database Migrations

python manage.py migrate
python manage.py makemigrations

5.Create a Superuser (Admin Login)

python manage.py createsuperuser

6.run the program

python manage.py runserver

Access the Application
App URL: http://127.0.0.1:8000/
