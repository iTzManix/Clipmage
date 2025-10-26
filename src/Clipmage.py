import os
import sys
import threading
import time
import tkinter as tk

import keyboard
import pyautogui
import pyperclip
import pytesseract

from utils.regional_sector import RegionSelector


class OCRApp:
    def __init__(self):
        self.is_running = True
        self.capture_count = 0
        self.setup_tesseract()

    def setup_tesseract(self):
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))

            tesseract_path = os.path.join(base_path, '..', 'resources', 'tesseract_portable', 'tesseract.exe')

            if os.path.exists(tesseract_path):
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
                print(f"✅ Portable Tesseract found: {tesseract_path}")
                return True
            else:
                install_path = os.path.join(os.path.dirname(sys.executable), 'tesseract_portable', 'tesseract.exe')
                if os.path.exists(install_path):
                    pytesseract.pytesseract.tesseract_cmd = install_path
                    print(f"✅ Tesseract found in installation: {install_path}")
                    return True

                system_paths = [
                    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                    'tesseract'
                ]
                for path in system_paths:
                    try:
                        pytesseract.pytesseract.tesseract_cmd = path
                        pytesseract.get_tesseract_version()
                        print(f"✅ System Tesseract found: {path}")
                        return True
                    except:
                        continue

                raise Exception("Tesseract not found")

        except Exception as e:
            print(f"❌ Error configuring Tesseract: {e}")
            self.custom_toast("❌ Critical Error", "Tesseract OCR not found", 5000)
            return False

    def custom_toast(self, title, message, duration=2000):
        def show():
            toast = tk.Tk()
            toast.overrideredirect(True)
            toast.attributes("-topmost", True)
            toast.configure(bg="#000000", highlightthickness=0)

            screen_width = toast.winfo_screenwidth()

            width, height = 320, 100
            x = screen_width - width - 20
            y = 50

            toast.geometry(f"{width}x{height}+{x}+{y}")

            canvas = tk.Canvas(toast, bg="#000000", highlightthickness=0)
            canvas.pack(fill="both", expand=True)

            radius = 20
            canvas.create_rectangle(0, 0, width, height, fill="#333333", outline="#333333", width=0)
            canvas.create_oval(0, 0, 2 * radius, 2 * radius, fill="#333333", outline="#333333")
            canvas.create_oval(width - 2 * radius, 0, width, 2 * radius, fill="#333333", outline="#333333")

            canvas.create_text(20, 30, anchor="w", text=title, font=("Segoe UI", 12, "bold"), fill="white")
            canvas.create_text(20, 60, anchor="w", text=message, font=("Segoe UI", 10), fill="white")

            toast.after(duration, toast.destroy)
            toast.mainloop()

        threading.Thread(target=show, daemon=True).start()

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

            selector = RegionSelector()
            region = selector.get_region()

            if region is None:
                return

            x, y, width, height = region

            if width < 10 or height < 10:
                self.custom_toast("⚠️ Region too small", "Please select a larger region")
                return

            print(f"🎯 Capturing region: x={x}, y={y}, w={width}, h={height}")

            screenshot = pyautogui.screenshot(region=(x, y, width, height))

            custom_config = r'--oem 3 --psm 6 -l eng+spa'

            text = pytesseract.image_to_string(screenshot, config=custom_config).strip()

            if text:
                pyperclip.copy(text)
                self.capture_count += 1
                preview = text[:50] + "..." if len(text) > 50 else text
                preview = preview.replace('\n', ' ')

                self.custom_toast("✅ Text copied", f"# Preview: {preview}")
            else:
                self.custom_toast("⚠️ No text", "No readable text detected in region")

        except pytesseract.TesseractNotFoundError:
            self.custom_toast("❌ Error Tesseract", "Motor OCR not found or damaged")
        except Exception as e:
            print(f"Error detallado: {e}")
            self.custom_toast("❌ Error", f"Error capturing: {str(e)[:30]}...")

    def toggle_status(self):
        self.is_running = not self.is_running
        status = "🟢 Active" if self.is_running else "🟡 Paused"
        self.custom_toast("OCR Status", f"{status} - Captures: {self.capture_count}")

    def show_help(self):
        help_text = """Ctrl+Alt+S: Capture text
Ctrl+Alt+P: Pause/Resume
Ctrl+Alt+H: Help
Ctrl+Alt+W: Exit"""
        self.custom_toast("🔧 OCR Controls", help_text, 4000)

    def show_info(self):
        try:
            version = pytesseract.get_tesseract_version()
            info_text = f"""Tesseract: v{version}
Captures: {self.capture_count}
Status: {'🟢 Active' if self.is_running else '🟡 Paused'}"""
        except:
            info_text = f"""Tesseract: ⚠️ Error
Captures: {self.capture_count}
Status: {'🟢 Active' if self.is_running else '🟡 Paused'}"""

        self.custom_toast("ℹ️ System Info", info_text, 3000)

    def quit_app(self):
        self.custom_toast("👋 OCR Finished", f"Total captures: {self.capture_count}", 1500)
        time.sleep(2)
        keyboard.unhook_all()
        sys.exit()

    def run(self):
        try:
            keyboard.add_hotkey('ctrl+alt+s', self.capture_and_extract_text)
            keyboard.add_hotkey('ctrl+alt+p', self.toggle_status)
            keyboard.add_hotkey('ctrl+alt+h', self.show_help)
            keyboard.add_hotkey('ctrl+alt+i', self.show_info)
            keyboard.add_hotkey('ctrl+alt+w', self.quit_app)

            try:
                version = pytesseract.get_tesseract_version()
                self.custom_toast("🚀 OCR Started", f"Tesseract v{version} • Ctrl+Alt+H for help")
            except:
                self.custom_toast("🚀 OCR Started", "Ctrl+Alt+H for help • Ctrl+Alt+I for info")

            keyboard.wait()

        except KeyboardInterrupt:
            self.quit_app()
        except Exception as e:
            self.custom_toast("❌ Fatal Error", f"Error starting: {str(e)[:30]}...")
            time.sleep(3)
            sys.exit(1)

