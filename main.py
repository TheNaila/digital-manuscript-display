#Naila Thevenot Fall 2022 --> main.py
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import threading
import os
import playsound
import json
import re

configs = []
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
def get_configs():
    configs.append(coll_name.get(1.0, "end-1c"))
    configs.append(ignore_.get(1.0,"end-1c"))
    win.after(300,create())
    print(configs)
def pass_path(item):
    # Getting the folder path
    folder = item
    global pictures
    pictures = os.listdir(folder)
    pictures = sorted(pictures)
    label = Label(frame, text = item)
    label.grid(row = 4, column = 2)
    print(folder)
def get_img_path():
    coll_dir = filedialog.askdirectory()
    pass_path(coll_dir)
def get_text_path():
    file = filedialog.askopenfile(mode='r', initialdir= filedialog.askdirectory(), filetypes=[('text files', '*.txt')])
def prompt(win):
    #cab use grid
    global coll_name
    global ignore_
    win.title("Image Projection")
    win.configure(bg='white')
    frame = Frame(win, width=500, height=500, bg="white")
    frame.grid_propagate(False) #prevents frame from resizing based on child element
    frame.pack()
    # frame.columnconfigure(0, weight=3)
    # frame.rowconfigure(1, weight=1)

    tit_label = Label(frame, text = "Image Projection", font= " Times 12 bold")
    tit_label.grid(row = 0, column = 2, rowspan=2,columnspan=2)

    #collection name
    coll_n_l = Label(frame, text = "Collection Name")
    coll_n_l.grid(row=3, column=1)

    coll_name = Text(frame,height = 1,width = 25)
    coll_name.grid(row=3,column=2)

    #image folder
    p_btn = Button(frame, text="Select Folder", command=get_img_path)
    p_btn.grid(row = 4, column = 1)

    #Text File path
    p_btn = Button(frame, text="Select Description File", command=get_text_path)
    p_btn.grid(row=5, column=1)

    # #labels to ignore / need to grab input and update json loop
    # ignore_ = Text(frame,height = 1,width = 50) #Make expandable
    # ignore_.grid(row = 4, column = 2)
    #
    sub_btn = Button(frame, text= "Submit", command= get_configs)
    sub_btn.grid(row = 6, column = 6)
    return frame

def create():
    for child in win.winfo_children():
        child.destroy()

    win.attributes('-fullscreen', True)
    win.title("Mogul Period")
    win.configure(bg='black')
    frame = Frame(win, width=1000, height=800, bg="black")
    # frame.pack_propagate(False) #prevents frame from resizing based on child element
    frame.pack()
    frame.place(relx=.5, rely=.5, anchor=CENTER)  # makes it so that even short images/text are centered
    toss_l = Label()
    win.after(300, display_imgs, 0, toss_l, frame) #need to delay call because the frame is in memory after this function runs

win = Tk()
frame = prompt(win)

win.mainloop()

#finish getting text path
#add JSON conversion code as module
#confirm logic
#make prompt pretty


#add different styles for how to display image + text --> 2 or 3
#add ability to control projector
#add support for ignoring certain labels
#add security
#optimize code
#download to executable file
