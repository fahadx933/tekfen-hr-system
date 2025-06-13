"""
نماذج الرسائل والإعلانات والشكاوى
"""
from .base import db, TimestampMixin


class Message(db.Model, TimestampMixin):
    """
    نموذج الرسائل
    """
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime, nullable=True)
    attachment_path = db.Column(db.String(255), nullable=True)
    
    def __init__(self, sender_id, receiver_id, subject, content, **kwargs):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.subject = subject
        self.content = content
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f'<Message {self.subject}>'


class Announcement(db.Model, TimestampMixin):
    """
    نموذج الإعلانات
    """
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # العلاقات
    creator = db.relationship('User', backref=db.backref('announcements', lazy='dynamic'))
    
    def __init__(self, title, content, start_date, created_by, **kwargs):
        self.title = title
        self.content = content
        self.start_date = start_date
        self.created_by = created_by
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f'<Announcement {self.title}>'


class Complaint(db.Model, TimestampMixin):
    """
    نموذج الشكاوى والاقتراحات
    """
    __tablename__ = 'complaints'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # شكوى، اقتراح
    status = db.Column(db.String(20), default='جديد')  # جديد، قيد المراجعة، مكتمل
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    resolution = db.Column(db.Text, nullable=True)
    
    # العلاقات
    assignee = db.relationship('User', foreign_keys=[assigned_to], backref=db.backref('assigned_complaints', lazy='dynamic'))
    
    def __init__(self, user_id, title, description, type, **kwargs):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.type = type
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f'<Complaint {self.title}>'


class Log(db.Model):
    """
    نموذج سجلات النظام
    """
    __tablename__ = 'logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    entity_type = db.Column(db.String(50), nullable=True)
    entity_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # العلاقات
    user = db.relationship('User', backref=db.backref('logs', lazy='dynamic'))
    
    def __init__(self, action, **kwargs):
        self.action = action
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f'<Log {self.action}>'
