"""
مسارات لوحة التحكم الإدارية
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from .. import db
from ..models.user import User, Role, Permission, Department
from ..models.attendance import Attendance, LeaveType
from ..models.communication import Log
from ..utils.decorators import admin_required

admin = Blueprint('admin', __name__)


@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """
    لوحة التحكم الرئيسية للمدير
    """
    # إحصائيات عامة
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    departments = Department.query.count()
    
    # آخر سجلات النظام
    recent_logs = Log.query.order_by(Log.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                          total_users=total_users,
                          active_users=active_users,
                          departments=departments,
                          recent_logs=recent_logs)


@admin.route('/users')
@login_required
@admin_required
def users():
    """
    إدارة المستخدمين
    """
    users_list = User.query.all()
    roles = Role.query.all()
    departments = Department.query.all()
    
    return render_template('admin/users.html', 
                          users=users_list,
                          roles=roles,
                          departments=departments)


@admin.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    """
    إضافة مستخدم جديد
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        role_id = request.form.get('role_id')
        department_id = request.form.get('department_id')
        position = request.form.get('position')
        
        # التحقق من عدم وجود مستخدم بنفس اسم المستخدم أو البريد الإلكتروني
        if User.query.filter_by(username=username).first():
            flash('اسم المستخدم موجود بالفعل', 'danger')
            return redirect(url_for('admin.add_user'))
        
        if User.query.filter_by(email=email).first():
            flash('البريد الإلكتروني موجود بالفعل', 'danger')
            return redirect(url_for('admin.add_user'))
        
        # إنشاء المستخدم الجديد
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role_id=role_id,
            department_id=department_id,
            position=position
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # تسجيل العملية
        log = Log(
            user_id=current_user.id,
            action='إضافة مستخدم جديد',
            entity_type='user',
            entity_id=user.id,
            details=f'تمت إضافة المستخدم {username}',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(log)
        db.session.commit()
        
        flash('تمت إضافة المستخدم بنجاح', 'success')
        return redirect(url_for('admin.users'))
    
    roles = Role.query.all()
    departments = Department.query.all()
    
    return render_template('admin/add_user.html',
                          roles=roles,
                          departments=departments)


@admin.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """
    تعديل بيانات مستخدم
    """
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        role_id = request.form.get('role_id')
        department_id = request.form.get('department_id')
        position = request.form.get('position')
        is_active = True if request.form.get('is_active') else False
        
        # التحقق من عدم وجود مستخدم آخر بنفس اسم المستخدم أو البريد الإلكتروني
        username_exists = User.query.filter(User.username == username, User.id != user_id).first()
        if username_exists:
            flash('اسم المستخدم موجود بالفعل', 'danger')
            return redirect(url_for('admin.edit_user', user_id=user_id))
        
        email_exists = User.query.filter(User.email == email, User.id != user_id).first()
        if email_exists:
            flash('البريد الإلكتروني موجود بالفعل', 'danger')
            return redirect(url_for('admin.edit_user', user_id=user_id))
        
        # تحديث بيانات المستخدم
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.role_id = role_id
        user.department_id = department_id
        user.position = position
        user.is_active = is_active
        
        # تحديث كلمة المرور إذا تم توفيرها
        new_password = request.form.get('password')
        if new_password:
            user.set_password(new_password)
        
        db.session.commit()
        
        # تسجيل العملية
        log = Log(
            user_id=current_user.id,
            action='تعديل بيانات مستخدم',
            entity_type='user',
            entity_id=user.id,
            details=f'تم تعديل بيانات المستخدم {username}',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(log)
        db.session.commit()
        
        flash('تم تعديل بيانات المستخدم بنجاح', 'success')
        return redirect(url_for('admin.users'))
    
    roles = Role.query.all()
    departments = Department.query.all()
    
    return render_template('admin/edit_user.html',
                          user=user,
                          roles=roles,
                          departments=departments)


@admin.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """
    حذف مستخدم
    """
    user = User.query.get_or_404(user_id)
    
    # لا يمكن حذف المستخدم الحالي
    if user.id == current_user.id:
        flash('لا يمكنك حذف حسابك الشخصي', 'danger')
        return redirect(url_for('admin.users'))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    # تسجيل العملية
    log = Log(
        user_id=current_user.id,
        action='حذف مستخدم',
        entity_type='user',
        entity_id=user_id,
        details=f'تم حذف المستخدم {username}',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string
    )
    db.session.add(log)
    db.session.commit()
    
    flash('تم حذف المستخدم بنجاح', 'success')
    return redirect(url_for('admin.users'))


@admin.route('/roles')
@login_required
@admin_required
def roles():
    """
    إدارة الأدوار
    """
    roles_list = Role.query.all()
    permissions = Permission.query.all()
    
    return render_template('admin/roles.html',
                          roles=roles_list,
                          permissions=permissions)


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_role():
    """
    إضافة دور جديد
    """
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        permission_ids = request.form.getlist('permissions')
        
        # التحقق من عدم وجود دور بنفس الاسم
        if Role.query.filter_by(name=name).first():
            flash('اسم الدور موجود بالفعل', 'danger')
            return redirect(url_for('admin.add_role'))
        
        # إنشاء الدور الجديد
        role = Role(name=name, description=description)
        
        # إضافة الصلاحيات
        for permission_id in permission_ids:
            permission = Permission.query.get(permission_id)
            if permission:
                role.add_permission(permission)
        
        db.session.add(role)
        db.session.commit()
        
        # تسجيل العملية
        log = Log(
            user_id=current_user.id,
            action='إضافة دور جديد',
            entity_type='role',
            entity_id=role.id,
            details=f'تمت إضافة الدور {name}',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(log)
        db.session.commit()
        
        flash('تمت إضافة الدور بنجاح', 'success')
        return redirect(url_for('admin.roles'))
    
    permissions = Permission.query.all()
    
    return render_template('admin/add_role.html',
                          permissions=permissions)


@admin.route('/departments')
@login_required
@admin_required
def departments():
    """
    إدارة الأقسام
    """
    departments_list = Department.query.all()
    managers = User.query.filter(User.role.has(name='supervisor')).all()
    
    return render_template('admin/departments.html',
                          departments=departments_list,
                          managers=managers)


@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_department():
    """
    إضافة قسم جديد
    """
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        manager_id = request.form.get('manager_id')
        
        # التحقق من عدم وجود قسم بنفس الاسم
        if Department.query.filter_by(name=name).first():
            flash('اسم القسم موجود بالفعل', 'danger')
            return redirect(url_for('admin.add_department'))
        
        # إنشاء القسم الجديد
        department = Department(
            name=name,
            description=description,
            manager_id=manager_id if manager_id else None
        )
        
        db.session.add(department)
        db.session.commit()
        
        # تسجيل العملية
        log = Log(
            user_id=current_user.id,
            action='إضافة قسم جديد',
            entity_type='department',
            entity_id=department.id,
            details=f'تمت إضافة القسم {name}',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(log)
        db.session.commit()
        
        flash('تمت إضافة القسم بنجاح', 'success')
        return redirect(url_for('admin.departments'))
    
    managers = User.query.filter(User.role.has(name='supervisor')).all()
    
    return render_template('admin/add_department.html',
                          managers=managers)


@admin.route('/logs')
@login_required
@admin_required
def logs():
    """
    عرض سجلات النظام
    """
    page = request.args.get('page', 1, type=int)
    logs_list = Log.query.order_by(Log.created_at.desc()).paginate(page=page, per_page=50)
    
    return render_template('admin/logs.html', logs=logs_list)


@admin.route('/system-settings', methods=['GET', 'POST'])
@login_required
@admin_required
def system_settings():
    """
    إعدادات النظام
    """
    if request.method == 'POST':
        # تحديث الإعدادات
        # يمكن إضافة المزيد من الإعدادات حسب الحاجة
        
        flash('تم تحديث إعدادات النظام بنجاح', 'success')
        return redirect(url_for('admin.system_settings'))
    
    return render_template('admin/system_settings.html')
