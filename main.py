#Naila Thevenot Fall 2022 --> main.py
import tkinter as tk
#remove unecessary
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
txt_p = False
img_p = False
file = None
sub_btn = False
#creating a thread for the music
def play_song(filename):
    playsound.playsound(filename)
    global count
    global pictures
    if count != len(pictures):
        play_song(filename)

def display_imgs(_count, label,frame):
    global count
    count = _count
    #removes all widgets from the prev page
    for widgets in frame.winfo_children():
        widgets.destroy()
    if count == len(pictures):
        return
    if label != None:
        label.destroy()
    global img
    global folder
    img = ImageTk.PhotoImage(Image.open(folder + "/" + pictures[count]))
    #image label
    new_l = Label(frame, image = img, bg= 'black')
    new_l.pack(side = LEFT, padx = 30)

    #text description
    img_des = None
    global file
    data = json.loads(file)
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
        if items["Accession Number"] == num:
            img_des = items
            break
    if img_des:
        descrip = Text(frame)
        descrip.configure(bg='black', fg='white', font='Times 14', borderwidth=0)
        for keys in img_des:
            if keys == 'Title':
                descrip.tag_config("Title", justify='center', font= 'Times 24 bold')
                descrip.insert("1.0", img_des[keys] + "\n\n")
                descrip.tag_add("Title", "1.0", '1.0 lineend')
            else:
                #descrip.tag_config("Text", font='Times 14')
                descrip.insert(tk.END, img_des[keys] + "\n\n")
                #descrip.tag_add("Text", "1.0")

            #descrip.insert(tk.END, img_des[keys] + "\n\n")

        descrip.pack(side = RIGHT)

    count = count + 1
    win.after(3000, display_imgs, count, new_l,frame)
def get_configs():
    global mc_file
    if mc_file!= None:
        sng_thr = threading.Thread(target=play_song,
                                   args=(mc_file,))  # red is NOT an issue, super nitpicky about space between args
        sng_thr.start()
    win.after(300,create())
def pass_path(item, img = False):
    #Getting the folder path
    if img:
        global folder
        folder = item
        global pictures
        pictures = os.listdir(folder)
        pictures = sorted(pictures)
        label = Label(frame, text = item, justify= LEFT)
        label.grid(row = 4, column = 2, columnspan= len(item))
    else:
        global file
        file = open(item, "r")
        file = file.read()
        label = Label(frame, text=item, justify= LEFT)
        label.grid(row=5, column=2, columnspan= len(item))
def get_img_path():
    coll_dir = filedialog.askdirectory()
    for root, dirs, files in os.walk(coll_dir):
        print(len(files))
        if len(files) == 0:
            #FIXXXXXXXXXXX
            print("There are no files in this folder")
            # label = Label(frame, text=text, justify=LEFT)
            # label.grid(row=4, column=2, columnspan=len(text))
            break
        for file in files:
            if not file.endswith('jpg'):
                text = "All files must be images"
                label = Label(frame, text=text, justify=LEFT)
                label.grid(row=4, column=2, columnspan=len(text))
                break
    if coll_dir == "":
        text = "Please select a folder."
        label = Label(frame, text=text, justify=LEFT)
        label.grid(row=4, column=2, columnspan=len(text))
    elif os.path.getsize(coll_dir) == 0:
        text = "This folder is empty. Please select another."
        label = Label(frame, text=text, justify=LEFT)
        label.grid(row=4, column=2, columnspan=len(text))
    else:
        pass_path(coll_dir, img= True)
        global txt_p
        txt_p = True
        en_sub()
def get_text_path():
    file = filedialog.askopenfile(mode='r', initialdir= filedialog.askdirectory(), filetypes=[('json files', '*.json')])
    file_r = open(file.name, "r") #check if string path is valid first
    file_r = file.read()

    if re.match("\w",file_r) == None: #fix
        print("Empty")
    if file != "" and file != None :
        pass_path(file.name, img = False)
        global img_p
        img_p = True
        en_sub()
def en_sub():
    global txt_p
    global img_p

    if img_p and txt_p:
        global sub_btn
        sub_btn["state"] = "active"
def get_mc_path():
    file = filedialog.askopenfile(initialdir=filedialog.askdirectory(), filetypes=[('mp3 files', '*.mp3')])
    global mc_file
    mc_file = None
    if file != None:
        mc_file = file.name.replace("/", "\\")
def prompt(win):
    #cab use grid
    global coll_name
    global ignore_
    win.title("Image Projection")
    win.configure(bg='white')
    frame = Frame(win, width=500, height=500, bg="white")
    frame.grid_propagate(False) #prevents frame from resizing based on child element
    frame.pack()

    tit_label = Label(frame, text = "Image Projection", font= " Times 12 bold")
    tit_label.grid(row = 0, column = 2, rowspan=2,columnspan=2)

    #Music file
    m_btn = Button(frame, text="Select Music File", command=get_mc_path)
    m_btn.grid(row=3, column=1)

    #image folder
    p_btn = Button(frame, text="Select Folder", command=get_img_path)
    p_btn.grid(row = 4, column = 1)

    #Text File path
    i_btn = Button(frame, text="Select Description File", command=get_text_path)
    i_btn.grid(row=5, column=1)

    global sub_btn
    sub_btn = Button(frame, text= "Submit", command= get_configs, state= "disabled")
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

#allow setting duration
#make music loop
#make text description optional
#ensure that images and text correlate
#have a definite end/loop
#add JSON conversion code as module
#confirm logic
#make prompt pretty
#set music to come in properly

#add different styles for how to display image + text --> 2 or 3
#add ability to control projector
#add support for ignoring certain labels
#add security
#integrate an API
#optimize code
#download to executable file
#png vs jpg
#enusre that args are images folders with at least one thing/ text file with at least one item
#use exception handling
#ensure there are images inside folder/not other files/text

#Done
#stuff should only happen if everything is filled in