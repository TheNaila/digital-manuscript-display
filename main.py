# Naila Thevenot Fall 2022 --> main.py
import time
import tkinter as tk
# remove unecessary
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import threading
import os
import sounddevice as sd
import json
import re
import soundfile as sf
import json_conversion
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

provided_description_file = False
provided_img_folder = False
pictures = None
description_file = None
submit_btn = False
music_file = None
music_duration = None
img_dur_each = None
fade_dur = 10
music_data = None
fs = None
count = 0
img = None
img_collection_folder = None


# creating a thread for the music
def play_song(filename):
    global music_data
    global fs
    sd.play(music_data, fs, blocking=False)
    sessions = AudioUtilities.GetAllSessions()  # all programs running audio
    for session in sessions:
        if session.Process and session.Process.name() == "python.exe":
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            volume.SetMasterVolume(.5, None)
    sd.wait()


def display_imgs(_count, label, frame):
    global count
    count = _count
    # removes all widgets from the prev page
    for widgets in frame.winfo_children():
        widgets.destroy()
    if count == len(pictures):
        return
    if label is not None:
        label.destroy()
    global img
    global img_collection_folder
    img = ImageTk.PhotoImage(Image.open(img_collection_folder + "/" + pictures[count]))
    # image label
    new_l = Label(frame, image=img, bg='black')
    new_l.pack(side=LEFT, padx=30)

    # text description
    img_description = None
    global description_file

    json_data = json.loads(description_file)
    # gets the item from the jSON description_file for the corresponding image
    for items in json_data:
        # split the image name
        acc_num = re.split("-|.jpg", pictures[count])
        # put at all together with dots and removing the .jpg while adding AC" / drop off the last element or any empty
        num = acc_num[0]
        for char in acc_num:
            if char == num:  # change
                continue
            if char == " " or char == "":
                continue
            elif char != acc_num[-1]:
                num = num + '.' + char
        num = "AC " + num
        if items["Accession Number"] == num:
            img_description = items
            break
    if img_description:
        description = Text(frame)
        description.configure(bg='black', fg='white', font='Times 14', borderwidth=0)
        for keys in img_description:
            if keys == 'Title':
                description.tag_config("Title", justify='center', font='Times 24 bold')
                description.insert("1.0", img_description[keys] + "\n\n")
                description.tag_add("Title", "1.0", '1.0 lineend')
            else:
                description.insert(tk.END, img_description[keys] + "\n\n")

        description.pack(side=RIGHT)
    global img_dur_each
    if count == len(pictures):
        time.sleep(img_dur_each - fade_dur)
        change_vol()

    count = count + 1
    win.after(img_dur_each * 1000, display_imgs, count, new_l, frame)


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
                current = volume.GetMasterVolume()


def submit(img_duration):
    global music_data
    global fs
    global music_file
    global pictures
    global music_duration
    global img_dur_each
    global fade_dur
    global img_dur_each
    global description_file

    music_data, fs = sf.read(music_file)

    if music_file is not None:
        sng_thr = threading.Thread(target=play_song, args=(music_file,))  # red is NOT an issue, super nitpicky about space between args
        sng_thr.start()

    if img_duration.get("1.0", "end-1c") != "":
        music_duration = int(len(music_data) / fs)
        img_dur_each = int(img_duration.get("1.0", "end-1c"))
    else:
        music_duration = int(len(music_data) / fs)  # in seconds
        img_dur_each = int(music_duration / len(pictures))
        if img_dur_each < 30:
            img_dur_each = 30
    win.after(300, create())


def get_img_path(img_label):
    global img_collection_folder
    img_collection_folder = filedialog.askdirectory()
    for root, dirs, files in os.walk(img_collection_folder): #go through image folder
        if len(files) == 0:
            text = "There are no files in this folder"
            img_label.configure(text=text)
            break
        for file in files:
            if not file.endswith('jpg'):
                text = "All files must be images"
                img_label.configure(text=text)
                break
    if img_collection_folder == "":
        text = "Please select a folder."
        img_label.configure(text=text)
    elif os.path.getsize(img_collection_folder) == 0:
        text = "This folder is empty. Please select another."
        img_label.configure(text=text)
    else:
        global provided_img_folder
        provided_img_folder = True
        enable_submit()
        global pictures
        pictures = os.listdir(img_collection_folder)
        pictures = sorted(pictures)
        img_label.configure(text=img_collection_folder)


def get_text_path(txt_label):
    global description_file
    description_file = filedialog.askopenfile(mode='r', filetypes=[('text files', '*.txt'), ('json files', '*.json')])

    if description_file != "" and description_file is not None:
        txt_label.configure(text=description_file.name)
        split_path = os.path.splitext(description_file.name)  # splits between the description_file name and extension
        if split_path[1] == '.txt':
            description_file = json_conversion.main(description_file.name)
        global provided_description_file
        provided_description_file = True
        enable_submit()
        description_file = open(description_file, "r")
        description_file = description_file.read()


