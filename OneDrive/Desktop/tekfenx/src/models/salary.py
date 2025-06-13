"""
نماذج الرواتب وشهادات الراتب
"""
from .base import db, TimestampMixin


class Salary(db.Model, TimestampMixin):
    """
    نموذج الرواتب
    """
    __tablename__ = 'salaries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    basic_salary = db.Column(db.Numeric(10, 2), nullable=False)
    allowances = db.Column(db.Numeric(10, 2), default=0)
    deductions = db.Column(db.Numeric(10, 2), default=0)
    net_salary = db.Column(db.Numeric(10, 2), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    payment_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default='معلق')  # معلق، مدفوع
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # العلاقات
    user = db.relationship('User', backref=db.backref('salaries', lazy='dynamic'))
    creator = db.relationship('User', foreign_keys=[created_by], backref=db.backref('created_salaries', lazy='dynamic'))
    
    def __init__(self, user_id, basic_salary, month, year, **kwargs):
        self.user_id = user_id
        self.basic_salary = basic_salary
        self.month = month
        self.year = year
        
        # حساب صافي الراتب
        allowances = kwargs.get('allowances', 0)
        deductions = kwargs.get('deductions', 0)
        self.allowances = allowances
        self.deductions = deductions
        self.net_salary = basic_salary + allowances - deductions
        
        for key, value in kwargs.items():
            if key not in ['allowances', 'deductions']:
                setattr(self, key, value)
    
    def __repr__(self):
        return f'<Salary {self.user_id} {self.month}/{self.year}>'


class SalaryCertificate(db.Model, TimestampMixin):
    """
    نموذج شهادات الراتب
    """
    __tablename__ = 'salary_certificates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    request_date = db.Column(db.Date, nullable=False)
    purpose = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='معلق')  # معلق، مكتمل
    file_path = db.Column(db.String(255), nullable=True)
    
    def __init__(self, user_id, request_date, **kwargs):
        self.user_id = user_id
        self.request_date = request_date
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return f'<SalaryCertificate {self.user_id} {self.request_date}>'
