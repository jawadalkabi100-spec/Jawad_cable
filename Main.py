import tkinter as tk
from tkinter import messagebox
import arabic_reshaper

# دالة لإصلاح النص العربي فقط
def fix_arabic(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return reshaped_text[::-1]

def calculate_pump_electricals(hp, distance, material, phase):
    if phase == '1':
        current = hp * 4.5
        allowed_vd = 11.0
        vd_factor = 2.0
        phase_num = "1"
        volt_text = "(220V)"
        cores = "2" 
    else:
        current = hp * 1.5
        allowed_vd = 19.0
        vd_factor = 1.732
        phase_num = "3"
        volt_text = "(380V)"
        cores = "3" 
        
    if material == '2':
        rho = 0.0282
        effective_current = current * 1.6 
        material_name = "ألمنيوم"
    else:
        rho = 0.0175
        effective_current = current
        material_name = "نحاس"

    ampacity_sizes = [
        (10, 1.5), (16, 2.5), (25, 4), (32, 6), (40, 10),
        (63, 16), (80, 25), (100, 35), (125, 50), (160, 70), 
        (200, 95), (250, 120), (300, 150), (350, 185), (400, 240)
    ]
    
    size_by_current = 0
    for max_amp, size in ampacity_sizes:
        if effective_current <= max_amp:
            size_by_current = size
            break
            
    area_by_vd = (vd_factor * current * distance * rho * 0.85) / allowed_vd
    required_area = max(size_by_current, area_by_vd)
    
    standard_sizes = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400]
    final_cable_size = 0
    
    for std_size in standard_sizes:
        if std_size >= required_area:
            final_cable_size = std_size
            break
            
    safe_current = current * 1.25
    standard_breakers = [10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 320, 400]
    breaker_size = 0
    
    for b in standard_breakers:
        if b >= safe_current:
            breaker_size = b
            break
            
    return current, final_cable_size, breaker_size, material_name, phase_num, volt_text, cores

def on_calculate():
    try:
        hp = float(entry_hp.get())
        dist = float(entry_dist.get())
        mat = material_var.get()
        ph = phase_var.get()
        
        if hp < 0 or dist < 0:
            messagebox.showerror(fix_arabic("خطأ"), fix_arabic("الرجاء إدخال أرقام موجبة."))
            return
            
        amps, cable_size, breaker_size, mat_name, ph_num, v_text, cores = calculate_pump_electricals(hp, dist, mat, ph)
        
        line0 = v_text + " " + fix_arabic("فاز") + f" {ph_num} " + fix_arabic("النظام: ")
        line1 = fix_arabic(" أمبير") + f" {amps:.2f} " + fix_arabic("التيار: ")
        line2 = fix_arabic(mat_name) + " " + fix_arabic("القابلو: ")
        
        if cable_size == 0:
            line3 = fix_arabic("كابلات ضخمة") + " " + fix_arabic("الحجم: ")
        else:
            line3 = fix_arabic(" ملم²") + f" {cores}x{cable_size} " + fix_arabic("الحجم: ")
            
        # تم تغيير كلمة الجوزة إلى القاطع هنا
        line4 = fix_arabic(" أمبير") + f" {breaker_size} " + fix_arabic("القاطع: ")
        
        result_text = line0 + "\n" + line1 + "\n" + line2 + "\n" + line3 + "\n" + line4
        label_result.config(text=result_text, fg="#000080")
        
    except ValueError:
        messagebox.showerror(fix_arabic("خطأ إدخال"), fix_arabic("الرجاء إدخال أرقام صحيحة فقط."))

def on_clear():
    entry_hp.delete(0, tk.END)
    entry_dist.delete(0, tk.END)
    phase_var.set("3")
    material_var.set("1")
    label_result.config(text=fix_arabic("النتيجة ستظهر هنا"), fg="gray")

# --- بناء واجهة التطبيق ---
root = tk.Tk()
root.title(fix_arabic("حاسبة القابلو"))
root.geometry("350x680") 
root.configure(bg="#f0f0f0")

font_title = ("Arial", 16, "bold")
font_label = ("Arial", 12)
font_entry = ("Arial", 14)

# تم تغيير العنوان هنا أيضاً
tk.Label(root, text=fix_arabic("تطبيق حساب القابلو والقاطع"), font=font_title, bg="#f0f0f0", pady=15).pack()

tk.Label(root, text=" (HP): " + fix_arabic("القوة الحصانية للمضخة"), font=font_label, bg="#f0f0f0").pack(pady=5)
entry_hp = tk.Entry(root, font=font_entry, justify='center', width=15)
entry_hp.pack(pady=5)

tk.Label(root, text=fix_arabic("المسافة بالأمتار:"), font=font_label, bg="#f0f0f0").pack(pady=5)
entry_dist = tk.Entry(root, font=font_entry, justify='center', width=15)
entry_dist.pack(pady=5)

