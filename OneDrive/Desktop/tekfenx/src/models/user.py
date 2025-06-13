"""
نموذج المستخدمين والأدوار والصلاحيات
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .base import db, TimestampMixin

# جدول العلاقة بين الأدوار والصلاحيات
role_permissions = db.Table(
    'role_permissions',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), nullable=False),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), nullable=False),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)


class User(db.Model, UserMixin, TimestampMixin):
    """
    نموذج المستخدم
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    position = db.Column(db.String(100), nullable=True)
    hire_date = db.Column(db.Date, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime, nullable=True)
    language = db.Column(db.String(10), default='ar')
    
    # العلاقات
    role = db.relationship('Role', backref=db.backref('users', lazy='dynamic'))
    department = db.relationship('Department', backref=db.backref('users', lazy='dynamic'))
    attendances = db.relationship('Attendance', backref='user', lazy='dynamic')
    leaves = db.relationship('Leave', backref='user', lazy='dynamic')
    permission_requests = db.relationship('PermissionRequest', backref='user', lazy='dynamic')
    salary_certificates = db.relationship('SalaryCertificate', backref='user', lazy='dynamic')
    documents = db.relationship('Document', backref='user', lazy='dynamic')
    complaints = db.relationship('Complaint', backref='user', lazy='dynamic')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic')
    
    def __init__(self, username, email, first_name, last_name, role_id, **kwargs):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.role_id = role_id
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def set_password(self, password):
        """
        تعيين كلمة المرور المشفرة
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        التحقق من صحة كلمة المرور
        """
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """
        الحصول على الاسم الكامل للمستخدم
        """
        return f"{self.first_name} {self.last_name}"
    
    def has_permission(self, permission_name):
        """
        التحقق مما إذا كان المستخدم يملك صلاحية معينة
        """
        if not self.role:
            return False
        
        for permission in self.role.permissions:
            if permission.name == permission_name:
                return True
        
        return False
    
    def is_admin(self):
        """
        التحقق مما إذا كان المستخدم مدير نظام
        """
        return self.role.name == 'admin'
    
    def is_supervisor(self):
        """
        التحقق مما إذا كان المستخدم مشرف
        """
        return self.role.name == 'supervisor'
    
    def __repr__(self):
        return f'<User {self.username}>'


class Role(db.Model, TimestampMixin):
    """
    نموذج الدور
    """
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # العلاقات
    permissions = db.relationship('Permission', secondary=role_permissions, backref=db.backref('roles', lazy='dynamic'))
    
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
    
    def add_permission(self, permission):
        """
        إضافة صلاحية للدور
        """
        if permission not in self.permissions:
            self.permissions.append(permission)
    
    def remove_permission(self, permission):
        """
        إزالة صلاحية من الدور
        """
        if permission in self.permissions:
            self.permissions.remove(permission)
    
    def __repr__(self):
        return f'<Role {self.name}>'


class Permission(db.Model, TimestampMixin):
    """
    نموذج الصلاحية
    """
    __tablename__ = 'permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
    
    def __repr__(self):
        return f'<Permission {self.name}>'


class Department(db.Model, TimestampMixin):
    """
    نموذج القسم
    """
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    description = db.Column(db.Text, nullable=True)
    
    # العلاقات
    manager = db.relationship('User', foreign_keys=[manager_id], backref=db.backref('managed_department', uselist=False))
    
    def __init__(self, name, description=None, manager_id=None):
        self.name = name
        self.description = description
        self.manager_id = manager_id
    
    def __repr__(self):
        return f'<Department {self.name}>'
