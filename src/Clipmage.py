import os
import sys
import threading
import time
import tkinter as tk
from pathlib import Path

import keyboard
import pyautogui
import pyperclip
import pytesseract

from utils.regional_sector import RegionSelector


class OCRApp:
    def __init__(self):
        self.is_running = True
        self.capture_count = 0
        self.theme = "dark"
        self.setup_tesseract()


    def setup_tesseract(self):
        try:
            appdata_tesseract = os.path.join(os.getenv('LOCALAPPDATA'), 'Clipmage', 'tesseract')
            tesseract_exe = os.path.join(appdata_tesseract, 'tesseract.exe')
            
            if os.path.exists(tesseract_exe):
                try:
                    pytesseract.pytesseract.tesseract_cmd = tesseract_exe
                    pytesseract.get_tesseract_version()
                    return True
                except:
                    import shutil
                    shutil.rmtree(appdata_tesseract, ignore_errors=True)
            
            if getattr(sys, 'frozen', False):
                if hasattr(sys, '_MEIPASS'):
                    source = os.path.join(sys._MEIPASS, 'resources', 'tesseract_portable')
                else:
                    source = os.path.join(os.path.dirname(sys.executable), 'resources', 'tesseract_portable')
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
                source = os.path.join(os.path.dirname(base_path), 'resources', 'tesseract_portable')
            
            if not os.path.exists(source):
                raise FileNotFoundError(f"Tesseract no encontrado en: {source}")
            
            import shutil
            os.makedirs(os.path.dirname(appdata_tesseract), exist_ok=True)
            
            self.custom_toast("Configuración inicial", "Instalando OCR... (solo primera vez)", 3000, toast_type="info")
            shutil.copytree(source, appdata_tesseract, dirs_exist_ok=True)
            
            if not os.path.exists(tesseract_exe):
                raise FileNotFoundError(f"Error copiando tesseract.exe")
            
            pytesseract.pytesseract.tesseract_cmd = tesseract_exe
            version = pytesseract.get_tesseract_version()
            return True
        
        except Exception as e:
            self.custom_toast("Critical Error", f"Tesseract error: {str(e)[:30]}", 5000, toast_type="error")
            return False

    def custom_toast(self, title, message, duration=2000, toast_type="info"):
        def show():
            toast = tk.Tk()
            toast.overrideredirect(True)
            toast.attributes("-topmost", True)
            toast.attributes("-alpha", 0.0)
            toast.configure(bg="#F5E8C7" if self.theme == "light" else "#363636", highlightthickness=0)

            screen_width = toast.winfo_screenwidth()
            screen_height = toast.winfo_screenheight()

            width, height = 380, 110
            x = screen_width - width - 24
            y = screen_height - height - 70

            toast.geometry(f"{width}x{height}+{x}+{y}")

            canvas = tk.Canvas(toast, bg="#F5E8C7" if self.theme == "light" else "#2A2A2A", highlightthickness=0)
            canvas.pack(fill="both", expand=True)
            schemes_light = {
                "success": {"bg": "#E6F3E6", "accent": "#4CAF50", "title": "#2E7D32", "message": "#4CAF50", "icon": "✓"},
                "error": {"bg": "#FBE9E7", "accent": "#F44336", "title": "#D32F2F", "message": "#F44336", "icon": "✕"},
                "warning": {"bg": "#FFF3E0", "accent": "#FF9800", "title": "#F57C00", "message": "#FF9800", "icon": "⚠"},
                "info": {"bg": "#E8EAF6", "accent": "#3F51B5", "title": "#283593", "message": "#3F51B5", "icon": "ℹ"},
                "neutral": {"bg": "#F5F5F5", "accent": "#757575", "title": "#424242", "message": "#757575", "icon": "●"}
            }

            schemes_dark = {
                "success": {"bg": "#F5F5F5", "accent": "#5DF065", "title": "#000000", "message": "#656870", "icon": "✓"},
                "error": {"bg": "#5E1B1B", "accent": "#EF9A9A", "title": "#FCE4EC", "message": "#EF9A9A", "icon": "✕"},
                "warning": {"bg": "#5E3F1B", "accent": "#FFB74D", "title": "#FFF3E0", "message": "#FFB74D", "icon": "⚠"},
                "info": {"bg": "#1B2E5E", "accent": "#90CAF9", "title": "#E3F2FD", "message": "#90CAF9", "icon": "ℹ"},
                "neutral": {"bg": "#424242", "accent": "#B0BEC5", "title": "#ECEFF1", "message": "#B0BEC5", "icon": "●"}
            }

            schemes = schemes_light if self.theme == "light" else schemes_dark
            scheme = schemes.get(toast_type, schemes["neutral"])

            radius = 20
            canvas.create_oval(0, 0, radius * 2, radius * 2, fill=scheme["bg"], outline="")
            canvas.create_oval(width - radius * 2, 0, width, radius * 2, fill=scheme["bg"], outline="")
            canvas.create_oval(0, height - radius * 2, radius * 2, height, fill=scheme["bg"], outline="")
            canvas.create_oval(width - radius * 2, height - radius * 2, width, height, fill=scheme["bg"], outline="")
            canvas.create_rectangle(radius, 0, width - radius, height, fill=scheme["bg"], outline="")
            canvas.create_rectangle(0, radius, width, height - radius, fill=scheme["bg"], outline="")

            canvas.create_rectangle(0, 0, 6, height, fill=scheme["accent"], outline="")

            icon_x, icon_y = 32, 55
            canvas.create_text(icon_x, icon_y, text=scheme["icon"], font=("Segoe UI", 18, "bold"), fill=scheme["bg"])

            canvas.create_text(70, 38, anchor="w", text=title, font=("Segoe UI", 13, "bold"), fill=scheme["title"])

            message_lines = self._wrap_text(message, 38)
            y_offset = 58
            for line in message_lines[:2]:
                canvas.create_text(70, y_offset, anchor="w", text=line, font=("Segoe UI", 10), fill=scheme["message"])
                y_offset += 18
            def fade_in():
                alpha = 0.0
                while alpha < 0.98:
                    alpha += 0.08
                    toast.attributes("-alpha", alpha)
                    toast.update()
                    time.sleep(0.02)

            def fade_out():
                alpha = 0.98
                while alpha > 0:
                    alpha -= 0.12
                    toast.attributes("-alpha", alpha)
                    toast.update()
                    time.sleep(0.015)
                toast.destroy()

            fade_in()
            toast.after(duration, fade_out)
            toast.mainloop()

        threading.Thread(target=show, daemon=True).start()

    def _wrap_text(self, text, max_chars):
        """Divide el texto en líneas"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 <= max_chars:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)

        if current_line:
            lines.append(" ".join(current_line))

        return lines

    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.custom_toast("Theme Changed", f"Switched to {self.theme.capitalize()} theme", toast_type="info")

    def capture_and_extract_text(self):
        if not self.is_running:
            return

        try:
            try:
                import ctypes
                from ctypes import wintypes
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except:
                try:
                    ctypes.windll.user32.SetProcessDPIAware()
                except:
                    pass

            selector = RegionSelector(theme=self.theme)
            region = selector.get_region()
            time.sleep(0.1)

            if region is None:
                return

            x, y, width, height = region

            if width < 10 or height < 10:
                self.custom_toast("Region Too Small", "Please select a larger area to capture text", toast_type="warning")
                return
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            custom_config = r'--oem 3 --psm 6 -l eng+spa'
            text = pytesseract.image_to_string(screenshot, config=custom_config).strip()

            if text:
                pyperclip.copy(text)
                self.capture_count += 1
                preview = text[:45] + "..." if len(text) > 45 else text
                preview = preview.replace('\n', ' ')

                self.custom_toast("Text Copied Successfully", f"Captured: {preview}", toast_type="success")
            else:
                self.custom_toast("No Text Detected", "The selected region contains no readable text", toast_type="warning")

        except pytesseract.TesseractNotFoundError:
            self.custom_toast("Tesseract Error", "OCR engine not found or is damaged", toast_type="error")
        except Exception as e:
            self.custom_toast("Capture Failed", f"An error occurred: {str(e)[:35]}", toast_type="error")

    def toggle_status(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.custom_toast("OCR Activated", f"Ready to capture • Total: {self.capture_count} captures", toast_type="success")
        else:
            self.custom_toast("OCR Paused", f"Press Ctrl+Alt+P to resume • Total: {self.capture_count}", toast_type="warning")

    def show_help(self):
        help_text = "Ctrl+Alt+S: Capture • P: Pause • H: Help • T: Toggle Theme • I: Info • W: Exit"
        self.custom_toast("Keyboard Shortcuts", help_text, 4000, toast_type="info")

    def show_info(self):
        try:
            version = pytesseract.get_tesseract_version()
            info_text = f"Engine v{version} • {self.capture_count} captures • {'Active' if self.is_running else 'Paused'} • Theme: {self.theme.capitalize()}"
        except:
            info_text = f"Engine status: Unknown • {self.capture_count} captures • Theme: {self.theme.capitalize()}"

        self.custom_toast("System Information", info_text, 3000, toast_type="info")

    def quit_app(self):
        self.custom_toast("Session Ended", f"Successfully captured {self.capture_count} texts", 1000, toast_type="neutral")
        time.sleep(2.5)
        keyboard.unhook_all()
        sys.exit()

    def run(self):
        try:
            keyboard.add_hotkey('ctrl+alt+s', self.capture_and_extract_text)
            keyboard.add_hotkey('ctrl+alt+p', self.toggle_status)
            keyboard.add_hotkey('ctrl+alt+h', self.show_help)
            keyboard.add_hotkey('ctrl+alt+t', self.toggle_theme)
            keyboard.add_hotkey('ctrl+alt+i', self.show_info)
            keyboard.add_hotkey('ctrl+alt+w', self.quit_app)

            try:
                version = pytesseract.get_tesseract_version()
                self.custom_toast("OCR Ready", f"Tesseract v{version} initialized • Press Ctrl+Alt+H for shortcuts", toast_type="success")
            except:
                self.custom_toast("OCR Started", "Press Ctrl+Alt+H for help • Ctrl+Alt+I for system info", toast_type="info")

            keyboard.wait()

        except KeyboardInterrupt:
            self.quit_app()
        except Exception as e:
            self.custom_toast("Fatal Error", f"Application failed to start: {str(e)[:30]}", toast_type="error")
            time.sleep(3)
            sys.exit(1)


if __name__ == "__main__":
    try:
        app = OCRApp()
        app.run()
    except Exception as e:
        input("Press Enter to close...")
        sys.exit(1)