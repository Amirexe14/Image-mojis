import tkinter as tk
import pyautogui
import io
import win32clipboard
import time
import threading
import os
from PIL import Image, ImageTk
import keyboard

visible_and_active = True

def follow_mouse():
    while True:
        if not visible_and_active:
            x, y = pyautogui.position()
            root.geometry(f"+{x+10}+{y-40}")
            root.attributes('-alpha', 0.0)
            root.attributes('-disabled', True)

        elif visible_and_active:
            root.attributes('-alpha', 1.0)
            root.attributes('-disabled', False)
        time.sleep(0.01)


def ImageToClipboard(index, image):
    img = Image.open(f"{currentdirectory}{image}")
    output = io.BytesIO()
    img.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

def looper():
    global visible_and_active
    if keyboard.is_pressed('f4'):
        visible_and_active = not visible_and_active
        print("Toggled:", visible_and_active)
    root.after(50, looper)


root = tk.Tk()
root.title("Image-moji")
root.overrideredirect(True)  # No 
root.attributes("-topmost", True) 

currentdirectory = f"{os.getcwd()}\\src\\"

pictures = os.listdir(currentdirectory)

image_refs = []
y = 0
x = -1

for index, picture in enumerate(pictures):

    x += 1
    if x / 10 == 1:
        y += 1
        x = 0

    img = Image.open(f"{currentdirectory}{picture}")
    img = img.resize((50,50))
    tk_img = ImageTk.PhotoImage(img)
    image_refs.append(tk_img)

    btn = tk.Button(root, image=tk_img, command=lambda i=index, p=picture: ImageToClipboard(i, p), borderwidth=0)
    btn.grid(row=y, column=x)

threading.Thread(target=follow_mouse, daemon=True).start()

looper()
root.mainloop()