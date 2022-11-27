#Naila Thevenot Fall 2022 --> main.py
import cv2 as cv
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import threading
import os
import playsound
import json
import re

canvas_colour = "black"
#creating a thread for the music
def play_song(filename):
    playsound.playsound(filename)
    print("running thread")

sng_thr = threading.Thread(target = play_song, args = ("music.mp3",)) #red is NOT an issue, super nitpicky about space between args
sng_thr.start()

def display_imgs(count, label,frame):
    #removes all widgets from the prev page
    for widgets in frame.winfo_children():
        widgets.destroy()
    if count == len(pictures) - 1:
        return
    if label != None:
        label.destroy()
    global img
    img = ImageTk.PhotoImage(Image.open("Mogul Period/" + pictures[count]))
    #image label
    new_l = Label(frame, image = img, bg= 'black')
    new_l.pack(side = LEFT, padx = 30)

    #text description
    img_des = None
    file = open("sample.json", "r")
    data = json.loads(file.read())

    #gets the item from the jSON file for the corresponding image
    for items in data:
        #split the image name
        acc_num = re.split("-|.jpg", pictures[count])
        #put at all together with dots and removing the .jpg while adding AC" / drop off the last element or any empty
        num = acc_num[0]
        for p in acc_num:
            if p == num: #change
                continue
            if p == " " or p == "":
                continue
            elif p != acc_num[-1]:
                num = num + '.' + p
        num = "AC " + num
        #print(num)
        if items["Accession Number"] == num:
            img_des = items
            break
    if img_des:
        descrip = Text(frame)
        descrip.configure(bg='black', fg='white', font='Times 12')
        for keys in img_des:
            descrip.insert(tk.END, img_des[keys] + "\n\n")
        descrip.pack(side = RIGHT)

    count = count + 1
    win.after(3000, display_imgs, count, new_l,frame)

def create(win):
    win.attributes('-fullscreen', True)
    win.title("Mogul Period")
    win.configure(bg='black')
    frame = Frame(win, width=1000, height=800, bg= "black")
    #frame.pack_propagate(False) #prevents frame from resizing based on child element
    frame.pack()
    frame.place(relx=.5, rely=.5, anchor = CENTER) #makes it so that even short images/text are centered

    toss_l = Label()

    win.after(300, display_imgs, 0, toss_l, frame) #need to delay call because the frame is in memory after this function runs

    return frame

win = Tk()
frame = create(win)

# Getting the folder path
folder = "Mogul Period"

pictures = os.listdir(folder)
pictures = sorted(pictures)

win.mainloop()
