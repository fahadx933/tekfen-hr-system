"""
وحدة المساعدة لإخفاء بيانات المستخدمين
"""
from flask import g, session
from flask_login import current_user

class DataProtection:
    """
    فئة لإخفاء وحماية بيانات المستخدمين
    """
    
    @staticmethod
    def hide_user_data(user_data, current_user_role):
        """
        إخفاء بيانات المستخدم حسب دور المستخدم الحالي
        """
        # نسخة من البيانات لتجنب تعديل البيانات الأصلية
        protected_data = user_data.copy() if isinstance(user_data, dict) else user_data
        
        # إذا كان المستخدم مدير نظام، يمكنه رؤية جميع البيانات
        if current_user_role == 'admin':
            return protected_data
        
        # إذا كان المستخدم مشرف، يمكنه رؤية بعض البيانات
        if current_user_role == 'supervisor':
            if isinstance(protected_data, dict):
                # إخفاء البيانات الحساسة
                if 'password_hash' in protected_data:
                    protected_data.pop('password_hash')
                if 'last_login' in protected_data:
                    protected_data.pop('last_login')
            return protected_data
        
        # للمستخدم العادي، إخفاء معظم البيانات
        if isinstance(protected_data, dict):
            # الاحتفاظ فقط بالبيانات الأساسية
            allowed_fields = ['id', 'username', 'first_name', 'last_name', 'department_id', 'position']
            return {k: v for k, v in protected_data.items() if k in allowed_fields}
        
        return protected_data
    
    @staticmethod
    def filter_users_list(users_list, current_user_role, current_user_department=None):
        """
        تصفية قائمة المستخدمين حسب دور المستخدم الحالي
        """
        # إذا كان المستخدم مدير نظام، يمكنه رؤية جميع المستخدمين
        if current_user_role == 'admin':
            return users_list
        
        # إذا كان المستخدم مشرف، يمكنه رؤية المستخدمين في قسمه فقط
        if current_user_role == 'supervisor' and current_user_department:
            return [user for user in users_list if user.department_id == current_user_department]
        
        # للمستخدم العادي، لا يمكنه رؤية قائمة المستخدمين
        return []
    
    @staticmethod
    def can_view_user_details(user_id, current_user_id, current_user_role, current_user_department=None):
        """
        التحقق مما إذا كان المستخدم الحالي يمكنه عرض تفاصيل مستخدم معين
        """
        # المستخدم يمكنه دائماً عرض تفاصيله الشخصية
        if user_id == current_user_id:
            return True
        
        # مدير النظام يمكنه عرض تفاصيل أي مستخدم
        if current_user_role == 'admin':
            return True
        
        # المشرف يمكنه عرض تفاصيل المستخدمين في قسمه فقط
        if current_user_role == 'supervisor':
            from ..models.user import User
            user = User.query.get(user_id)
            if user and user.department_id == current_user_department:
                return True
        
        # في الحالات الأخرى، لا يمكن عرض التفاصيل
        return False
