"""
ملف التهيئة للنشر على منصة Render
"""
# run.py - ملف التشغيل لمنصة Render

import os
from src import create_app, db
from src.models.user import User, Role, Permission, Department
from src.models.attendance import Attendance, LeaveType, Leave, PermissionRequest
from src.models.salary import Salary, SalaryCertificate
from src.models.document import Document
from src.models.training import TrainingCourse, TrainingEnrollment
from src.models.communication import Message, Announcement, Complaint, Log

app = create_app(os.getenv('FLASK_CONFIG') or 'production')

@app.before_first_request
def create_tables():
    """
    إنشاء الجداول وبيانات البدء
    """
    db.create_all()
    
    # إنشاء الأدوار الأساسية إذا لم تكن موجودة
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', description='مدير النظام')
        db.session.add(admin_role)
    
    supervisor_role = Role.query.filter_by(name='supervisor').first()
    if not supervisor_role:
        supervisor_role = Role(name='supervisor', description='مشرف')
        db.session.add(supervisor_role)
    
    employee_role = Role.query.filter_by(name='employee').first()
    if not employee_role:
        employee_role = Role(name='employee', description='موظف')
        db.session.add(employee_role)
    
    db.session.commit()
    
    # إنشاء حساب مدير النظام إذا لم يكن موجوداً
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@tekfen.com',
            first_name='مدير',
            last_name='النظام',
            role_id=admin_role.id
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
    
    # إنشاء حساب مشرف الموارد البشرية إذا لم يكن موجوداً
    hr_supervisor = User.query.filter_by(username='hr_supervisor').first()
    if not hr_supervisor:
        # إنشاء قسم الموارد البشرية أولاً
        hr_dept = Department.query.filter_by(name='الموارد البشرية').first()
        if not hr_dept:
            hr_dept = Department(name='الموارد البشرية', description='قسم الموارد البشرية')
            db.session.add(hr_dept)
            db.session.commit()
        
        hr_supervisor = User(
            username='hr_supervisor',
            email='hr_supervisor@tekfen.com',
            first_name='مشرف',
            last_name='الموارد البشرية',
            role_id=supervisor_role.id,
            department_id=hr_dept.id,
            position='مشرف الموارد البشرية'
        )
        hr_supervisor.set_password('password')
        db.session.add(hr_supervisor)
        db.session.commit()
    
    # إنشاء حساب موظف عادي إذا لم يكن موجوداً
    employee = User.query.filter_by(username='employee').first()
    if not employee:
        # التأكد من وجود قسم الموارد البشرية
        hr_dept = Department.query.filter_by(name='الموارد البشرية').first()
        if not hr_dept:
            hr_dept = Department(name='الموارد البشرية', description='قسم الموارد البشرية')
            db.session.add(hr_dept)
            db.session.commit()
        
        employee = User(
            username='employee',
            email='employee@tekfen.com',
            first_name='موظف',
            last_name='عادي',
            role_id=employee_role.id,
            department_id=hr_dept.id,
            position='موظف موارد بشرية'
        )
        employee.set_password('password')
        db.session.add(employee)
        db.session.commit()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
