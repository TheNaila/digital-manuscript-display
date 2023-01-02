#Naila Thevenot Fall 2022 --> main.py
import time
import tkinter as tk
#remove unecessary
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import threading
import os
import sounddevice as sd
import json
import re
import soundfile as sf

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume

configs = []
canvas_colour = "black"
mc_file = None
txt_p = False
img_p = False
file = None
sub_btn = False
mc_dur = None
img_dur_each = None
fade_dur = 10
index_img_start_fade = None
data = None
fs = None

#creating a thread for the music
def play_song(filename):
    global data
    global fs
    sd.play(data, fs, blocking=False)
    sd.wait()

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
    global index_img_start_fade
    global img_dur_each
    if count == index_img_start_fade:
        change_vol()

    count = count + 1
    win.after(img_dur_each*1000, display_imgs, count, new_l,frame)
def change_vol():
    sessions = AudioUtilities.GetAllSessions()  # all programs running audio

    for session in sessions:
        if session.Process and session.Process.name() == "python.exe":
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            current = volume.GetMasterVolume()
            math = current / fade_dur
            while current > 0.1:
                volume.SetMasterVolume(current - math, None)
                time.sleep(1)
                print(current)
                current = volume.GetMasterVolume()
            # volume.SetMasterVolume(.0, None) #0 is mute

def get_configs():
    global data
    global fs
    global mc_file

    data, fs = sf.read(mc_file)
    if mc_file!= None:
        sng_thr = threading.Thread(target=play_song,
                                   args=(mc_file,))  # red is NOT an issue, super nitpicky about space between args
        sng_thr.start()

    win.after(300,create())
    global pictures
    global mc_dur
    global img_dur_each
    global fade_dur
    global index_img_start_fade


    mc_dur = len(data) / fs  # in seconds
    img_dur_each = mc_dur / len(pictures)
    fade_dur = 10  # seconds
    index_img_start_fade = (mc_dur - fade_dur) / img_dur_each + 1
    print(index_img_start_fade, "index")

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
    file = filedialog.askopenfile(mode='r', filetypes=[('json files', '*.json')])
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
    file = filedialog.askopenfile(filetypes=[('mp3 files', '*.mp3')])
    global mc_file
    mc_file = None
    if file != None:
        mc_file = file.name.replace("/", "\\")
    label = Label(frame, text=mc_file, justify=LEFT)
    label.grid(row=3, column=2, columnspan=len(mc_file))
def prompt(win):
    #cab use grid
    global coll_name
    global ignore_
    win.title("Image Projection")
    win.configure(bg='white')
    frame = Frame(win, width=800, height=500, bg="black")
    frame.grid_propagate(False) #prevents frame from resizing based on child element
    frame.grid()

    title_label = Label(frame, text = "Image Projection", font= " Times 16 bold", fg="white", bg = "black")
    title_label.grid(row = 0, column = 1, sticky = "W", padx = (55,0))

    #image folder
    img_selection_btn = Button(frame, text="Select Image Collection", command=get_img_path, font="Times 12", width = 20,borderwidth=0, pady = 3, bg= "grey")
    img_selection_btn.grid(row = 1, column = 0, padx = (35,0), pady= (45,0), sticky= "E")

    img_label = Label(frame, width=50, height=1, font="Times 12", pady=5)
    img_label.grid(row=1, column=1,pady=(45,0))

    notes_img_label = Label(frame, height=1, font="Times 10", text = "This must be a folder and isn’t optional", fg="white", bg = "black")
    notes_img_label.grid(row=2, column=0,columnspan=2,sticky = "W", padx=(30,0), pady= (0,15))

    #Text File path
    txt_selection_btn = Button(frame, text="Select Text Description File",font="Times 12 ", command=get_text_path, width= 20, borderwidth=0, pady = 3, bg= "grey")
    txt_selection_btn.grid(row=3, column=0, padx = (35,0), sticky= "E")

    txt_label = Label(frame, width=50, font="Times 12", pady=5)
    txt_label.grid(row=3, column=1)

    notes_txt_label = Label(frame, height=1, font="Times 10",
                            text="This should be a JSON or .txt file where each entry corresponds to an image in the collection folder.\nEach entry must include at least a title and an Accession Number (Image ID)",
                            pady=5, fg="white", bg = "black", wraplength=1000, justify=LEFT)
    notes_txt_label.grid(row=4, column=0, padx=(31, 0), columnspan=2, sticky="W", pady= (3,15))

    #Music file
    music_selection_btn = Button(frame, text="Select Music File", command=get_mc_path, font="Times 12", width=20, borderwidth=0, pady = 3, bg= "grey")
    music_selection_btn.grid(row=5, column=0, padx = (35,0),sticky= "E")

    music_label = Label(frame, width=50, height=1, font="Times 12", pady=5)
    music_label.grid(row=5, column=1)

    notes_mc_label = Label(frame, height=1, font="Times 10", text="Please ensure that the music file is in MP3 format", fg="white", bg = "black")
    notes_mc_label.grid(row=6, column=0, padx=(31, 0), columnspan=2, sticky="W", pady= (0,15))

    #image duration
    img_duration_label = Label(frame, text = "Set duration for each image (Optional)", font="Times 12 ", fg="white", bg = "black")
    img_duration_label.grid(row = 7, column= 0, sticky="W", columnspan= 2, padx=(30,0))

    img_duration = Text(frame, width= 4, height= 1)
    img_duration.grid(row = 7, column= 1, sticky="W", padx=(50,0))

    global sub_btn
    sub_btn = Button(frame, text= "Submit", command= get_configs, state= "disabled", width = 10, borderwidth=0, pady = 3, bg= "grey")
    sub_btn.grid(row = 8, column = 1, sticky="E")
    return frame
def create():
    sessions = AudioUtilities.GetAllSessions()  # all programs running audio
    for session in sessions:
        if session.Process and session.Process.name() == "python.exe":
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            volume.SetMasterVolume(.5,None)

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
# #
# #allow setting duration
# #make music loop
# #make text description optional
# #ensure that images and text correlate
# #have a definite end/loop
# #add JSON conversion code as module
# #confirm logic
# #make prompt pretty
# #set music to come in properly
#
# #add different styles for how to display image + text --> 2 or 3
# #add ability to control projector
# #add support for ignoring certain labels
# #add security
# #integrate an API
# #optimize code
# #download to executable file
# #png vs jpg
# #enusre that args are images folders with at least one thing/ text file with at least one item
# #use exception handling
# #ensure there are images inside folder/not other files/text
#
# #Done
# #stuff should only happen if everything is filled in