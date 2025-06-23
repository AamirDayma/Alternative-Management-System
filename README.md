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

| Login Page                           | Admin Dashboard                                     |
| ------------------------------------ | --------------------------------------------------- |
| ![login page](https://github.com/user-attachments/assets/0788d851-a3f0-40fb-902a-fe16badb192d)
 | ![admin dash](https://github.com/user-attachments/assets/a7eb993b-5f9f-4816-91e6-e70e212199cd)
 |
 
| Add Teacher                                 | Class & Subject Management                         |
| ------------------------------------------- | -------------------------------------------------- |
| ![Add Teacher](screenshots/add_teacher.png) | ![Class Management](screenshots/class_subject.png) |




![add teach](https://github.com/user-attachments/assets/ecbbf72a-8ac8-4bc9-bee6-9c82a1a857ac)

![Class And Subject manage](https://github.com/user-attachments/assets/a5440824-3c60-4ad3-a181-b3bdd2107ffd)

![leave req](https://github.com/user-attachments/assets/5b1798da-3142-4f36-aff4-9e6ef8749375)

![replace Assign](https://github.com/user-attachments/assets/67e0d521-b3cf-4fc9-b497-d127c3b860a3)




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
