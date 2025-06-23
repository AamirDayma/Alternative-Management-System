# Alternative-Management-System 

A comprehensive web application built using Flask, Bootstrap, and PostgreSQL, designed to streamline the management of teacher schedules, leave workflows, and class-subject assignments in educational institutions.

🚀 Features
✅ Authentication & Roles: Secure login system with role-based access control (Admin, Teacher, Student)

📊 Admin Dashboard:

Manage teachers

Create classes and subjects

Build and manage timetables

📝 Leave Management System:

Teachers can apply for leave

Admin can approve or reject requests

Option to assign replacement teachers

👨‍🏫 Teacher Dashboard:

View personal timetable

Apply for leave

View replacement requests

🎓 Student Access: View public timetable without login

🌙 Dark Mode UI: Modern and responsive design using Bootstrap with dark theme

🗄️ Database: Integrated with PostgreSQL for efficient data management

🔐 Demo Credentials
yaml
Copy
Edit
Admin Login:
Username: admin
Password: admin123
📸 Screenshots
![add teach](https://github.com/user-attachments/assets/8f76cfbe-4645-42ce-bdb7-64a50bb83b9f)

![admin dash](https://github.com/user-attachments/assets/d988c4cd-e62f-4738-af0f-da52b95111f4)


Ensure the above image files are placed in the screenshots/ folder in your repo.

🛠️ Tech Stack
Backend: Flask (Python)

Frontend: HTML, CSS, Bootstrap (Dark Theme)

Database: PostgreSQL

ORM: SQLAlchemy

Authentication: Flask-Login

📦 Installation
Prerequisites
Python 3.8+

PostgreSQL

Git

Steps
bash
Copy
Edit
git clone https://github.com/yourusername/teacher-scheduling-system.git
cd teacher-scheduling-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure database in config.py or .env

# Initialize DB
flask db init
flask db migrate
flask db upgrade

# Run the app
flask run
