import tkinter as tk


class RegionSelector:
    def __init__(self, theme="dark"):
        self.start_x = None
        self.start_y = None
        self.region = None
        self.cancelled = False
        self.theme = theme

    def create_overlay(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.25)
        self.root.configure(bg='#0A0A0A' if self.theme == "dark" else '#F3F4F6')
        self.root.attributes('-topmost', True)

        self.canvas = tk.Canvas(
            self.root,
            cursor="crosshair",
            bg="#0A0A0A" if self.theme == "dark" else "#F3F4F6",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        screen_width = self.root.winfo_screenwidth()
        bg_width, bg_height = 480, 60
        bg_x, bg_y = (screen_width - bg_width) // 2, 30
        self.canvas.create_rectangle(bg_x, bg_y, bg_x + bg_width, bg_y + bg_height, fill="#F5E8C7" if self.theme == "light" else "#2A2A2A", outline="")
        self.canvas.create_rectangle(bg_x, bg_y, bg_x + bg_width, bg_y + 3, fill="#4CAF50" if self.theme == "light" else "#81C784", outline="")
        self.canvas.create_text(screen_width // 2, bg_y + 30, text="Drag to select text region  •  ESC to cancel", font=("Segoe UI", 16, "bold"), fill="#2E7D32" if self.theme == "light" else "#E8F5E9")

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Escape>", self.cancel_selection)

    def on_button_press(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root
        
        self.selection_box_outer = self.canvas.create_rectangle(
            event.x, event.y, event.x, event.y,
            outline='#4CAF50' if self.theme == "light" else '#81C784',
            width=2,
            dash=(4, 4)
        )
        
        self.selection_box_inner = self.canvas.create_rectangle(
            event.x + 2, event.y + 2, event.x + 2, event.y + 2,
            outline='#4CAF50' if self.theme == "light" else '#81C784',
            width=2,
            dash=(4, 4)
        )

    def on_move_press(self, event):
        x1 = self.start_x - self.root.winfo_rootx()
        y1 = self.start_y - self.root.winfo_rooty()
        
        self.canvas.coords(self.selection_box_outer, x1, y1, event.x, event.y)
        self.canvas.coords(self.selection_box_inner, x1 + 2, y1 + 2, event.x - 2, event.y - 2)

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