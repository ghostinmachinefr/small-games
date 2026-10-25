# customizer.py
import tkinter as tk
from tkinter import colorchooser
import settings

def pick_color(target, label_widget):
    color = colorchooser.askcolor()[0]
    if color:
        r, g, b = int(color[0]), int(color[1]), int(color[2])
        setattr(settings, target, (r, g, b))
        label_widget.config(bg='#%02x%02x%02x' % (r, g, b))

def run_customizer():
    root = tk.Tk()
    root.title("Customise Your Bird")
    root.resizable(False, False)

    tk.Label(root, text="Flappy Bird Customizer",
             font=("Arial", 16, "bold")).pack(pady=10)

    def color_row(label_text, setting_key):
        frame = tk.Frame(root)
        frame.pack(pady=4, padx=20, fill="x")
        tk.Label(frame, text=label_text, width=18, anchor="w").pack(side="left")
        r, g, b = getattr(settings, setting_key)
        swatch = tk.Label(frame, bg='#%02x%02x%02x' % (r, g, b),
                          width=4, relief="solid")
        swatch.pack(side="left", padx=6)
        tk.Button(frame, text="Pick",
                  command=lambda k=setting_key, s=swatch: pick_color(k, s)
                  ).pack(side="left")

    color_row("Bird colour", "bird_color")
    color_row("Sky colour", "bg_color")
    color_row("Ground colour", "ground_color")
    color_row("Pipe colour", "pipe_color")

    # Bird shape
    shape_frame = tk.Frame(root)
    shape_frame.pack(pady=8)
    tk.Label(shape_frame, text="Bird shape:").pack(side="left")
    shape_var = tk.StringVar(value=settings.bird_shape)
    for s in ("round", "square"):
        tk.Radiobutton(shape_frame, text=s.capitalize(),
                       variable=shape_var, value=s,
                       command=lambda: setattr(settings, "bird_shape",
                                               shape_var.get())
                       ).pack(side="left", padx=4)

    def start():
        settings.bird_shape = shape_var.get()
        root.destroy()

    tk.Button(root, text="Play!", font=("Arial", 13, "bold"),
              bg="#4CAF50", fg="white", padx=20, pady=8,
              command=start).pack(pady=16)

    root.mainloop()