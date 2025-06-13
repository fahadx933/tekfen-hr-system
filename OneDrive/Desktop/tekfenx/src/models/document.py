"""
نماذج المستندات والملفات
"""
from .base import db, TimestampMixin


class Document(db.Model, TimestampMixin):
    """
    نموذج المستندات
    """
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # بالبايت
    is_private = db.Column(db.Boolean, default=True)
    
    def __init__(self, user_id, title, file_path, file_type, file_size, **kwargs):
        self.user_id = user_id
        self.title = title
        self.file_path = file_path
        self.file_type = file_type
        self.file_size = file_size
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f'<Document {self.title}>'
