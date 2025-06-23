from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, DateField, TimeField, IntegerField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional
from models import User, Teacher, Class, Subject
from datetime import date

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    role = SelectField('Role', choices=[('teacher', 'Teacher'), ('admin', 'Admin')], default='teacher')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please choose a different one.')

class TeacherForm(FlaskForm):
    employee_id = StringField('Employee ID', validators=[DataRequired(), Length(max=20)])
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    department = StringField('Department', validators=[Optional(), Length(max=100)])
    qualification = StringField('Qualification', validators=[Optional(), Length(max=200)])
    experience_years = IntegerField('Years of Experience', validators=[Optional()])
    joining_date = DateField('Joining Date', validators=[Optional()], default=date.today)

class ClassForm(FlaskForm):
    name = StringField('Class Name', validators=[DataRequired(), Length(max=50)])
    grade = StringField('Grade', validators=[DataRequired(), Length(max=10)])
    section = StringField('Section', validators=[DataRequired(), Length(max=10)])
    total_students = IntegerField('Total Students', validators=[Optional()])
    room_number = StringField('Room Number', validators=[Optional(), Length(max=20)])

class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired(), Length(max=100)])
    code = StringField('Subject Code', validators=[DataRequired(), Length(max=20)])
    description = TextAreaField('Description', validators=[Optional()])

class TimetableEntryForm(FlaskForm):
    class_id = SelectField('Class', coerce=int, validators=[DataRequired()])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])
    teacher_id = SelectField('Teacher', coerce=int, validators=[DataRequired()])
    day_of_week = SelectField('Day', choices=[
        (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), 
        (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday')
    ], coerce=int, validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    room_number = StringField('Room Number', validators=[Optional(), Length(max=20)])
    
    def __init__(self, *args, **kwargs):
        super(TimetableEntryForm, self).__init__(*args, **kwargs)
        self.class_id.choices = [(c.id, c.name) for c in Class.query.all()]
        self.subject_id.choices = [(s.id, s.name) for s in Subject.query.all()]
        self.teacher_id.choices = [(t.id, t.user.name) for t in Teacher.query.all()]

class LeaveRequestForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    start_time = TimeField('Start Time (optional for partial day)', validators=[Optional()])
    end_time = TimeField('End Time (optional for partial day)', validators=[Optional()])
    reason = TextAreaField('Reason', validators=[DataRequired(), Length(min=10, max=500)])
    
    def validate_end_date(self, end_date):
        if end_date.data < self.start_date.data:
            raise ValidationError('End date must be after start date.')

class LeaveApprovalForm(FlaskForm):
    status = SelectField('Status', choices=[('approved', 'Approve'), ('rejected', 'Reject')], validators=[DataRequired()])
    admin_comments = TextAreaField('Comments', validators=[Optional(), Length(max=500)])

class ReplacementAssignmentForm(FlaskForm):
    replacement_teacher_id = SelectField('Replacement Teacher', coerce=int, validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        super(ReplacementAssignmentForm, self).__init__(*args, **kwargs)
        self.replacement_teacher_id.choices = [(t.id, t.user.name) for t in Teacher.query.all()]
