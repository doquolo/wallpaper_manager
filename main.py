import ctypes
import random
import os
import image
import screeninfo

def applyBG(imagePath):
    ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, imagePath , 0x01 | 0x02) #SPI_SETDESKWALLPAPER
    return;

# set dir
directory = r"C:\Users\doquolo\Pictures\bg"
# discover image
file_list = os.listdir(directory)
# filter out image that isnt image (now looking for jpg, bmp, png)
image_list = []
for i in range(len(file_list)-1):
    # seperate file name and file extension
    print(i)
    ext = file_list[i].split(".")[-1]
    if ext.lower() in ['jpg', 'bmp', 'png']:
        image_list.append(file_list[i])

print(image_list)

while True:
    inp = input("d for single monitor, a for all, q to quit: ")
    if inp == "d":
        # choose image
        image_index = random.randrange(0, len(image_list)-1)
        # get all available screen
        num_screen = len(screeninfo.get_monitors())
        # turn background on/off on which screen?
        onoff = []
        for i in range(num_screen):
            choice = int(input(f"Background on display {i+1} (1-on/0-off): "))
            onoff.append(choice)
        image.generateBG(onoff, f"{directory}\\{image_list[image_index]}")
        applyBG(f"{os.getcwd()}\\out.jpg")
    if inp == "a":
        # choose image
        image_index = random.randrange(0, len(image_list)-1)
        # get all available screen
        num_screen = len(screeninfo.get_monitors())
        # turn background on for all screen
        onoff = []
        for i in range(num_screen):
            onoff.append(1)
        image.generateBG(onoff, f"{directory}\\{image_list[image_index]}")
        applyBG(f"{os.getcwd()}\\out.jpg")
    elif inp == "q":
        break;