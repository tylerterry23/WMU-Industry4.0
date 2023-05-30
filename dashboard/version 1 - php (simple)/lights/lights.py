# This is a simple example of how to use the tinytuya library to control a Tuya Smart WiFi Light Bulb
# created by @jasonacox for @hobbyquaker src: https://github.com/jasonacox/tinytuya
# Current created by @tylerterry23 for Western Michigan University industry4.0 lab

import tinytuya
import time

#? Connect to Device - pytuya Method
    # information in the following order: device ID, IP address, local key

d = tinytuya.BulbDevice('eb5ea8b4303fac35dcjyvu', '192.168.1.10', 'e443b95cc4b6a3a1')
d.set_version(3.3)
data = d.status()


#? Show status of first controlled switch on device
    # useful for debugging and testing

print(f'Status: {data}')



#? Dictionary of common colors
    # A couple common colors are included as well as a rainbow dictionary
    # this can be appended to as needed
rainbow = {"red": [255, 0, 0], "orange": [255, 127, 0], "yellow": [255, 200, 0], "green": [0, 255, 0], "blue": [0, 0, 255], "indigo": [46, 43, 95], "violet": [139, 0, 255]}

colors = {
    "red": [255, 0, 0], 
    "orange": [255, 127, 0], 
    "yellow": [255, 200, 0], 
    "green": [0, 255, 0], 
    "blue": [0, 0, 255], 
    "indigo": [46, 43, 95], 
    "violet": [139, 0, 255], 
    "white": [255, 255, 255], 
    "rainbow": {"red": [255, 0, 0], "orange": [255, 127, 0], "yellow": [255, 200, 0], "green": [0, 255, 0], "blue": [0, 0, 255], "indigo": [46, 43, 95], "violet": [139, 0, 255]}
}


# while input == 'y' lights are green and while input == 'n' lights toggle red repeatedly anything else is disregarded
while True:
    inn = input("> ")
    if inn == 'y':
        d.set_colour(colors["green"][0], colors["green"][1], colors["green"][2])
    elif inn == 'n':
        d.set_colour(colors["red"][0], colors["red"][1], colors["red"][2])
    else:
        # print("invalid input")
        time.sleep(.2)
        for i in range(2):
            for color in rainbow:
                d.set_colour(rainbow[color][0], rainbow[color][1], rainbow[color][2])
                time.sleep(.1)


#? Other possibly relevant functions
    # COLOR: set_colour(red, green, blue) |
        # Example: d.set_colour(255, 0, 0) - sets color to red (255/255, 0/255, 0/255)

    # BRIGHTNESS: set_brightness(brightness) | set_brightness_percentage(brightness=100, nowait):
        # Example: d.set_brightness(255) - sets brightness to 100% (255/255)
        # Example: d.set_brightness_percentage(50) - sets brightness to 50% (127.5/255)

    # WHITE: set_white(brightness, colourtemp) | set_white_percentage(brightness=100, colourtemp=100, nowait):
        # Example: d.set_white(255, 255) - sets brightness to 100% (255/255) and color temperature to 100% (255/255)
        # Example: d.set_white_percentage(50, 50) - sets brightness to 50% (127.5/255) and color temperature to 50% (127.5/255)

    # TEMPERATURE: set_colour_temp(colourtemp) | set_colour_temp_percentage(colourtemp=100, nowait):
        # Example: d.set_colour_temp(255) - sets color temperature to 100% (255/255)











#* TIPS AND TRICKS
#? Cycle through the Rainbow repeatedly until user enters 'q'
# while True:
#     for color in rainbow:
#         print(color)
#         d.set_colour(rainbow[color][0], rainbow[color][1], rainbow[color][2])
#         time.sleep(.1)

    





