from functools import wraps
from flask import abort, redirect, url_for
from flask_login import current_user
from datetime import datetime, date, timedelta
from models import TimetableEntry, LeaveRequest, ReplacementAssignment, Teacher

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return role_required('admin')(f)

def teacher_required(f):
    return role_required('teacher')(f)

def get_day_name(day_num):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    return days[day_num] if 0 <= day_num < len(days) else ''

def get_affected_classes(teacher_id, start_date, end_date):
    """Get all timetable entries affected by a teacher's leave"""
    affected_entries = []
    current_date = start_date
    
    while current_date <= end_date:
        day_of_week = current_date.weekday()
        if day_of_week < 6:  # Monday to Saturday
            entries = TimetableEntry.query.filter_by(
                teacher_id=teacher_id,
                day_of_week=day_of_week
            ).all()
            
            for entry in entries:
                affected_entries.append({
                    'date': current_date,
                    'entry': entry
                })
        
        current_date += timedelta(days=1)
    
    return affected_entries

def find_available_teachers(subject_id, day_of_week, start_time, end_time, exclude_date=None):
    """Find teachers available for replacement"""
    # Get all teachers who can teach this subject
    from models import SubjectAssignment
    qualified_teachers = Teacher.query.join(SubjectAssignment).filter(
        SubjectAssignment.subject_id == subject_id
    ).all()
    
    available_teachers = []
    
    for teacher in qualified_teachers:
        # Check if teacher has any conflicting timetable entries
        conflict = TimetableEntry.query.filter_by(
            teacher_id=teacher.id,
            day_of_week=day_of_week
        ).filter(
            ((TimetableEntry.start_time <= start_time) & (TimetableEntry.end_time > start_time)) |
            ((TimetableEntry.start_time < end_time) & (TimetableEntry.end_time >= end_time)) |
            ((TimetableEntry.start_time >= start_time) & (TimetableEntry.end_time <= end_time))
        ).first()
        
        if not conflict:
            # Check if teacher is on leave on that date
            if exclude_date:
                leave_conflict = LeaveRequest.query.filter_by(
                    teacher_id=teacher.id,
                    status='approved'
                ).filter(
                    (LeaveRequest.start_date <= exclude_date) & 
                    (LeaveRequest.end_date >= exclude_date)
                ).first()
                
                if not leave_conflict:
                    available_teachers.append(teacher)
            else:
                available_teachers.append(teacher)
    
    return available_teachers

def format_time(time_obj):
    """Format time object for display"""
    if time_obj:
        return time_obj.strftime('%I:%M %p')
    return ''

def get_dashboard_stats():
    """Get dashboard statistics for admin"""
    from models import Teacher, LeaveRequest, TimetableEntry
    
    total_teachers = Teacher.query.count()
    pending_leaves = LeaveRequest.query.filter_by(status='pending').count()
    
    # Get today's classes
    today = date.today()
    today_weekday = today.weekday()
    if today_weekday < 6:  # Monday to Saturday
        today_classes = TimetableEntry.query.filter_by(day_of_week=today_weekday).count()
    else:
        today_classes = 0
    
    return {
        'total_teachers': total_teachers,
        'pending_leaves': pending_leaves,
        'today_classes': today_classes
    }
