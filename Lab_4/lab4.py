# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import digitalio
import webcolors
import pyttsx3

from adafruit_apds9960.apds9960 import APDS9960
from adafruit_apds9960 import colorutility

from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789

from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# The display uses a communication protocol called SPI.
# SPI will not be covered in depth in this course. 
# you can read more https://www.circuitbasics.com/basics-of-the-spi-communication-protocol/
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000  # the rate  the screen talks to the pi

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    board.SPI(),
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# these setup the code for our buttons and the backlight and tell the pi to treat the GPIO pins as digitalIO vs analogIO
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()


i2c = board.I2C()
apds = APDS9960(i2c)
apds.enable_color = True

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (disp.height, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
#draw.rectangle((width, 0, disp.height, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 20)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
back_text_color="#FFFFFF"
fore_text_color="#FF0000"

# Audio settings
engine=pyttsx3.init()

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = "None"
    return actual_name, closest_name

while True:
    # create some variables to store the color data in
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    y=top
    
    # wait for color data to be ready
    while not apds.color_data_ready:
        time.sleep(0.005)

    # get the data and print the different channels
    r, g, b, c = apds.color_data
    print("red: ", r)
    print("green: ", g)
    print("blue: ", b)
    print("clear: ", c)

    print("color temp {}".format(colorutility.calculate_color_temperature(r, g, b)))
    print("light lux {}".format(colorutility.calculate_lux(r, g, b)))
    #display.fill(color565(r, g, b))
    requested_colour = (r, g, b)
    actual_name, closest_name = get_colour_name(requested_colour)
    print("Actual colour name:", actual_name, ", closest colour name:", closest_name)

    _str= "Actual colour name:"
    draw.text((x,y),_str,font=font,fill=back_text_color)

    y += font.getsize(_str)[1]
    x=0

    _str= actual_name
    draw.text((x,y),_str,font=font,fill=back_text_color)

    y += font.getsize(_str)[1]
    x=0

    _str="closest colour name:"
    draw.text((x,y),_str,font=font,fill=back_text_color)

    y += font.getsize(_str)[1]
    x=0

    _str=closest_name
    draw.text((x,y),_str,font=font,fill=back_text_color)
    engine.say(_str)
    engine.runAndWait()

    # Display image.
    disp.image(image, rotation)

    time.sleep(0.5)
