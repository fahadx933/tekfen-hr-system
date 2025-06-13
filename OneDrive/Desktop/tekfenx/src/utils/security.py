"""
وحدة المساعدة للأمان
"""
import re
import secrets
import string
from flask import session, request, abort
from flask_login import current_user
from functools import wraps

def generate_csrf_token():
    """
    إنشاء رمز CSRF
    """
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(16)
    return session['_csrf_token']

def validate_csrf_token(token):
    """
    التحقق من صحة رمز CSRF
    """
    return token and '_csrf_token' in session and token == session['_csrf_token']

def csrf_protect(f):
    """
    مزخرف لحماية النماذج من هجمات CSRF
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "POST":
            token = request.form.get('_csrf_token')
            if not validate_csrf_token(token):
                abort(403)
        return f(*args, **kwargs)
    return decorated_function

def generate_secure_password(length=12):
    """
    إنشاء كلمة مرور آمنة
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def is_password_strong(password):
    """
    التحقق من قوة كلمة المرور
    """
    if len(password) < 8:
        return False
    
    # يجب أن تحتوي على حرف كبير واحد على الأقل
    if not re.search(r'[A-Z]', password):
        return False
    
    # يجب أن تحتوي على حرف صغير واحد على الأقل
    if not re.search(r'[a-z]', password):
        return False
    
    # يجب أن تحتوي على رقم واحد على الأقل
    if not re.search(r'[0-9]', password):
        return False
    
    # يجب أن تحتوي على رمز خاص واحد على الأقل
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    
    return True

def sanitize_input(text):
    """
    تنظيف المدخلات من الرموز الخاصة
    """
    if text is None:
        return ""
    
    # إزالة أكواد HTML والجافا سكريبت
    text = re.sub(r'<[^>]*>', '', text)
    
    # إزالة أكواد الجافا سكريبت
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    
    # إزالة أكواد SQL
    text = re.sub(r'(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE|UNION)', 
                 lambda m: m.group(1).lower(), text, flags=re.IGNORECASE)
    
    return text

def hide_sensitive_data(data, fields_to_hide=None):
    """
    إخفاء البيانات الحساسة
    """
    if fields_to_hide is None:
        fields_to_hide = ['password', 'password_hash', 'token', 'secret']
    
    if isinstance(data, dict):
        for field in fields_to_hide:
            if field in data:
                data[field] = '********'
    
    return data

def log_security_event(db, user_id, action, details=None, ip_address=None, user_agent=None):
    """
    تسجيل حدث أمني
    """
    from ..models.communication import Log
    
    log = Log(
        user_id=user_id,
        action=action,
        details=details,
        ip_address=ip_address or request.remote_addr,
        user_agent=user_agent or request.user_agent.string
    )
    
    db.session.add(log)
    db.session.commit()

def rate_limit(max_requests=5, window=60):
    """
    مزخرف للحد من عدد الطلبات
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # يمكن تنفيذ آلية الحد من عدد الطلبات هنا
            # باستخدام Redis أو قاعدة بيانات أخرى
            return f(*args, **kwargs)
        return decorated_function
    return decorator
