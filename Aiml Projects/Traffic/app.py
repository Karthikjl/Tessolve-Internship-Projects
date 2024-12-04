import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os

def detect_traffic_signals_and_symbols(image_path, hsv_ranges):
    if not os.path.exists(image_path):
        messagebox.showerror("Error", f"File not found: {image_path}")
        return

    image = cv2.imread(image_path)
    if image is None:
        messagebox.showerror("Error", "Failed to load image.")
        return

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    red_lower, red_upper = hsv_ranges['red_lower'], hsv_ranges['red_upper']
    yellow_lower, yellow_upper = hsv_ranges['yellow_lower'], hsv_ranges['yellow_upper']
    green_lower, green_upper = hsv_ranges['green_lower'], hsv_ranges['green_upper']

    mask_red = cv2.inRange(hsv, red_lower, red_upper)
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    mask_green = cv2.inRange(hsv, green_lower, green_upper)

    mask_combined = mask_red | mask_yellow | mask_green

    contours, _ = cv2.findContours(mask_combined, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        if radius > 5:
            if cv2.pointPolygonTest(cnt, (int(x), int(y)), True) >= 0:
                if mask_red[int(y), int(x)] > 0:
                    color = (0, 0, 255)
                elif mask_yellow[int(y), int(x)] > 0:
                    color = (0, 255, 255)
                elif mask_green[int(y), int(x)] > 0:
                    color = (0, 255, 0)
                cv2.circle(image, (int(x), int(y)), int(radius), color, 2)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)

        if len(approx) == 8:
            cv2.drawContours(image, [approx], 0, (255, 0, 0), 3)
            x, y, w, h = cv2.boundingRect(approx)
            cv2.putText(image, 'Stop Sign', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        elif len(approx) > 8:
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            if 30 < radius < 100:
                cv2.circle(image, (int(x), int(y)), int(radius), (255, 255, 0), 2)
                cv2.putText(image, 'Speed Limit', (int(x) - 40, int(y) - int(radius) - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_rgb)
    return image_pil

def process_image():
    if not image_path:
        messagebox.showerror("Error", "No image loaded.")
        return

    try:
        hsv_ranges = {
            'red_lower': np.array([
                red_lower_hue.get(),
                red_lower_sat.get(),
                red_lower_val.get()
            ]),
            'red_upper': np.array([
                red_upper_hue.get(),
                red_upper_sat.get(),
                red_upper_val.get()
            ]),
            'yellow_lower': np.array([
                yellow_lower_hue.get(),
                yellow_lower_sat.get(),
                yellow_lower_val.get()
            ]),
            'yellow_upper': np.array([
                yellow_upper_hue.get(),
                yellow_upper_sat.get(),
                yellow_upper_val.get()
            ]),
            'green_lower': np.array([
                green_lower_hue.get(),
                green_lower_sat.get(),
                green_lower_val.get()
            ]),
            'green_upper': np.array([
                green_upper_hue.get(),
                green_upper_sat.get(),
                green_upper_val.get()
            ]),
        }

        output_image = detect_traffic_signals_and_symbols(image_path, hsv_ranges)
        
        if output_image:
            img = ImageTk.PhotoImage(output_image)
            image_label.config(image=img)
            image_label.image = img
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process image: {e}")

def load_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    if not image_path:
        return

    try:
        img = Image.open(image_path)
        img.thumbnail((400, 400))
        img = ImageTk.PhotoImage(img)
        
        image_label.config(image=img)
        image_label.image = img
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open image: {e}")

# GUI setup
root = tk.Tk()
root.title("Traffic Signal and Symbol Detection")

# Create a canvas for scrolling
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a scrollbar
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a frame to contain the sliders and image
frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor=tk.NW)

# Bind scrolling
def on_canvas_configure(event):
    canvas.config(scrollregion=canvas.bbox("all"))

canvas.bind("<Configure>", on_canvas_configure)

# Image label
image_label = tk.Label(frame)
image_label.grid(row=0, column=0, padx=10, pady=10)

# Sliders for HSV ranges
def create_slider(frame, label, row, from_, to_, orient=tk.HORIZONTAL):
    tk.Label(frame, text=label).grid(row=row, column=0, padx=5, pady=2, sticky="w")
    slider = tk.Scale(frame, from_=from_, to_=to_, orient=orient)
    slider.grid(row=row, column=1, padx=5, pady=2, sticky="ew")
    return slider

# Red color sliders
red_lower_hue = create_slider(frame, "Red Lower Hue:", 1, 0, 179)
red_lower_sat = create_slider(frame, "Red Lower Saturation:", 2, 0, 255)
red_lower_val = create_slider(frame, "Red Lower Value:", 3, 0, 255)
red_upper_hue = create_slider(frame, "Red Upper Hue:", 4, 0, 179)
red_upper_sat = create_slider(frame, "Red Upper Saturation:", 5, 0, 255)
red_upper_val = create_slider(frame, "Red Upper Value:", 6, 0, 255)

# Yellow color sliders
yellow_lower_hue = create_slider(frame, "Yellow Lower Hue:", 7, 0, 179)
yellow_lower_sat = create_slider(frame, "Yellow Lower Saturation:", 8, 0, 255)
yellow_lower_val = create_slider(frame, "Yellow Lower Value:", 9, 0, 255)
yellow_upper_hue = create_slider(frame, "Yellow Upper Hue:", 10, 0, 179)
yellow_upper_sat = create_slider(frame, "Yellow Upper Saturation:", 11, 0, 255)
yellow_upper_val = create_slider(frame, "Yellow Upper Value:", 12, 0, 255)

# Green color sliders
green_lower_hue = create_slider(frame, "Green Lower Hue:", 13, 0, 179)
green_lower_sat = create_slider(frame, "Green Lower Saturation:", 14, 0, 255)
green_lower_val = create_slider(frame, "Green Lower Value:", 15, 0, 255)
green_upper_hue = create_slider(frame, "Green Upper Hue:", 16, 0, 179)
green_upper_sat = create_slider(frame, "Green Upper Saturation:", 17, 0, 255)
green_upper_val = create_slider(frame, "Green Upper Value:", 18, 0, 255)

# Buttons
load_button = tk.Button(frame, text="Load Image", command=load_image)
load_button.grid(row=19, column=0, padx=10, pady=5, sticky="ew")

process_button = tk.Button(frame, text="Process Image", command=process_image)
process_button.grid(row=19, column=1, padx=10, pady=5, sticky="ew")

# Initialize global variables
image_path = ""

# Start GUI main loop
root.mainloop()
