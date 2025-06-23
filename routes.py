from flask import render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db
from models import User, Teacher, Class, Subject, TimetableEntry, LeaveRequest, ReplacementAssignment, SubjectAssignment
from forms import (LoginForm, RegisterForm, TeacherForm, ClassForm, SubjectForm, 
                  TimetableEntryForm, LeaveRequestForm, LeaveApprovalForm, ReplacementAssignmentForm)
from utils import admin_required, teacher_required, get_day_name, get_affected_classes, find_available_teachers, get_dashboard_stats
from datetime import datetime, date

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.role == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        else:
            return redirect(url_for('student_timetable'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Logged in successfully!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Invalid username or password!', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
@admin_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            name=form.name.data,
            phone=form.phone.data,
            role=form.role.data
        )
        db.session.add(user)
        db.session.commit()
        
        # Create teacher profile if role is teacher
        if form.role.data == 'teacher':
            teacher = Teacher(
                user_id=user.id,
                employee_id=f'EMP{user.id:04d}',
                department='',
                qualification='',
                experience_years=0
            )
            db.session.add(teacher)
            db.session.commit()
        
        flash('User registered successfully!', 'success')
        return redirect(url_for('admin_teachers'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name', current_user.name)
        current_user.email = request.form.get('email', current_user.email)
        current_user.phone = request.form.get('phone', current_user.phone)
        
        if current_user.role == 'teacher' and current_user.teacher_profile:
            teacher = current_user.teacher_profile
            teacher.department = request.form.get('department', teacher.department)
            teacher.qualification = request.form.get('qualification', teacher.qualification)
            teacher.experience_years = int(request.form.get('experience_years', teacher.experience_years) or 0)
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html')

# Admin Routes
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    stats = get_dashboard_stats()
    recent_leaves = LeaveRequest.query.filter_by(status='pending').order_by(LeaveRequest.applied_date.desc()).limit(5).all()
    return render_template('admin/dashboard.html', stats=stats, recent_leaves=recent_leaves)

@app.route('/admin/teachers')
@admin_required
def admin_teachers():
    teachers = Teacher.query.join(User).all()
    return render_template('admin/teachers.html', teachers=teachers)

@app.route('/admin/teachers/add', methods=['GET', 'POST'])
@admin_required
def admin_add_teacher():
    form = TeacherForm()
    if form.validate_on_submit():
        # Create user account
        user = User(
            username=form.employee_id.data.lower(),
            email=form.email.data,
            password_hash=generate_password_hash('password123'),  # Default password
            name=form.name.data,
            phone=form.phone.data,
            role='teacher'
        )
        db.session.add(user)
        db.session.flush()
        
        # Create teacher profile
        teacher = Teacher(
            user_id=user.id,
            employee_id=form.employee_id.data,
            department=form.department.data,
            qualification=form.qualification.data,
            experience_years=form.experience_years.data or 0,
            joining_date=form.joining_date.data or date.today()
        )
        db.session.add(teacher)
        db.session.commit()
        
        flash(f'Teacher added successfully! Default password: password123', 'success')
        return redirect(url_for('admin_teachers'))
    
    return render_template('admin/teachers.html', form=form, action='add')

@app.route('/admin/teachers/edit/<int:teacher_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    form = TeacherForm(obj=teacher)
    
    if form.validate_on_submit():
        teacher.employee_id = form.employee_id.data
        teacher.user.name = form.name.data
        teacher.user.email = form.email.data
        teacher.user.phone = form.phone.data
        teacher.department = form.department.data
        teacher.qualification = form.qualification.data
        teacher.experience_years = form.experience_years.data or 0
        teacher.joining_date = form.joining_date.data or teacher.joining_date
        
        db.session.commit()
        flash('Teacher updated successfully!', 'success')
        return redirect(url_for('admin_teachers'))
    
    # Pre-fill form with current data
    form.name.data = teacher.user.name
    form.email.data = teacher.user.email
    form.phone.data = teacher.user.phone
    
    return render_template('admin/teachers.html', form=form, teacher=teacher, action='edit')

@app.route('/admin/teachers/delete/<int:teacher_id>', methods=['POST'])
@admin_required
def admin_delete_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    user = teacher.user
    
    db.session.delete(teacher)
    db.session.delete(user)
    db.session.commit()
    
    flash('Teacher deleted successfully!', 'success')
    return redirect(url_for('admin_teachers'))

@app.route('/admin/classes')
@admin_required
def admin_classes():
    classes = Class.query.all()
    subjects = Subject.query.all()
    return render_template('admin/classes.html', classes=classes, subjects=subjects)

@app.route('/admin/classes/add', methods=['POST'])
@admin_required
def admin_add_class():
    form = ClassForm()
    if form.validate_on_submit():
        class_obj = Class(
            name=form.name.data,
            grade=form.grade.data,
            section=form.section.data,
            total_students=form.total_students.data or 0,
            room_number=form.room_number.data
        )
        db.session.add(class_obj)
        db.session.commit()
        flash('Class added successfully!', 'success')
    return redirect(url_for('admin_classes'))

@app.route('/admin/subjects/add', methods=['POST'])
@admin_required
def admin_add_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(
            name=form.name.data,
            code=form.code.data,
            description=form.description.data
        )
        db.session.add(subject)
        db.session.commit()
        flash('Subject added successfully!', 'success')
    return redirect(url_for('admin_classes'))

@app.route('/admin/timetable')
@admin_required
def admin_timetable():
    timetable_entries = TimetableEntry.query.all()
    form = TimetableEntryForm()
    return render_template('admin/timetable.html', entries=timetable_entries, form=form)

@app.route('/admin/timetable/add', methods=['POST'])
@admin_required
def admin_add_timetable():
    form = TimetableEntryForm()
    if form.validate_on_submit():
        entry = TimetableEntry(
            class_id=form.class_id.data,
            subject_id=form.subject_id.data,
            teacher_id=form.teacher_id.data,
            day_of_week=form.day_of_week.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            room_number=form.room_number.data
        )
        db.session.add(entry)
        db.session.commit()
        flash('Timetable entry added successfully!', 'success')
    return redirect(url_for('admin_timetable'))

@app.route('/admin/leaves')
@admin_required
def admin_leaves():
    leaves = LeaveRequest.query.order_by(LeaveRequest.applied_date.desc()).all()
    return render_template('admin/leaves.html', leaves=leaves)

@app.route('/admin/leaves/<int:leave_id>/approve', methods=['POST'])
@admin_required
def admin_approve_leave(leave_id):
    leave_request = LeaveRequest.query.get_or_404(leave_id)
    form = LeaveApprovalForm()
    
    if form.validate_on_submit():
        leave_request.status = form.status.data
        leave_request.admin_comments = form.admin_comments.data
        leave_request.approved_by = current_user.id
        leave_request.approved_date = datetime.utcnow()
        
        # If approved, create replacement assignments
        if form.status.data == 'approved':
            affected_classes = get_affected_classes(
                leave_request.teacher_id,
                leave_request.start_date,
                leave_request.end_date
            )
            
            for affected in affected_classes:
                replacement = ReplacementAssignment(
                    leave_request_id=leave_request.id,
                    original_teacher_id=leave_request.teacher_id,
                    timetable_entry_id=affected['entry'].id,
                    replacement_date=affected['date'],
                    assigned_by=current_user.id
                )
                db.session.add(replacement)
        
        db.session.commit()
        flash(f'Leave request {form.status.data} successfully!', 'success')
    
    return redirect(url_for('admin_leaves'))

@app.route('/admin/replacements')
@admin_required
def admin_replacements():
    replacements = ReplacementAssignment.query.filter_by(replacement_teacher_id=None).all()
    return render_template('admin/replacements.html', replacements=replacements)

@app.route('/admin/replacements/<int:replacement_id>/assign', methods=['POST'])
@admin_required
def admin_assign_replacement(replacement_id):
    replacement = ReplacementAssignment.query.get_or_404(replacement_id)
    form = ReplacementAssignmentForm()
    
    if form.validate_on_submit():
        replacement.replacement_teacher_id = form.replacement_teacher_id.data
        replacement.status = 'pending'
        db.session.commit()
        flash('Replacement teacher assigned successfully!', 'success')
    
    return redirect(url_for('admin_replacements'))

# Teacher Routes
@app.route('/teacher/dashboard')
@teacher_required
def teacher_dashboard():
    teacher = current_user.teacher_profile
    if not teacher:
        flash('Teacher profile not found!', 'danger')
        return redirect(url_for('logout'))
    
    # Get today's schedule
    today = date.today()
    today_weekday = today.weekday()
    today_schedule = []
    if today_weekday < 6:  # Monday to Saturday
        today_schedule = TimetableEntry.query.filter_by(
            teacher_id=teacher.id,
            day_of_week=today_weekday
        ).order_by(TimetableEntry.start_time).all()
    
    # Get pending replacement requests
    pending_replacements = ReplacementAssignment.query.filter_by(
        replacement_teacher_id=teacher.id,
        status='pending'
    ).all()
    
    return render_template('teacher/dashboard.html', 
                         today_schedule=today_schedule,
                         pending_replacements=pending_replacements)

@app.route('/teacher/timetable')
@teacher_required
def teacher_timetable():
    teacher = current_user.teacher_profile
    timetable = TimetableEntry.query.filter_by(teacher_id=teacher.id).all()
    
    # Organize by day
    schedule = {i: [] for i in range(6)}  # Monday to Saturday
    for entry in timetable:
        schedule[entry.day_of_week].append(entry)
    
    return render_template('teacher/timetable.html', schedule=schedule)

@app.route('/teacher/leave/apply', methods=['GET', 'POST'])
@teacher_required
def teacher_apply_leave():
    form = LeaveRequestForm()
    if form.validate_on_submit():
        leave_request = LeaveRequest(
            teacher_id=current_user.teacher_profile.id,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            reason=form.reason.data
        )
        db.session.add(leave_request)
        db.session.commit()
        flash('Leave request submitted successfully!', 'success')
        return redirect(url_for('teacher_my_leaves'))
    
    return render_template('teacher/leave_apply.html', form=form)

@app.route('/teacher/leaves')
@teacher_required
def teacher_my_leaves():
    teacher = current_user.teacher_profile
    leaves = LeaveRequest.query.filter_by(teacher_id=teacher.id).order_by(LeaveRequest.applied_date.desc()).all()
    return render_template('teacher/my_leaves.html', leaves=leaves)

@app.route('/teacher/replacements')
@teacher_required
def teacher_replacements():
    teacher = current_user.teacher_profile
    replacements = ReplacementAssignment.query.filter_by(replacement_teacher_id=teacher.id).all()
    return render_template('teacher/replacements.html', replacements=replacements)

@app.route('/teacher/replacements/<int:replacement_id>/respond', methods=['POST'])
@teacher_required
def teacher_respond_replacement(replacement_id):
    replacement = ReplacementAssignment.query.get_or_404(replacement_id)
    
    if replacement.replacement_teacher_id != current_user.teacher_profile.id:
        abort(403)
    
    response = request.form.get('response')
    if response in ['accepted', 'rejected']:
        replacement.status = response
        replacement.response_date = datetime.utcnow()
        db.session.commit()
        flash(f'Replacement request {response} successfully!', 'success')
    
    return redirect(url_for('teacher_replacements'))

# Student Routes
@app.route('/student/timetable')
def student_timetable():
    classes = Class.query.all()
    selected_class_id = request.args.get('class_id', type=int)
    
    schedule = {i: [] for i in range(6)}  # Monday to Saturday
    
    if selected_class_id:
        timetable = TimetableEntry.query.filter_by(class_id=selected_class_id).all()
        for entry in timetable:
            schedule[entry.day_of_week].append(entry)
    
    return render_template('student/timetable.html', 
                         classes=classes, 
                         schedule=schedule, 
                         selected_class_id=selected_class_id)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

# Template filters
@app.template_filter('day_name')
def day_name_filter(day_num):
    return get_day_name(day_num)

@app.template_filter('time_format')
def time_format_filter(time_obj):
    if time_obj:
        return time_obj.strftime('%I:%M %p')
    return ''
