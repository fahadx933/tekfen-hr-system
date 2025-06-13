"""
نماذج التدريب والتطوير
"""
from .base import db, TimestampMixin


class TrainingCourse(db.Model, TimestampMixin):
    """
    نموذج الدورات التدريبية
    """
    __tablename__ = 'training_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(100), nullable=True)
    instructor = db.Column(db.String(100), nullable=True)
    max_participants = db.Column(db.Integer, default=0)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # العلاقات
    creator = db.relationship('User', foreign_keys=[created_by], backref=db.backref('created_courses', lazy='dynamic'))
    enrollments = db.relationship('TrainingEnrollment', backref='course', lazy='dynamic')
    
    def __init__(self, title, start_date, end_date, **kwargs):
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f'<TrainingCourse {self.title}>'


class TrainingEnrollment(db.Model, TimestampMixin):
    """
    نموذج تسجيل الدورات
    """
    __tablename__ = 'training_enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('training_courses.id'), nullable=False)
    status = db.Column(db.String(20), default='معلق')  # معلق، مقبول، مرفوض، مكتمل
    enrollment_date = db.Column(db.Date, nullable=False)
    completion_date = db.Column(db.Date, nullable=True)
    certificate_path = db.Column(db.String(255), nullable=True)
    
    # العلاقات
    user = db.relationship('User', backref=db.backref('training_enrollments', lazy='dynamic'))
    
    def __init__(self, user_id, course_id, enrollment_date, **kwargs):
        self.user_id = user_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f'<TrainingEnrollment {self.user_id} {self.course_id}>'
