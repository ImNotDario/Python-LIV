import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, UnidentifiedImageError
import os
import time

class LiveImageLoader:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Image Loader")
        
        self.create_menu()
        
        self.image_label = tk.Label(self.root)
        self.image_label.grid(row=0, column=0, sticky="nsew")

        self.status_label = tk.Label(self.root, text="", bg="white")
        self.status_label.grid(row=1, column=0, sticky="ew")

        self.image_path = None
        self.loaded_image = None

        self.load_image()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Window menu
        window_menu = tk.Menu(menubar, tearoff=0)
        self.on_top_var = tk.BooleanVar()
        window_menu.add_checkbutton(label="On Top", variable=self.on_top_var, command=self.toggle_on_top)
        menubar.add_cascade(label="Window", menu=window_menu)
        
        self.root.config(menu=menubar)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:
            self.image_path = file_path
            self.load_image()

    def load_image(self):
        if self.image_path:
            try:
                image = Image.open(self.image_path)
                self.loaded_image = ImageTk.PhotoImage(image)
                self.image_label.config(image=self.loaded_image)
                self.status_label.config(text="Image last updated: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                self.root.update_idletasks()  # Update window size
                self.root.after(1000, self.load_image)  # Update image every second
                # Adjust window geometry to accommodate both image and label
                width = max(image.width, self.status_label.winfo_reqwidth())
                height = image.height + self.status_label.winfo_reqheight()
                self.root.geometry(f"{width}x{height}")
            except UnidentifiedImageError as e:
                print("Error loading image:", e)
                self.root.after(1000, self.load_image)  # Continue loading next image

    def toggle_on_top(self):
        if self.on_top_var.get():
            self.root.attributes("-topmost", True)
        else:
            self.root.attributes("-topmost", False)

if __name__ == "__main__":
    root = tk.Tk()
    app = LiveImageLoader(root)
    root.mainloop()
