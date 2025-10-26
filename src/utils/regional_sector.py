import tkinter as tk
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
            text="🖱️ Drag to select region • ESC to cancel",
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
