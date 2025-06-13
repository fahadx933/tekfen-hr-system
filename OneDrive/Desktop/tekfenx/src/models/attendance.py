"""
نماذج الحضور والإجازات والاستئذان
"""
from datetime import datetime
from .base import db, TimestampMixin


class Attendance(db.Model, TimestampMixin):
    """
    نموذج الحضور والانصراف
    """
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    check_in = db.Column(db.DateTime, nullable=True)
    check_out = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='حاضر')  # حاضر، متأخر، غائب
    note = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # العلاقات
    creator = db.relationship('User', foreign_keys=[created_by], backref=db.backref('created_attendances', lazy='dynamic'))
    updater = db.relationship('User', foreign_keys=[updated_by], backref=db.backref('updated_attendances', lazy='dynamic'))
    
    def __init__(self, user_id, **kwargs):
        self.user_id = user_id
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f'<Attendance {self.user_id} {self.check_in}>'


class LeaveType(db.Model, TimestampMixin):
    """
    نموذج أنواع الإجازات
    """
    __tablename__ = 'leave_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    days_allowed = db.Column(db.Integer, default=0)
    
    # العلاقات
    leaves = db.relationship('Leave', backref='leave_type', lazy='dynamic')
    
    def __init__(self, name, days_allowed=0, description=None):
        self.name = name
        self.days_allowed = days_allowed
        self.description = description
    
    def __repr__(self):
        return f'<LeaveType {self.name}>'


class Leave(db.Model, TimestampMixin):
    """
    نموذج طلبات الإجازة
    """
    __tablename__ = 'leaves'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    leave_type_id = db.Column(db.Integer, db.ForeignKey('leave_types.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='معلق')  # معلق، موافق، مرفوض
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    
    # العلاقات
    approver = db.relationship('User', foreign_keys=[approved_by], backref=db.backref('approved_leaves', lazy='dynamic'))
    
    def __init__(self, user_id, leave_type_id, start_date, end_date, **kwargs):
        self.user_id = user_id
        self.leave_type_id = leave_type_id
        self.start_date = start_date
        self.end_date = end_date
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f'<Leave {self.user_id} {self.start_date} to {self.end_date}>'


class PermissionRequest(db.Model, TimestampMixin):
    """
    نموذج طلبات الاستئذان
    """
    __tablename__ = 'permissions_request'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='معلق')  # معلق، موافق، مرفوض
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    
    # العلاقات
    approver = db.relationship('User', foreign_keys=[approved_by], backref=db.backref('approved_permissions', lazy='dynamic'))
    
    def __init__(self, user_id, date, start_time, end_time, **kwargs):
        self.user_id = user_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f'<PermissionRequest {self.user_id} {self.date} {self.start_time}-{self.end_time}>'