def get_mc_path(mc_label):
    temp_file = filedialog.askopenfile(filetypes=[('mp3 files', '*.mp3')])
    global music_file
    if temp_file is not None:
        music_file = temp_file.name.replace("/", "\\")
    mc_label.configure(text=music_file)


def enable_submit():
    global provided_img_folder
    global provided_img_folder

    if provided_img_folder and provided_img_folder:
        global submit_btn
        submit_btn["state"] = "active"


def prompt(window):

    window.title("Image Projection")
    window.configure(bg='black')
    frame = Frame(window, width=800, height=500, bg="black")
    frame.grid_propagate(False)  # prevents frame from resizing based on child element
    frame.grid()

    title_label = Label(frame, text="Image Projection", font=" Times 16 bold", fg="white", bg="black")
    title_label.grid(row=0, column=1, sticky="W", padx=(95, 0))

    # image folder
    img_selection_btn = Button(frame, text="Select Image Collection", command=lambda: get_img_path(img_label),
                               font="Times 12", width=20, borderwidth=0, pady=3, bg="grey")
    img_selection_btn.grid(row=1, column=0, padx=(35, 0), pady=(45, 0), sticky="E")

    img_label = Label(frame, width=60, height=1, font="Times 12", pady=5)
    img_label.grid(row=1, column=1, pady=(45, 0))

    notes_img_label = Label(frame, height=1, font="Times 10", text="Please select the image folder. This must be a folder, even if there is only one image inside. All files inside the folder must be a PNG or JPG.",
                            fg="white", bg="black")
    notes_img_label.grid(row=2, column=0, columnspan=2, sticky="W", padx=(32, 0), pady=(3, 15))

    # Text File path
    txt_selection_btn = Button(frame, text="Select Description File", font="Times 12 ",
                               command=lambda: get_text_path(txt_label), width=20, borderwidth=0, pady=3, bg="grey")
    txt_selection_btn.grid(row=3, column=0, padx=(35, 0), sticky="E")

    txt_label = Label(frame, width=60, font="Times 12", pady=5)
    txt_label.grid(row=3, column=1)

    notes_txt_label = Label(frame, height=3, font="Times 10",
                            text="This should be a JSON or text file where each entry corresponds to an image in the collection folder. The order does not matter. Each entry must include at least a Title and an Accession Number (Image ID). Please select the file type in the bottom right corner of file selection window to see all acceptable files in a folder. Please don't include text you don't want to display.",
                            pady=5, fg="white", bg="black", wraplength=730, justify=LEFT)
    notes_txt_label.grid(row=4, column=0, padx=(31, 0), columnspan=2, sticky="W", pady=(3, 15))

    # Music description_file
    music_selection_btn = Button(frame, text="Select Music File", command=lambda: get_mc_path(music_label),
                                 font="Times 12", width=20, borderwidth=0, pady=3, bg="grey")
    music_selection_btn.grid(row=5, column=0, padx=(35, 0), sticky="E")

    music_label = Label(frame, width=60, height=1, font="Times 12", pady=5)
    music_label.grid(row=5, column=1)

    notes_mc_label = Label(frame, height=4, font="Times 10", text="Please ensure that the music file is in MP3 format. Verify that if you set a duration, that the music will last the entirety of the projection with a 10 second fade at the end. If you are not setting a duration, the music should allow that each image be displayed for at least 30 seconds. If a duration isn't set, each image will take up an equal stretch of time as allowed by the length of the music accounting for a 10 second fage out at the end.",
                           fg="white", bg="black", wraplength=730, justify= LEFT)
    notes_mc_label.grid(row=6, column=0, padx=(31, 0), columnspan=2, sticky="W", pady=(3, 15))

    # image duration
    img_duration_label = Label(frame, text="Set duration for each image (Optional)", font="Times 12 ", fg="white",
                               bg="black")
    img_duration_label.grid(row=8, column=0, sticky="W", columnspan=2, padx=(30, 0))

    img_duration = Text(frame, width=4, height=1)
    img_duration.grid(row=8, column=1, sticky="W", padx=(50, 0))

    global submit_btn
    submit_btn = Button(frame, text="Submit", command=lambda: submit(img_duration), state="disabled", width=10,
                        borderwidth=0, pady=3, bg="white")
    submit_btn.grid(row=9, column=1, sticky="E")
    return frame


def create():
    for child in win.winfo_children():
        child.destroy()

    win.attributes('-fullscreen', True)
    win.title("Mogul Period")
    win.configure(bg='black')
    frame = Frame(win, width=1000, height=800, bg="black")
    frame.pack_propagate(False) #prevents frame from resizing based on child element
    frame.pack()
    frame.place(relx=.5, rely=.5, anchor=CENTER)  # makes it so that even short images/text are centered
    toss_l = Label()
    win.after(300, display_imgs, count, toss_l, frame)  # need to delay call because the frame is in memory after this function runs

win = Tk()
prompt(win)
win.mainloop()


#fit text description
# use event listener to make pause, start, restart, end
#don't show accession number
#don't allow submit button if assertions are false
#better text format
#test out other collections
#Title only Option
#global vs passing args
#Go over code