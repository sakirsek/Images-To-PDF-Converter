import tkinter as tk
from tkinter.filedialog import asksaveasfile
from PIL import Image, ImageTk
from fpdf import FPDF
import tempfile
from SnippingTool import SnippingTool

class ImagesToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.objects = []
        self.pdf = FPDF()
        self.create_ui()

    def create_ui(self):
        self.root.title("Images To PDF")
        self.root.geometry(self.starting_position(230, 305))
        self.root.attributes('-topmost', True)
        self.root.attributes('-toolwindow', True)

        self.listbox_frame = tk.Frame(self.root)
        self.listbox_frame.grid(row=0, column=0, sticky="nsew")

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.grid(row=1, column=0, sticky="nsew")

        self.listbox = tk.Listbox(self.listbox_frame)
        self.listbox.grid(row=0, column=0, sticky="nsew")
        self.listbox.bind("<Double-Button-1>", self.on_item_click)

        scrollbar = tk.Scrollbar(self.listbox_frame, orient="vertical")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=scrollbar.set)

        add_button = tk.Button(self.buttons_frame, text="+", width=5, bg='green', fg='white', command=self.add_image)
        add_button.grid(row=0, column=0, sticky="nsew")

        remove_button = tk.Button(self.buttons_frame, text="-", width=5, bg='red', fg='white', command=self.remove_image)
        remove_button.grid(row=0, column=1, sticky="nsew")

        create_button = tk.Button(self.buttons_frame, text="Create PDF", width=10, bg='blue', fg='white', command=self.create_pdf)
        create_button.grid(row=0, column=2, sticky="nsew")

    def add_image(self):
        try:
            self.root.withdraw()
            new_object = SnippingTool()
            self.objects.append(new_object.image)
            new_object.destroy()
            self.listbox.insert(tk.END, f"Image {self.listbox.size() + 1}")
            self.listbox.yview("end")
            self.root.deiconify()
        except Exception as e:
            tk.messagebox.showinfo("Error", str(e))

    def remove_image(self):
        selected_item = self.listbox.curselection()
        if selected_item:
            index = selected_item[0]
            self.listbox.delete(index)
            del self.objects[index]

    def create_pdf(self):
        if self.listbox.size() > 0:
            try:
                for item in self.objects:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                        self.pdf.add_page()
                        item.save(temp_file.name, format='PNG')
                        self.pdf.image(temp_file.name, x=5, y=5, w=200)

                filename = self.save_dialog()
                message = "PDF File Created!"
                if filename:
                    self.pdf.output(filename)
                    self.clear_data()
                else:
                    message = "File Name Missing!"
            except Exception as e:
                tk.messagebox.showinfo("Error", str(e))
        else:
            message = "Please Add An Item First."
        tk.messagebox.showinfo("Information", message)

    def clear_data(self):
        self.objects = []
        self.pdf = FPDF()
        self.listbox.delete(0, tk.END)
    
    def on_item_click(self, event):
        try:
            selected_item = self.listbox.curselection()[0]
            image = Image.frombytes("RGB", self.objects[selected_item].size, self.objects[selected_item].tobytes())
            image_window = tk.Toplevel(self.root)
            image_window.title(f"Image {selected_item + 1}")
            canvas = tk.Canvas(image_window, width=image.width, height=image.height)
            canvas.grid(row=0, column=0)
            photo = ImageTk.PhotoImage(image)
            canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            image_window.mainloop()
        except Exception as e:
            tk.messagebox.showinfo("Error", str(e))

    @staticmethod
    def save_dialog():
        try:
            filename = asksaveasfile(filetypes=[("PDF", "*.pdf")], defaultextension=[("PDF", "*.pdf")]).name
        except Exception:
            filename = ''
        return filename

    @staticmethod
    def starting_position(width, height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        start_x = screen_width - width - 50
        start_y = (screen_height - height) // 2
        return f"{width}x{height}+{start_x}+{start_y}"

if __name__ == "__main__":
    root = tk.Tk()
    app = ImagesToPDFConverter(root)
    root.mainloop()
