import os
from datetime import timedelta

class Config:
    """قاعدة التكوين الأساسية"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tekfen-hr-system-secret-key-2025'
    
    # إعدادات قاعدة البيانات
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///tekfen_hr.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # إعدادات الجلسة
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True
    
    # إعدادات تعدد اللغات
    LANGUAGES = ['ar', 'en']
    BABEL_DEFAULT_LOCALE = 'ar'
    
    # إعدادات تحميل الملفات
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 ميجابايت
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'xls', 'xlsx'}
    
    # إعدادات البريد الإلكتروني
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@tekfen.com'
    
    # إعدادات الأمان
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or 'tekfen-hr-system-salt-2025'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_LENGTH_MIN = 8
    
    # إعدادات التسجيل
    LOGIN_DISABLED = False
    LOGIN_VIEW = 'auth.login'
    
    # إعدادات التطبيق
    APP_NAME = 'نظام إدارة الموارد البشرية - TEKFEN'
    COMPANY_NAME = 'TEKFEN'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@tekfen.com'
    
    # إعدادات التطوير
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """إعدادات بيئة التطوير"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///tekfen_hr_dev.db'


class TestingConfig(Config):
    """إعدادات بيئة الاختبار"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///tekfen_hr_test.db'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """إعدادات بيئة الإنتاج"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # إعدادات إضافية للإنتاج
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
