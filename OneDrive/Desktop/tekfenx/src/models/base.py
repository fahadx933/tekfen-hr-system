"""
النموذج الأساسي لقاعدة البيانات
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TimestampMixin:
    """
    مزيج لإضافة حقول الطوابع الزمنية للإنشاء والتحديث
    """
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
