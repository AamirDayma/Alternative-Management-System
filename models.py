from app import db
from flask_login import UserMixin
from datetime import datetime, date, time
from sqlalchemy import func

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='teacher')  # admin, teacher, student
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship for teachers
    teacher_profile = db.relationship('Teacher', backref='user', uselist=False, cascade='all, delete-orphan')

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    department = db.Column(db.String(100))
    qualification = db.Column(db.String(200))
    experience_years = db.Column(db.Integer, default=0)
    joining_date = db.Column(db.Date, default=date.today)
    
    # Relationships
    subject_assignments = db.relationship('SubjectAssignment', backref='teacher', cascade='all, delete-orphan')
    leave_requests = db.relationship('LeaveRequest', backref='teacher', cascade='all, delete-orphan')
    replacement_assignments = db.relationship('ReplacementAssignment', 
                                            foreign_keys='ReplacementAssignment.replacement_teacher_id',
                                            backref='replacement_teacher')

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # e.g., "Grade 10A"
    grade = db.Column(db.String(10), nullable=False)  # e.g., "10"
    section = db.Column(db.String(10), nullable=False)  # e.g., "A"
    total_students = db.Column(db.Integer, default=0)
    room_number = db.Column(db.String(20))
    
    # Relationships
    timetable_entries = db.relationship('TimetableEntry', backref='class_ref', cascade='all, delete-orphan')

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    # Relationships
    assignments = db.relationship('SubjectAssignment', backref='subject', cascade='all, delete-orphan')
    timetable_entries = db.relationship('TimetableEntry', backref='subject', cascade='all, delete-orphan')

class SubjectAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    assigned_date = db.Column(db.Date, default=date.today)
    
    # Relationship
    class_ref = db.relationship('Class', backref='subject_assignments')

class TimetableEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Monday, 1=Tuesday, ..., 5=Saturday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    room_number = db.Column(db.String(20))
    
    # Relationship
    teacher = db.relationship('Teacher', backref='timetable_entries')

class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time)  # Optional for partial day leaves
    end_time = db.Column(db.Time)    # Optional for partial day leaves
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    approved_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    approved_date = db.Column(db.DateTime)
    admin_comments = db.Column(db.Text)
    
    # Relationships
    approver = db.relationship('User', foreign_keys=[approved_by])
    replacement_assignments = db.relationship('ReplacementAssignment', backref='leave_request', cascade='all, delete-orphan')

class ReplacementAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    leave_request_id = db.Column(db.Integer, db.ForeignKey('leave_request.id'), nullable=False)
    original_teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)
    replacement_teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    timetable_entry_id = db.Column(db.Integer, db.ForeignKey('timetable_entry.id'), nullable=False)
    replacement_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    assigned_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_date = db.Column(db.DateTime, default=datetime.utcnow)
    response_date = db.Column(db.DateTime)
    
    # Relationships
    original_teacher = db.relationship('Teacher', foreign_keys=[original_teacher_id])
    timetable_entry = db.relationship('TimetableEntry', backref='replacement_assignments')
    assigner = db.relationship('User', foreign_keys=[assigned_by])
