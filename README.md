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
                    

🎓 Student Access: 
                    
                    View public timetable without login


🌙 Dark Mode UI: 

                    Modern and responsive design using Bootstrap with dark theme


🗄️ Database: 

                    Integrated with PostgreSQL for efficient data management

🔐 Demo Credentials
yaml
Copy
Edit
Admin Login:
Username: admin
Password: admin123




📸 Screenshots


![login page](https://github.com/user-attachments/assets/2cb2a888-ad7a-4c20-a200-d4876ea78860)


![admin dash](https://github.com/user-attachments/assets/d988c4cd-e62f-4738-af0f-da52b95111f4)


![add teach](https://github.com/user-attachments/assets/6d24db68-d7d2-441a-94eb-acf7928f1c03)


![Class And Subject manage](https://github.com/user-attachments/assets/3ba4736c-8488-4e08-809b-ab0f2417edba)


![leave req](https://github.com/user-attachments/assets/b7c59032-a994-41ec-8b5e-d4b1d3dc1610)


![replace Assign](https://github.com/user-attachments/assets/fc2f044c-6510-4de7-aaa5-eb07e4e5d0da)



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
