import tkinter as tk


class RegionSelector:
    def __init__(self, theme="dark"):
        self.start_x = None
        self.start_y = None
        self.region = None
        self.cancelled = False
        self.theme = theme
        self.selection_box_outer = None
        self.selection_box_inner = None

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
        screen_height = self.root.winfo_screenheight()
        
        bg_width, bg_height = screen_width, 90
        bg_x, bg_y = 0, 0
        
        self.canvas.create_rectangle(bg_x, bg_y, bg_x + bg_width, bg_y + bg_height, 
                                    fill="#68EDFF" if self.theme == "light" else "#2A2A2A", outline="")
        self.canvas.create_rectangle(bg_x, bg_y, bg_x + bg_width, bg_y + 3, 
                                    fill="#77F17B" if self.theme == "light" else "#81C784", outline="")
        self.canvas.create_text(screen_width // 2, bg_y + 30, 
                               text="Drag to select text region  •  ESC to cancel", 
                               font=("Segoe UI", 16, "bold"), 
                               fill="#2E7D32" if self.theme == "light" else "#E8F5E9")

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Escape>", self.cancel_selection)

    def on_button_press(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root
        
        self.selection_box_outer = self.canvas.create_rectangle(
            event.x, event.y, event.x, event.y,
            outline="#FFFFFF" if self.theme == "light" else "#FFFFFF",
            width=2,
            dash=(6, 3)
        )
        
        self.selection_box_inner = self.canvas.create_rectangle(
            event.x + 3, event.y + 3, event.x + 3, event.y + 3,
            outline='#1976D2' if self.theme == "light" else '#FFFFFF',
            width=1,
            dash=(6, 3)
        )

    def on_move_press(self, event):
        if self.start_x is None or self.start_y is None:
            return
            
        x1 = self.start_x - self.root.winfo_rootx()
        y1 = self.start_y - self.root.winfo_rooty()
        
        if self.selection_box_outer:
            self.canvas.coords(self.selection_box_outer, x1, y1, event.x, event.y)
        
        if self.selection_box_inner:
            self.canvas.coords(self.selection_box_inner, x1 + 3, y1 + 3, event.x - 3, event.y - 3)

    def on_button_release(self, event):
        if self.start_x is None or self.start_y is None:
            return
            
        x1 = self.start_x - self.root.winfo_rootx()
        y1 = self.start_y - self.root.winfo_rooty()
        x2 = event.x
        y2 = event.y
        
        if abs(x2 - x1) < 20 or abs(y2 - y1) < 20:
            return
        
        x_min = min(x1, x2)
        y_min = min(y1, y2)
        x_max = max(x1, x2)
        y_max = max(y1, y2)
        
        screen_x = self.root.winfo_rootx() + x_min
        screen_y = self.root.winfo_rooty() + y_min
        width = x_max - x_min
        height = y_max - y_min
        
        self.region = (screen_x, screen_y, width, height)
        self.root.quit()
        self.root.destroy()

    def cancel_selection(self, event=None):
        self.cancelled = True
        self.region = None
        self.root.quit()
        self.root.destroy()

    def get_region(self):
        self.create_overlay()
        self.root.mainloop()
        return self.region