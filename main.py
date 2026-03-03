import flet as ft

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

def main(page: ft.Page):
    page.title = "حاسبة القابلو"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True 
    page.window_width = 400
    page.window_height = 700
    page.scroll = "auto"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    title_text = ft.Text("تطبيق حساب القابلو والقاطع", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900)

    entry_hp = ft.TextField(label="القوة الحصانية للمضخة (HP)", keyboard_type=ft.KeyboardType.NUMBER, text_align=ft.TextAlign.CENTER)
    entry_dist = ft.TextField(label="المسافة بالأمتار", keyboard_type=ft.KeyboardType.NUMBER, text_align=ft.TextAlign.CENTER)

    phase_var = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="3", label="3 فاز"),
            ft.Radio(value="1", label="1 فاز")
        ], alignment=ft.MainAxisAlignment.CENTER),
        value="3"
    )

    material_var = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="1", label="نحاس"),
            ft.Radio(value="2", label="ألمنيوم")
        ], alignment=ft.MainAxisAlignment.CENTER),
        value="1"
    )

    label_result = ft.Text("النتيجة ستظهر هنا", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_700, text_align=ft.TextAlign.CENTER)

    def on_calculate(e):
        try:
            hp = float(entry_hp.value)
            dist = float(entry_dist.value)
            mat = material_var.value
            ph = phase_var.value
            
            if hp < 0 or dist < 0:
                page.snack_bar = ft.SnackBar(ft.Text("الرجاء إدخال أرقام موجبة."), bgcolor=ft.colors.RED)
                page.snack_bar.open = True
                page.update()
                return
                
            amps, cable_size, breaker_size, mat_name, ph_num, v_text, cores = calculate_pump_electricals(hp, dist, mat, ph)
            
            line0 = f"النظام: {ph_num} فاز {v_text}"
            line1 = f"التيار: {amps:.2f} أمبير"
            line2 = f"القابلو: {mat_name}"
            
            if cable_size == 0:
                line3 = "الحجم: كابلات ضخمة"
            else:
                line3 = f"الحجم: {cores}x{cable_size} ملم²"
                
            line4 = f"القاطع: {breaker_size} أمبير"
            
            label_result.value = f"{line0}\n{line1}\n{line2}\n{line3}\n{line4}"
            label_result.color = ft.colors.GREEN_800
            page.update()
            
        except (ValueError, TypeError):
            page.snack_bar = ft.SnackBar(ft.Text("الرجاء إدخال أرقام صحيحة فقط!"), bgcolor=ft.colors.RED)
            page.snack_bar.open = True
            page.update()

    def on_clear(e):
        entry_hp.value = ""
        entry_dist.value = ""
        phase_var.value = "3"
        material_var.value = "1"
        label_result.value = "النتيجة ستظهر هنا"
        label_result.color = ft.colors.GREY_700
        page.update()

    btn_calc = ft.ElevatedButton("احسب الآن", on_click=on_calculate, bgcolor=ft.colors.GREEN, color=ft.colors.WHITE, width=150)
    btn_clear = ft.ElevatedButton("مسح", on_click=on_clear, bgcolor=ft.colors.RED, color=ft.colors.WHITE, width=150)

    footer_label = ft.Text("توزيع كهرباء شيخ سعد", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_500)

    page.add(
        ft.Container(height=20),
        title_text,
        ft.Divider(),
        entry_hp,
        entry_dist,
        ft.Text("النظام الكهربائي:", weight=ft.FontWeight.BOLD),
        phase_var,
        ft.Text("نوع القابلو:", weight=ft.FontWeight.BOLD),
        material_var,
        ft.Container(height=10),
        ft.Row([btn_calc, btn_clear], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(height=20),
        ft.Card(
            content=ft.Container(content=label_result, padding=20),
            elevation=5
        ),
        ft.Container(height=40), 
        footer_label
    )

ft.app(target=main)