tk.Label(root, text=fix_arabic("النظام الكهربائي:"), font=font_label, bg="#f0f0f0").pack(pady=5)
phase_var = tk.StringVar(value="3") 
frame_phase = tk.Frame(root, bg="#f0f0f0")
frame_phase.pack()
tk.Radiobutton(frame_phase, text=fix_arabic("3 فاز"), variable=phase_var, value="3", font=font_label, bg="#f0f0f0").pack(side=tk.RIGHT, padx=10)
tk.Radiobutton(frame_phase, text=fix_arabic("1 فاز"), variable=phase_var, value="1", font=font_label, bg="#f0f0f0").pack(side=tk.RIGHT, padx=10)

tk.Label(root, text=fix_arabic("نوع القابلو:"), font=font_label, bg="#f0f0f0").pack(pady=5)
material_var = tk.StringVar(value="1") 
frame_mat = tk.Frame(root, bg="#f0f0f0")
frame_mat.pack()
tk.Radiobutton(frame_mat, text=fix_arabic("نحاس"), variable=material_var, value="1", font=font_label, bg="#f0f0f0").pack(side=tk.RIGHT, padx=10)
tk.Radiobutton(frame_mat, text=fix_arabic("ألمنيوم"), variable=material_var, value="2", font=font_label, bg="#f0f0f0").pack(side=tk.RIGHT, padx=10)

frame_buttons = tk.Frame(root, bg="#f0f0f0")
frame_buttons.pack(pady=20)

