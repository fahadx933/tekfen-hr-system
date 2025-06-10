// وظائف جافاسكريبت لنظام إدارة الموارد البشرية TEKFEN

// تحديث الوقت الحالي
function updateCurrentTime() {
    const now = new Date();
    const timeElement = document.getElementById('current-time');
    if (timeElement) {
        timeElement.textContent = now.toLocaleTimeString('ar-SA');
    }
}

// تشغيل تحديث الوقت كل ثانية
setInterval(updateCurrentTime, 1000);

// تهيئة tooltips بوتستراب
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // تهيئة popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // تفعيل التنبيهات التلقائية
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            setTimeout(function() {
                bsAlert.close();
            }, 5000);
        });
    }, 2000);
});

// طباعة المحتوى
function printContent() {
    window.print();
}

// تصدير البيانات إلى Excel
function exportToExcel(tableId, fileName) {
    const table = document.getElementById(tableId);
    if (!table) {
        console.error('Table not found');
        return;
    }
    
    const wb = XLSX.utils.table_to_book(table, {sheet: "Sheet JS"});
    XLSX.writeFile(wb, fileName + '.xlsx');
}

// التحقق من صحة نموذج
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) {
        console.error('Form not found');
        return false;
    }
    
    if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
        form.classList.add('was-validated');
        return false;
    }
    
    return true;
}

// تحميل البيانات عبر AJAX
function loadData(url, targetId) {
    const target = document.getElementById(targetId);
    if (!target) {
        console.error('Target element not found');
        return;
    }
    
    fetch(url)
        .then(response => response.text())
        .then(data => {
            target.innerHTML = data;
        })
        .catch(error => {
            console.error('Error loading data:', error);
            target.innerHTML = '<div class="alert alert-danger">حدث خطأ أثناء تحميل البيانات</div>';
        });
}

// تحديث عدد الرسائل غير المقروءة
function updateUnreadMessagesCount() {
    fetch('/messages/unread-count')
        .then(response => response.json())
        .then(data => {
            const badge = document.querySelector('.messages-badge');
            if (badge) {
                if (data.count > 0) {
                    badge.textContent = data.count;
                    badge.style.display = 'inline-block';
                } else {
                    badge.style.display = 'none';
                }
            }
        })
        .catch(error => console.error('Error updating unread messages count:', error));
}

// تحديث عدد الرسائل كل دقيقة
setInterval(updateUnreadMessagesCount, 60000);

// تغيير اللغة
function changeLanguage(lang) {
    window.location.href = '/auth/set-language/' + lang;
}

// تأكيد الحذف
function confirmDelete(message, formId) {
    if (confirm(message || 'هل أنت متأكد من الحذف؟')) {
        document.getElementById(formId).submit();
    }
}

// تحميل الصورة المختارة
function previewImage(input, previewId) {
    const preview = document.getElementById(previewId);
    if (!preview) {
        console.error('Preview element not found');
        return;
    }
    
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        }
        reader.readAsDataURL(input.files[0]);
    }
}
