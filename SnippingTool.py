from tkinter import *
import pyautogui

class SnippingTool:
    def __init__(self):
        self.master = Tk()
        self.start_x, self.start_y = None, None
        self.current_x, self.current_y = None, None

        self.master.withdraw()
        self.master_screen = Toplevel(self.master)
        self.configure_master_screen()

        self.picture_frame = Frame(self.master_screen, background="maroon3")
        self.picture_frame.pack(fill=BOTH, expand=YES)

        self.snip_surface = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.snip_surface.pack(fill=BOTH, expand=YES)

        self.snip_surface.bind("<ButtonPress-1>", self.on_button_press)
        self.snip_surface.bind("<B1-Motion>", self.on_snip_drag)
        self.snip_surface.bind("<ButtonRelease-1>", self.on_button_release)

        self.master.mainloop()

    def configure_master_screen(self):
        self.master_screen.attributes("-transparent", "maroon3")
        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', 0.3)
        self.master_screen.attributes("-topmost", True)
        self.master_screen.deiconify()
        self.master_screen.lift()

    def on_button_press(self, event):
        self.start_x, self.start_y = self.snip_surface.canvasx(event.x), self.snip_surface.canvasy(event.y)
        self.snip_surface.create_rectangle(0, 0, 1, 1, outline='red', width=3, fill="maroon3")

    def on_snip_drag(self, event):
        self.current_x, self.current_y = event.x, event.y
        self.snip_surface.coords(1, self.start_x, self.start_y, self.current_x, self.current_y)

    def on_button_release(self, event):
        try:
            x1, x2 = min(self.start_x, self.current_x) + 2, max(self.start_x, self.current_x) - 2
            y1, y2 = min(self.start_y, self.current_y) + 2, max(self.start_y, self.current_y) - 2
            width, height = x2 - x1, y2 - y1
            self.image = pyautogui.screenshot(region=(x1, y1, width, height))
            self.master.quit()
        except Exception:
            pass
    
    def destroy(self):
        self.master.destroy()