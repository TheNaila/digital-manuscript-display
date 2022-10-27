# Naila Thevenot Fall 2022 --> test2.py
# displaying images with sound

import os
from threading import Thread
from pathlib import Path

import playsound
from matplotlib import pyplot as plt
import time
from matplotlib import image as mpimg


#creating a thread for the music
def play_song(filename):
    playsound.playsound(filename)
    print("running thread")



sng_thr = Thread(target = play_song, args = ("music.mp3",)) #red is NOT an issue, super nitpicky about space between args
sng_thr.start()

# Getting the folder path
folder = "Mogul Period"

pictures = os.listdir(folder)
pictures = sorted(pictures)
print(pictures)
pics_dict = {}
#
#assigning the images "Imagei" and tracking their respective file path
for count, pics in enumerate(pictures):
    pics_dict["Image" + str(count)] =  folder + '/' + pics

# #using matplotlib image to plot each image to a subplot by indexing the subplot array
three_counter = 0
three_pics = []

def three_dis(img_array,fig,_plot_arr):
    for count, pics in enumerate(img_array):
        fig.canvas.draw()
        _plot_arr[count].imshow(img_array[count])
        _plot_arr[count].axis("off")
    fig.canvas.draw()
    plt.pause(.1) #very important
    time.sleep(10)
    plt.close()
    three_pics.pop(0)


for img_key in pics_dict.keys():
    img = mpimg.imread(pics_dict[img_key])
    three_pics.append(img)

    if len(three_pics) == 3:
        fig, plot_arr = plt.subplots(1, 3, figsize=(15, 20))
        fig.set_facecolor('black')
        three_dis(three_pics, fig, plot_arr)
