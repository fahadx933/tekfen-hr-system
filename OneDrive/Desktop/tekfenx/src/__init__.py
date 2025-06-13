"""
تهيئة التطبيق وربط النماذج البرمجية
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_babel import Babel
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

from .config.config import config

# تهيئة المكتبات
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
babel = Babel()
mail = Mail()
csrf = CSRFProtect()

def create_app(config_name='default'):
    """
    إنشاء وتهيئة تطبيق Flask
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # تهيئة المكتبات مع التطبيق
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'يرجى تسجيل الدخول للوصول إلى هذه الصفحة'
    migrate.init_app(app, db)
    babel.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    
    # استيراد النماذج
    from .models.user import User, Role, Permission, Department
    from .models.attendance import Attendance, Leave, LeaveType, PermissionRequest
    from .models.salary import Salary, SalaryCertificate
    from .models.document import Document
    from .models.training import TrainingCourse, TrainingEnrollment
    from .models.communication import Message, Announcement, Complaint, Log
    
    # تسجيل مستخرج المستخدم لـ Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # تسجيل المسارات (Blueprints)
    from .routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .routes.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    from .routes.attendance import attendance as attendance_blueprint
    app.register_blueprint(attendance_blueprint, url_prefix='/attendance')
    
    from .routes.leaves import leaves as leaves_blueprint
    app.register_blueprint(leaves_blueprint, url_prefix='/leaves')
    
    from .routes.permissions import permissions as permissions_blueprint
    app.register_blueprint(permissions_blueprint, url_prefix='/permissions')
    
    from .routes.salary import salary as salary_blueprint
    app.register_blueprint(salary_blueprint, url_prefix='/salary')
    
    from .routes.documents import documents as documents_blueprint
    app.register_blueprint(documents_blueprint, url_prefix='/documents')
    
    from .routes.training import training as training_blueprint
    app.register_blueprint(training_blueprint, url_prefix='/training')
    
    from .routes.messages import messages as messages_blueprint
    app.register_blueprint(messages_blueprint, url_prefix='/messages')
    
    from .routes.announcements import announcements as announcements_blueprint
    app.register_blueprint(announcements_blueprint, url_prefix='/announcements')
    
    from .routes.complaints import complaints as complaints_blueprint
    app.register_blueprint(complaints_blueprint, url_prefix='/complaints')
    
    # تهيئة Babel للغات
    @babel.localeselector
    def get_locale():
        from flask import request, session, g
        from flask_login import current_user
        
        # الأولوية للغة المخزنة في الجلسة
        if 'language' in session:
            return session['language']
        
        # ثم للغة المستخدم المسجل
        if current_user.is_authenticated:
            return current_user.language
        
        # ثم للغة المتصفح
        return request.accept_languages.best_match(app.config['LANGUAGES'])
    
    # إنشاء جميع الجداول عند بدء التطبيق
    @app.before_first_request
    def create_tables():
        db.create_all()
    
    return app
