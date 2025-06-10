"""
نقطة الدخول الرئيسية للتطبيق
"""
import os
from src import create_app, db
from src.models.user import User, Role, Permission, Department
from src.models.attendance import Attendance, LeaveType, Leave, PermissionRequest
from src.models.salary import Salary, SalaryCertificate
from src.models.document import Document
from src.models.training import TrainingCourse, TrainingEnrollment
from src.models.communication import Message, Announcement, Complaint, Log
from flask_migrate import Migrate

# تحديد وضع التشغيل من متغير البيئة أو استخدام وضع التطوير افتراضياً
app = create_app(os.getenv('FLASK_CONFIG') or 'development')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    """
    توفير سياق للصدفة التفاعلية
    """
    return dict(
        app=app, db=db, User=User, Role=Role, Permission=Permission,
        Department=Department, Attendance=Attendance, LeaveType=LeaveType,
        Leave=Leave, PermissionRequest=PermissionRequest, Salary=Salary,
        SalaryCertificate=SalaryCertificate, Document=Document,
        TrainingCourse=TrainingCourse, TrainingEnrollment=TrainingEnrollment,
        Message=Message, Announcement=Announcement, Complaint=Complaint, Log=Log
    )

@app.cli.command()
def test():
    """
    تشغيل الاختبارات
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
def create_admin():
    """
    إنشاء حساب مدير النظام
    """
    # التحقق من وجود الأدوار
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', description='مدير النظام')
        db.session.add(admin_role)
        db.session.commit()
    
    # التحقق من وجود مدير النظام
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
        print('تم إنشاء حساب مدير النظام بنجاح')
    else:
        print('حساب مدير النظام موجود بالفعل')

@app.cli.command()
def create_demo_data():
    """
    إنشاء بيانات تجريبية
    """
    # إنشاء الأدوار
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
    
    # إنشاء الأقسام
    hr_dept = Department.query.filter_by(name='الموارد البشرية').first()
    if not hr_dept:
        hr_dept = Department(name='الموارد البشرية', description='قسم الموارد البشرية')
        db.session.add(hr_dept)
    
    it_dept = Department.query.filter_by(name='تكنولوجيا المعلومات').first()
    if not it_dept:
        it_dept = Department(name='تكنولوجيا المعلومات', description='قسم تكنولوجيا المعلومات')
        db.session.add(it_dept)
    
    finance_dept = Department.query.filter_by(name='المالية').first()
    if not finance_dept:
        finance_dept = Department(name='المالية', description='قسم المالية')
        db.session.add(finance_dept)
    
    db.session.commit()
    
    # إنشاء المستخدمين
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@tekfen.com',
            first_name='مدير',
            last_name='النظام',
            role_id=admin_role.id,
            department_id=hr_dept.id,
            position='مدير النظام'
        )
        admin.set_password('admin123')
        db.session.add(admin)
    
    hr_supervisor = User.query.filter_by(username='hr_supervisor').first()
    if not hr_supervisor:
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
    
    it_supervisor = User.query.filter_by(username='it_supervisor').first()
    if not it_supervisor:
        it_supervisor = User(
            username='it_supervisor',
            email='it_supervisor@tekfen.com',
            first_name='مشرف',
            last_name='تكنولوجيا المعلومات',
            role_id=supervisor_role.id,
            department_id=it_dept.id,
            position='مشرف تكنولوجيا المعلومات'
        )
        it_supervisor.set_password('password')
        db.session.add(it_supervisor)
    
    employee1 = User.query.filter_by(username='employee').first()
    if not employee1:
        employee1 = User(
            username='employee',
            email='employee@tekfen.com',
            first_name='موظف',
            last_name='عادي',
            role_id=employee_role.id,
            department_id=hr_dept.id,
            position='موظف موارد بشرية'
        )
        employee1.set_password('password')
        db.session.add(employee1)
    
    employee2 = User.query.filter_by(username='employee2').first()
    if not employee2:
        employee2 = User(
            username='employee2',
            email='employee2@tekfen.com',
            first_name='أحمد',
            last_name='محمد',
            role_id=employee_role.id,
            department_id=it_dept.id,
            position='مطور برمجيات'
        )
        employee2.set_password('password')
        db.session.add(employee2)
    
    db.session.commit()
    
    # إنشاء أنواع الإجازات
    annual_leave = LeaveType.query.filter_by(name='إجازة سنوية').first()
    if not annual_leave:
        annual_leave = LeaveType(name='إجازة سنوية', days_allowed=21, description='الإجازة السنوية المدفوعة')
        db.session.add(annual_leave)
    
    sick_leave = LeaveType.query.filter_by(name='إجازة مرضية').first()
    if not sick_leave:
        sick_leave = LeaveType(name='إجازة مرضية', days_allowed=14, description='إجازة مرضية مدفوعة')
        db.session.add(sick_leave)
    
    unpaid_leave = LeaveType.query.filter_by(name='إجازة بدون راتب').first()
    if not unpaid_leave:
        unpaid_leave = LeaveType(name='إجازة بدون راتب', days_allowed=30, description='إجازة بدون راتب')
        db.session.add(unpaid_leave)
    
    db.session.commit()
    
    # إنشاء إعلانات
    if Announcement.query.count() == 0:
        announcement1 = Announcement(
            title='مرحباً بكم في نظام إدارة الموارد البشرية',
            content='مرحباً بكم في نظام إدارة الموارد البشرية الجديد لشركة TEKFEN. يمكنكم الآن استخدام النظام لإدارة الحضور والإجازات والاستئذان وغيرها من الخدمات.',
            start_date='2025-06-01',
            created_by=admin.id
        )
        db.session.add(announcement1)
        
        announcement2 = Announcement(
            title='دورة تدريبية جديدة',
            content='تعلن إدارة الموارد البشرية عن دورة تدريبية جديدة في مجال تطوير الذات. للتسجيل يرجى التواصل مع قسم الموارد البشرية.',
            start_date='2025-06-05',
            end_date='2025-06-20',
            created_by=hr_supervisor.id
        )
        db.session.add(announcement2)
    
    db.session.commit()
    
    print('تم إنشاء البيانات التجريبية بنجاح')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