btn_calc = tk.Button(frame_buttons, text=fix_arabic("احسب الآن"), font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", command=on_calculate, width=10)
btn_calc.pack(side=tk.RIGHT, padx=5)

btn_clear = tk.Button(frame_buttons, text=fix_arabic("مسح"), font=("Arial", 14, "bold"), bg="#f44336", fg="white", command=on_clear, width=8)
btn_clear.pack(side=tk.RIGHT, padx=5)

label_result = tk.Label(root, text=fix_arabic("النتيجة ستظهر هنا"), font=("Arial", 14, "bold"), bg="#f0f0f0", fg="gray", justify='center')
label_result.pack(pady=10)

# --- التوقيع في أسفل الشاشة ---
footer_label = tk.Label(root, text=fix_arabic("توزيع كهرباء شيخ سعد"), font=("Arial", 11, "bold"), bg="#f0f0f0", fg="#555555")
footer_label.pack(side=tk.BOTTOM, pady=20)

root.mainloop()
import tkinter as tk
from tkinter import messagebox
import arabic_reshaper

# دالة لإصلاح النص العربي فقط
def fix_arabic(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return reshaped_text[::-1]

def calculate_pump_electricals(hp, distance, material, phase):
    if phase == '1':
        current = hp * 4.5
        allowed_vd = 11.0
        vd_factor = 2.0
        phase_num = "1"
        volt_text = "(220V)"
        cores = "2" 
    else:
        current = hp * 1.5
        allowed_vd = 19.0
        vd_factor = 1.732
        phase_num = "3"
        volt_text = "(380V)"
        cores = "3" 
        
    if material == '2':
        rho = 0.0282
        effective_current = current * 1.6 
        material_name = "ألمنيوم"
    else:
        rho = 0.0175
        effective_current = current
        material_name = "نحاس"

    ampacity_sizes = [
        (10, 1.5), (16, 2.5), (25, 4), (32, 6), (40, 10),
        (63, 16), (80, 25), (100, 35), (125, 50), (160, 70), 
        (200, 95), (250, 120), (300, 150), (350, 185), (400, 240)
    ]
    
    size_by_current = 0
    for max_amp, size in ampacity_sizes:
        if effective_current <= max_amp:
            size_by_current = size
            break
            
    area_by_vd = (vd_factor * current * distance * rho * 0.85) / allowed_vd
    required_area = max(size_by_current, area_by_vd)
    
    standard_sizes = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400]
    final_cable_size = 0
    
    for std_size in standard_sizes:
        if std_size >= required_area:
            final_cable_size = std_size
            break
            
    safe_current = current * 1.25
    standard_breakers = [10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 320, 400]
    breaker_size = 0
    
    for b in standard_breakers:
        if b >= safe_current:
            breaker_size = b
            break
            
    return current, final_cable_size, breaker_size, material_name, phase_num, volt_text, cores

def on_calculate():
    try:
        hp = float(entry_hp.get())
        dist = float(entry_dist.get())
        mat = material_var.get()
        ph = phase_var.get()
        
        if hp < 0 or dist < 0:
            messagebox.showerror(fix_arabic("خطأ"), fix_arabic("الرجاء إدخال أرقام موجبة."))
            return
            
        amps, cable_size, breaker_size, mat_name, ph_num, v_text, cores = calculate_pump_electricals(hp, dist, mat, ph)
        
        line0 = v_text + " " + fix_arabic("فاز") + f" {ph_num} " + fix_arabic("النظام: ")
        line1 = fix_arabic(" أمبير") + f" {amps:.2f} " + fix_arabic("التيار: ")
        line2 = fix_arabic(mat_name) + " " + fix_arabic("القابلو: ")
        
        if cable_size == 0:
            line3 = fix_arabic("كابلات ضخمة") + " " + fix_arabic("الحجم: ")
        else:
            line3 = fix_arabic(" ملم²") + f" {cores}x{cable_size} " + fix_arabic("الحجم: ")
            
        # تم تغيير كلمة الجوزة إلى القاطع هنا
        line4 = fix_arabic(" أمبير") + f" {breaker_size} " + fix_arabic("القاطع: ")
        
        result_text = line0 + "\n" + line1 + "\n" + line2 + "\n" + line3 + "\n" + line4
        label_result.config(text=result_text, fg="#000080")
        
    except ValueError:
        messagebox.showerror(fix_arabic("خطأ إدخال"), fix_arabic("الرجاء إدخال أرقام صحيحة فقط."))

def on_clear():
    entry_hp.delete(0, tk.END)
    entry_dist.delete(0, tk.END)
    phase_var.set("3")
    material_var.set("1")
    label_result.config(text=fix_arabic("النتيجة ستظهر هنا"), fg="gray")

# --- بناء واجهة التطبيق ---
root = tk.Tk()
root.title(fix_arabic("حاسبة القابلو"))
root.geometry("350x680") 
root.configure(bg="#f0f0f0")

font_title = ("Arial", 16, "bold")
font_label = ("Arial", 12)
font_entry = ("Arial", 14)

# تم تغيير العنوان هنا أيضاً
tk.Label(root, text=fix_arabic("تطبيق حساب القابلو والقاطع"), font=font_title, bg="#f0f0f0", pady=15).pack()

tk.Label(root, text=" (HP): " + fix_arabic("القوة الحصانية للمضخة"), font=font_label, bg="#f0f0f0").pack(pady=5)
entry_hp = tk.Entry(root, font=font_entry, justify='center', width=15)
entry_hp.pack(pady=5)

tk.Label(root, text=fix_arabic("المسافة بالأمتار:"), font=font_label, bg="#f0f0f0").pack(pady=5)
entry_dist = tk.Entry(root, font=font_entry, justify='center', width=15)
entry_dist.pack(pady=5)

tk.Label(root, text=fix_arabic("النظام الكهربائي:"), font=font_label, bg="#f0f0f0").pack(pady=5)
phase_var = tk.StringVar(value="3") 
frame_phase = tk.Frame(root, bg="#f0f0f0")
frame_phase.pack()
tk.Radiobutton(frame_phase, text=fix_arabic("3 فاز"), variable=phase_var, value="3", font=font_label, bg="#f0f0f0").pack(side=tk.RIGHT, padx=10)
tk.Radiobutton(frame_phase, text=fix_arabic("1 فاز"), variable=phase_var, value="1", font=font_label, bg="#f0f0f0").pack(side=tk.RIGHT, padx=10)

tk.Label(root, text=fix_arabic("نوع القابلو:"), font=font_label, bg="#f0f0f0").pack(pady=5)
material_var = tk.StringVar(value="1") 
frame_mat = tk.Frame(root, bg="#f0f0f0")
frame_mat.pack()
tk.Radiobutton(frame_mat, text=fix_arabic("نحاس"), variable=material_var, value="1", font=font_label, bg="#f0f0f0").pack(side=tk.RIGHT, padx=10)
tk.Radiobutton(frame_mat, text=fix_arabic("ألمنيوم"), variable=material_var, value="2", font=font_label, bg="#f0f0f0").pack(side=tk.RIGHT, padx=10)

frame_buttons = tk.Frame(root, bg="#f0f0f0")
frame_buttons.pack(pady=20)

btn_calc = tk.Button(frame_buttons, text=fix_arabic("احسب الآن"), font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", command=on_calculate, width=10)
btn_calc.pack(side=tk.RIGHT, padx=5)

btn_clear = tk.Button(frame_buttons, text=fix_arabic("مسح"), font=("Arial", 14, "bold"), bg="#f44336", fg="white", command=on_clear, width=8)
btn_clear.pack(side=tk.RIGHT, padx=5)

label_result = tk.Label(root, text=fix_arabic("النتيجة ستظهر هنا"), font=("Arial", 14, "bold"), bg="#f0f0f0", fg="gray", justify='center')
label_result.pack(pady=10)

# --- التوقيع في أسفل الشاشة ---
footer_label = tk.Label(root, text=fix_arabic("توزيع كهرباء شيخ سعد"), font=("Arial", 11, "bold"), bg="#f0f0f0", fg="#555555")
footer_label.pack(side=tk.BOTTOM, pady=20)

root.mainloop()
