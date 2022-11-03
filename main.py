import cv2
from tkinter import *
from PIL import Image, ImageTk
import time
import threading
import os
import playsound

canvas_colour = "black"

# #creating a thread for the music
# def play_song(filename):
#     playsound.playsound(filename)
#     print("running thread")
#
#
# sng_thr = threading.Thread(target = play_song, args = ("music.mp3",)) #red is NOT an issue, super nitpicky about space between args
# sng_thr.start()

def create(win):
    #win.attributes('-fullscreen', True)
    win.title("Mogul Period")
    frame = Frame(win, width=800, height=800, bg= "black")
    frame.pack()
    return frame

win = Tk()
frame = create(win)

#Adding img to frame ********

# Getting the folder path
folder = "Mogul Period"

pictures = os.listdir(folder)
pictures = sorted(pictures)

img = None

def recurse(count, label,frame):
    if count == len(pictures):
        return
    if label != None:
        label.destroy()
    global img
    img = ImageTk.PhotoImage(Image.open("Mogul Period/" + pictures[count]))
    new_l = Label(frame, image = img)
    new_l.pack()
    new_l.place(relheight=1,relwidth=1)
    count = count + 1
    win.after(3000, recurse, count, new_l,frame)

label = Label()
recurse(0, label,frame)

win.mainloop()
