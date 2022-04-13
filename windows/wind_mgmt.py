from tkinter import *

def destroy_frame_content(frame):
    for content in frame.winfo_children():
        content.destroy()

