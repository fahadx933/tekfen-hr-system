// وظائف JavaScript لموقع TEKFEN للموارد البشرية

// تحديث الوقت الحالي
function updateCurrentTime() {
    const now = new Date();
    const timeElement = document.getElementById('current-time');
    const dateElement = document.getElementById('current-date');
    
    if (timeElement) {
        timeElement.textContent = now.toLocaleTimeString('ar-SA');
    }
    
    if (dateElement) {
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        dateElement.textContent = now.toLocaleDateString('ar-SA', options);
    }
    
    setTimeout(updateCurrentTime, 1000);
}

// تسجيل الحضور
function checkIn() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('ar-SA');
    const statusElement = document.querySelector('.attendance-status');
    
    if (statusElement) {
        statusElement.innerHTML = `
            <div class="alert alert-success" role="alert">
                <i class="bi bi-check-circle"></i> تم تسجيل حضورك بنجاح في الساعة ${timeString}
            </div>
        `;
    }
    
    // تحديث حالة الحضور في الإحصائيات السريعة
    const attendanceStatusElement = document.querySelector('.quick-stats .card:first-child .badge');
    if (attendanceStatusElement) {
        attendanceStatusElement.className = 'badge bg-success';
        attendanceStatusElement.textContent = 'حاضر';
    }
    
    // إظهار إشعار
    showNotification('تم تسجيل الحضور', `تم تسجيل حضورك بنجاح في الساعة ${timeString}`);
}

// تسجيل الانصراف
function checkOut() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('ar-SA');
    const statusElement = document.querySelector('.attendance-status');
    
    if (statusElement) {
        statusElement.innerHTML = `
            <div class="alert alert-info" role="alert">
                <i class="bi bi-check-circle"></i> تم تسجيل انصرافك بنجاح في الساعة ${timeString}
            </div>
        `;
    }
    
    // تحديث حالة الحضور في الإحصائيات السريعة
    const attendanceStatusElement = document.querySelector('.quick-stats .card:first-child .badge');
    if (attendanceStatusElement) {
        attendanceStatusElement.className = 'badge bg-secondary';
        attendanceStatusElement.textContent = 'منصرف';
    }
    
    // إظهار إشعار
    showNotification('تم تسجيل الانصراف', `تم تسجيل انصرافك بنجاح في الساعة ${timeString}`);
}

// تسجيل الخروج
function logout() {
    // في النسخة الثابتة، نقوم بتوجيه المستخدم إلى صفحة تسجيل الدخول
    window.location.href = 'login_ar.html';
}

// تغيير اللغة
function changeLanguage(lang) {
    // في النسخة الثابتة، نقوم بتوجيه المستخدم إلى الصفحة المقابلة باللغة المختارة
    const currentPage = window.location.pathname.split('/').pop();
    
    if (lang === 'ar') {
        // إذا كانت الصفحة الحالية بالإنجليزية، نقوم بتحويلها إلى العربية
        if (currentPage.includes('_en.html')) {
            const arabicPage = currentPage.replace('_en.html', '_ar.html');
            window.location.href = arabicPage;
        }
    } else if (lang === 'en') {
        // إذا كانت الصفحة الحالية بالعربية، نقوم بتحويلها إلى الإنجليزية
        if (currentPage.includes('_ar.html')) {
            const englishPage = currentPage.replace('_ar.html', '_en.html');
            window.location.href = englishPage;
        }
    }
}

// إظهار إشعار
function showNotification(title, message) {
    // التحقق من دعم الإشعارات
    if (!("Notification" in window)) {
        alert("هذا المتصفح لا يدعم إشعارات سطح المكتب");
    }
    
    // التحقق من إذن الإشعارات
    else if (Notification.permission === "granted") {
        const notification = new Notification(title, {
            body: message,
            icon: 'images/tekfen.jpg'
        });
    }
    
    // طلب الإذن إذا لم يتم منحه بعد
    else if (Notification.permission !== "denied") {
        Notification.requestPermission().then(function (permission) {
            if (permission === "granted") {
                const notification = new Notification(title, {
                    body: message,
                    icon: 'images/tekfen.jpg'
                });
            }
        });
    }
}

// تعديل الملف الشخصي
function editProfile() {
    alert('سيتم فتح نموذج تعديل الملف الشخصي');
}

// تغيير صورة الملف الشخصي
function changeProfileImage() {
    alert('سيتم فتح نافذة اختيار صورة جديدة للملف الشخصي');
}

// تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    // تحديث الوقت الحالي
    updateCurrentTime();
    
    // إضافة مستمعي الأحداث للنماذج
    const leaveForm = document.getElementById('leaveRequestForm');
    if (leaveForm) {
        leaveForm.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('تم إرسال طلب الإجازة بنجاح');
            leaveForm.reset();
        });
    }
    
    const permissionForm = document.getElementById('permissionRequestForm');
    if (permissionForm) {
        permissionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('تم إرسال طلب الاستئذان بنجاح');
            permissionForm.reset();
        });
    }
    
    const complaintForm = document.getElementById('complaintForm');
    if (complaintForm) {
        complaintForm.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('تم إرسال الشكوى/الاقتراح بنجاح');
            complaintForm.reset();
        });
    }
    
    const messageForm = document.getElementById('messageForm');
    if (messageForm) {
        messageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('تم إرسال الرسالة بنجاح');
            messageForm.reset();
        });
    }
    
    const salaryForm = document.getElementById('salaryCertificateForm');
    if (salaryForm) {
        salaryForm.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('تم إرسال طلب تعريف الراتب بنجاح');
            salaryForm.reset();
        });
    }
    
    // إضافة مستمع الأحداث لنموذج تسجيل الدخول
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            // التحقق من بيانات تسجيل الدخول (محاكاة)
            if (username && password) {
                window.location.href = 'index_ar.html';
            } else {
                alert('يرجى إدخال اسم المستخدم وكلمة المرور');
            }
        });
    }
});