class RegionSelector:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.region = None
        self.cancelled = False

    def create_overlay(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.configure(bg='black')
        self.root.attributes('-topmost', True)

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.create_text(
            self.root.winfo_screenwidth()//2, 40,
            text="🖱️ Drag to select region  •  ESC to cancel",
            font=("Segoe UI", 16, "bold"), fill="white"
        )

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Escape>", self.cancel_selection)

    def on_button_press(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.selection_box = self.canvas.create_rectangle(
            event.x, event.y, event.x, event.y,
            outline='#00FF00', width=3, dash=(5, 5)
        )

    def on_move_press(self, event):
        self.canvas.coords(
            self.selection_box,
            self.start_x - self.root.winfo_rootx(),
            self.start_y - self.root.winfo_rooty(),
            event.x, event.y
        )

    def on_button_release(self, event):
        if self.cancelled:
            return

        end_x = event.x_root
        end_y = event.y_root

        x1, y1 = self.start_x, self.start_y
        x2, y2 = end_x, end_y

        if abs(x2 - x1) < 20 or abs(y2 - y1) < 20:
            self.cancelled = True
            self.root.quit()
            return

        x = min(x1, x2)
        y = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)

        self.region = (x, y, width, height)
        self.root.quit()

    def cancel_selection(self, event=None):
        self.cancelled = True
        self.root.quit()

    def get_region(self):
        self.create_overlay()
        self.root.mainloop()
        self.root.destroy()
        return None if self.cancelled else self.region

if __name__ == "__main__":
    try:
        app = OCRApp()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        input("Press Enter to close...")
        sys.exit(1)        
        print(f"Fatal error: {e}")
        input("Press Enter to close...")
        sys.exit(1)