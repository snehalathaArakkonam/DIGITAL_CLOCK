import tkinter as tk
from time import strftime
import requests
import threading
import time

# Main window
root = tk.Tk()
root.title("Digital Clock - Competition Edition")
root.configure(bg='black')
root.resizable(False, False)

# Location Label - Professional touch
location_var = tk.StringVar()
location_var.set("Detecting approximate location...")
location_label = tk.Label(
    root,
    textvariable=location_var,
    font=("Helvetica", 18, "italic"),
    fg="#00ffff",          # Cyan
    bg="black"
)
location_label.pack(pady=20)

# Time Label - Huge Neon Green
time_label = tk.Label(
    root,
    font=("Arial", 110, "bold"),
    fg="#ff0000",          # Bright Neon Green
    bg="black"
)
time_label.pack(pady=20)

# Date Label - Magenta
date_label = tk.Label(
    root,
    font=("Helvetica", 30),
    fg="#ffff00",          # Magenta
    bg="black"
)
date_label.pack(pady=20)

# Multiple APIs for best possible location
APIs = [
    "https://ipapi.co/json/",
    "http://ip-api.com/json/",
    "https://freeipapi.com/api/json",
    "https://ipwho.is/"
]

def fetch_location():
    for api in APIs:
        try:
            response = requests.get(api, timeout=8)
            data = response.json()
            city = data.get("city") or "Unknown"
            region = data.get("region") or data.get("regionName", "")
            country = data.get("country") or data.get("country_name", "India")
            if city != "Unknown":
                location_var.set(f"Approximate Location: {city}, {region}, {country}")
                return
        except:
            continue
    location_var.set("Approximate Location: India")

# Update time & date
def update_clock():
    time_str = strftime("%H:%M:%S")          # 24-hour format
    date_str = strftime("%A, %d %B %Y")
    time_label.config(text=time_str)
    date_label.config(text=date_str)
    root.after(1000, update_clock)

# Refresh location every 30 minutes
def location_loop():
    while True:
        fetch_location()
        time.sleep(1800)

# Start everything
fetch_location()
update_clock()
threading.Thread(target=location_loop, daemon=True).start()

# Center the window
root.update_idletasks()
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
size = tuple(int(_) for _ in root.geometry().split('+')[0].split('x'))
x = w//2 - size[0]//2
y = h//2 - size[1]//2
root.geometry(f"+{x}+{y}")

# Uncomment these 2 lines for fullscreen demo (Esc to exit)
# root.attributes("-fullscreen", True)
# root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()