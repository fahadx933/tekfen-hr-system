"""
مسارات الصفحة الرئيسية
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models.user import User, Department
from ..models.attendance import Attendance
from ..models.communication import Announcement, Message
from ..utils.data_protection import DataProtection
from ..utils.security import sanitize_input, hide_sensitive_data

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    """
    الصفحة الرئيسية
    """
    # الإعلانات النشطة
    announcements = Announcement.query.filter_by(is_active=True).order_by(Announcement.created_at.desc()).limit(5).all()
    
    # الرسائل غير المقروءة
    unread_messages_count = Message.query.filter_by(receiver_id=current_user.id, is_read=False).count()
    
    # آخر تسجيل حضور
    today_attendance = Attendance.query.filter_by(user_id=current_user.id).order_by(Attendance.created_at.desc()).first()
    
    # معلومات القسم
    department = None
    if current_user.department_id:
        department = Department.query.get(current_user.department_id)
    
    return render_template('main/index.html',
                          announcements=announcements,
                          unread_messages_count=unread_messages_count,
                          today_attendance=today_attendance,
                          department=department)


@main.route('/profile')
@login_required
def profile():
    """
    الملف الشخصي للمستخدم
    """
    return render_template('main/profile.html')


@main.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    """
    تحديث الملف الشخصي
    """
    if request.method == 'POST':
        # تحديث البيانات الشخصية المسموح بها فقط
        current_user.first_name = sanitize_input(request.form.get('first_name'))
        current_user.last_name = sanitize_input(request.form.get('last_name'))
        current_user.email = sanitize_input(request.form.get('email'))
        current_user.phone = sanitize_input(request.form.get('phone'))
        current_user.language = request.form.get('language', 'ar')
        
        # تحديث صورة الملف الشخصي إذا تم تحميلها
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename:
                # التحقق من نوع الملف
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
                if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                    # حفظ الصورة
                    from werkzeug.utils import secure_filename
                    import os
                    from .. import app
                    
                    filename = secure_filename(f"profile_{current_user.id}_{file.filename}")
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'profiles', filename)
                    
                    # التأكد من وجود المجلد
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    file.save(file_path)
                    current_user.profile_picture = f'/static/uploads/profiles/{filename}'
        
        db.session.commit()
        
        # تسجيل العملية
        from ..models.communication import Log
        log = Log(
            user_id=current_user.id,
            action='تحديث الملف الشخصي',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(log)
        db.session.commit()
        
        flash('تم تحديث الملف الشخصي بنجاح', 'success')
        return redirect(url_for('main.profile'))


@main.route('/company-history')
@login_required
def company_history():
    """
    تاريخ الشركة
    """
    return render_template('main/company_history.html')


@main.route('/contact-directory')
@login_required
def contact_directory():
    """
    دليل الاتصال بالموظفين
    """
    # الحصول على قائمة الموظفين حسب صلاحيات المستخدم الحالي
    users = User.query.filter_by(is_active=True).all()
    
    # تصفية القائمة حسب دور المستخدم الحالي
    role_name = current_user.role.name if current_user.role else 'employee'
    department_id = current_user.department_id
    
    filtered_users = DataProtection.filter_users_list(users, role_name, department_id)
    
    # تنظيم المستخدمين حسب القسم
    users_by_department = {}
    for user in filtered_users:
        dept_id = user.department_id or 0
        if dept_id not in users_by_department:
            dept_name = user.department.name if user.department else 'بدون قسم'
            users_by_department[dept_id] = {'name': dept_name, 'users': []}
        
        # إخفاء البيانات الحساسة
        user_data = {
            'id': user.id,
            'name': user.get_full_name(),
            'position': user.position,
            'email': user.email,
            'phone': user.phone
        }
        
        users_by_department[dept_id]['users'].append(user_data)
    
    return render_template('main/contact_directory.html',
                          users_by_department=users_by_department)


@main.route('/help')
@login_required
def help():
    """
    صفحة المساعدة
    """
    return render_template('main/help.html')


@main.route('/api/user-info')
@login_required
def user_info_api():
    """
    واجهة برمجية للحصول على معلومات المستخدم الحالي
    """
    user_data = {
        'id': current_user.id,
        'username': current_user.username,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'email': current_user.email,
        'role': current_user.role.name if current_user.role else None,
        'department': current_user.department.name if current_user.department else None,
        'position': current_user.position,
        'language': current_user.language
    }
    
    # إخفاء البيانات الحساسة
    user_data = hide_sensitive_data(user_data)
    
    return jsonify(user_data)
