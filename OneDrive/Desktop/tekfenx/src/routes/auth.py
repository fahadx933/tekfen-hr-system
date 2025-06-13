"""
مسارات المصادقة وتسجيل الدخول
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from .. import db
from ..models.user import User, Role
from ..utils.decorators import admin_required

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    صفحة تسجيل الدخول
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(username=username).first()
        
        # التحقق من وجود المستخدم وصحة كلمة المرور
        if not user or not user.check_password(password):
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'danger')
            return redirect(url_for('auth.login'))
        
        # التحقق من حالة المستخدم
        if not user.is_active:
            flash('هذا الحساب غير نشط. يرجى التواصل مع مدير النظام', 'warning')
            return redirect(url_for('auth.login'))
        
        # تسجيل الدخول
        login_user(user, remember=remember)
        
        # تحديث آخر تسجيل دخول
        user.last_login = db.func.current_timestamp()
        db.session.commit()
        
        # تسجيل عملية تسجيل الدخول
        from ..models.communication import Log
        log = Log(
            user_id=user.id,
            action='تسجيل الدخول',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(log)
        db.session.commit()
        
        # توجيه المستخدم إلى الصفحة التي كان يحاول الوصول إليها
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            if user.is_admin():
                next_page = url_for('admin.dashboard')
            else:
                next_page = url_for('main.index')
        
        # تعيين اللغة المفضلة للمستخدم
        session['language'] = user.language
        
        return redirect(next_page)
    
    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    """
    تسجيل الخروج
    """
    # تسجيل عملية تسجيل الخروج
    from ..models.communication import Log
    log = Log(
        user_id=current_user.id,
        action='تسجيل الخروج',
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string
    )
    db.session.add(log)
    db.session.commit()
    
    logout_user()
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('auth.login'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """
    تغيير كلمة المرور
    """
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # التحقق من صحة كلمة المرور الحالية
        if not current_user.check_password(current_password):
            flash('كلمة المرور الحالية غير صحيحة', 'danger')
            return redirect(url_for('auth.change_password'))
        
        # التحقق من تطابق كلمة المرور الجديدة
        if new_password != confirm_password:
            flash('كلمة المرور الجديدة غير متطابقة', 'danger')
            return redirect(url_for('auth.change_password'))
        
        # التحقق من طول كلمة المرور
        if len(new_password) < 8:
            flash('يجب أن تكون كلمة المرور الجديدة 8 أحرف على الأقل', 'danger')
            return redirect(url_for('auth.change_password'))
        
        # تغيير كلمة المرور
        current_user.set_password(new_password)
        db.session.commit()
        
        # تسجيل عملية تغيير كلمة المرور
        from ..models.communication import Log
        log = Log(
            user_id=current_user.id,
            action='تغيير كلمة المرور',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(log)
        db.session.commit()
        
        flash('تم تغيير كلمة المرور بنجاح', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('auth/change_password.html')


@auth.route('/change-language/<language>')
@login_required
def change_language(language):
    """
    تغيير اللغة
    """
    if language in ['ar', 'en']:
        current_user.language = language
        session['language'] = language
        db.session.commit()
        
        # تسجيل عملية تغيير اللغة
        from ..models.communication import Log
        log = Log(
            user_id=current_user.id,
            action=f'تغيير اللغة إلى {language}',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(log)
        db.session.commit()
    
    return redirect(request.referrer or url_for('main.index'))
