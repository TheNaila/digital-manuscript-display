#Naila Thevenot Fall 2022 --> main.py
import cv2 as cv
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import time
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
    if count == len(pictures) - 1:
        return
    if label != None:
        label.destroy()
    global img
    img = ImageTk.PhotoImage(Image.open("Mogul Period/" + pictures[count]))
    #image label
    new_l = Label(frame, image = img, bg= 'black')
    new_l.pack()
    new_l.place(relheight=1,relwidth=1)
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
            if p == num:
                continue
            if p == " " or p == "":
                continue
            elif p != acc_num[-1]:
                num = num + '.' + p
        num = "AC " + num
        #print(num)
        if items["Accession Number"] == num:
            img_des = items
            print(img_des)
            break
    ##WARNING must find way to display image on half the screen and text on the other
    descrip = Text(frame, height=1, width=25)
    descrip.insert(tk.END, str(img_des))
    descrip.pack()

    count = count + 1
    win.after(3000, display_imgs, count, new_l,frame)
def intro(frame):
    # title bar
    title_l = Text(frame, height=1, width=25, borderwidth=0, pady= 5)
    title_l.insert(tk.END, "Majnun in the Wilderness")
    title_l.pack()
    title_l.tag_configure("tag_name", justify='center')
    title_l.tag_add("tag_name", "1.0", "end")
    title_l.configure(bg='black', fg='white', font='Times 20 bold') #has padding

    # adding cover image
    global cov_img
    img = Image.open("Mogul Period/" + "1967-47.jpg")
    img_res = img.resize((406, 562), Image.ANTIALIAS)
    cov_img = ImageTk.PhotoImage(img_res)
    img_l = Label(frame, image=cov_img)
    img_l.pack(side = tk.LEFT, padx = 50) #make padding such that it configures automatically

    # collection description
    text_l = Text(frame, height= 7, width = 80, wrap = WORD, borderwidth=0)
    text_l.configure(bg='black', fg='white', font='Times 12')
    txt2 = "\tThe story of Layla and Qays’s unrequited love is an allegory for the mystic’s desire for union with God. The star-crossed sweethearts meet as youths, but being from rival clans they are forbidden from marrying. As a result of their forced separation, Qays goes crazy, retreats into the desert, and becomes known as Majnun (“mad one”). This painting shows the emaciated, unkempt Majnun seated under a large tree. Sympathetic animals gather in pairs around him, while a crowd of concerned visitors approaches from the left. Majnun, meanwhile, appears otherwise preoccupied, no doubt with thoughts of his beloved."
    text_l.insert(tk.END, txt2)
    text_l.pack(side = tk.LEFT, padx = 15)
    #text_b.update() #need before getting dimensions

    toss_l = Label()
    win.after(3000,display_imgs,0,toss_l,frame)
def create(win):
    win.attributes('-fullscreen', True)
    win.title("Mogul Period")
    win.configure(bg='black')
    frame = Frame(win, width=1000, height=800, bg= "black")
    frame.pack_propagate(False) #prevents frame from resizing based on child element
    frame.pack()
    intro(frame)
    return frame

win = Tk()
frame = create(win)

# Getting the folder path
folder = "Mogul Period"

pictures = os.listdir(folder)
pictures = sorted(pictures)

win.mainloop()
