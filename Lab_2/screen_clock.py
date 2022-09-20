import time
import subprocess
import digitalio
import board
import copy
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime
import random
# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

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
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 15)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
#Logic for Clock starts here

#variables for time
array_to_print=[]
letters = [
            ['I','T','R','I','S','U','H','A','L','F','T','E','N'],
            ['Q','U','A','R','T','E','R','T','W','E','N','T','Y'],
            ['F','I','V','E','Q','M','I','N','U','T','E','S','T'],
            ['P','A','S','T','M','T','O','S','A','M','O','P','M'],
            ['O','N','E','N','T','W','O','Z','T','H','R','E','E'],
            ['F','O','U','R','F','I','V','E','S','E','V','E','N'],
            ['S','I','X','E','I','G','H','T','Y','N','I','N','E'],
            ['T','E','N','E','L','E','V','E','N','P','H','I','L'],
            ['T','W','E','L','V','E','L','O','C','L','O','C','K'],
        ]
letters_blank = [
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        ]

#Colors
disablebackgroundletter=False
number_of_colors = 128
START_CHAR='#'
back_text_color="#FFFFFF"
fore_text_color="#FF0000"

def update_time():
        #array_to_print=deepcopy(letters_blank)
        array_to_print = [row[:] for row in letters_blank]
        current_time = time.localtime()

        hour = int(time.strftime("%I", current_time))
        minute = int(time.strftime("%M", current_time))
        am_or_pm = time.strftime("%p", current_time)

        returned_letters = translate_time(hour, minute, am_or_pm)
        #print("array returned:", letters)
        for letter in returned_letters:
            #print("each item is",letters[0][1])
            array_to_print[letter[0]][letter[1]]=letters[letter[0]][letter[1]]        
        #self.after(1000, self.update_time)
        #print("array to print",array_to_print)
        return array_to_print
def translate_to_or_past(minute):
        to_or_past = []
        if 3 <= minute < 33:
            to_or_past = [[3,0],[3,1],[3,2],[3,3]] # PAST
        elif 33 <= minute <= 57:
            to_or_past = [[3,5],[3,6]] # TO
        return to_or_past

def translate_minute(minute):
        if (minute > 30):
            minute = 60 - minute

        if minute >= 3:
            minute_blocks = [
                [[2,0],[2,1],[2,2],[2,3],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10],[2,11]], # FIVE
                [[0,10],[0,11],[0,12],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10],[2,11]], # TEN
                [[0,7],[1,0],[1,1],[1,2],[1,3],[1,4],[1,5],[1,6]], # A QUARTER
                [[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10],[2,11]], # TWENTY
                [[1,7],[1,8],[1,9],[1,10],[1,11],[1,12],[2,0],[2,1],[2,2],[2,3],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10],[2,11]], # TWENTYFIVE
                [[0,6],[0,7],[0,8],[0,9]], # HALF
            ]
            mapped_minute_value = round((0 + (5 - 0) * ((minute - 3) / (28 - 3))) - 0.4)
            minute_name = minute_blocks[mapped_minute_value]
        else:
            minute_name = ''
        return minute_name

def translate_hour(hour, minute):
        hours = [
            [[4,0],[4,1],[4,2]], #ONE
            [[4,4],[4,5],[4,6]], # TWO
            [[4,8],[4,9],[4,10],[4,11],[4,12]], # THREE
            [[5,0],[5,1],[5,2],[5,3]], # FOUR
            [[5,4],[5,5],[5,6],[5,7]], # FIVE
            [[6,0],[6,1],[6,2]], # SIX
            [[5,8],[5,9],[5,10],[5,11],[5,12]], # SEVEN
            [[6,3],[6,4],[6,5],[6,6],[6,7]], # EIGHT
            [[6,9],[6,10],[6,11],[6,12]], # NINE
            [[7,0],[7,1],[7,2]], # TEN
            [[7,3],[7,4],[7,5],[7,6],[7,7],[7,8]], # ELEVEN
            [[8,0],[8,1],[8,2],[8,3],[8,4],[8,5]], # TWELVE'
            [[4,0],[4,1],[4,2]], #ONE
        ]
        if minute > 33:
            return hours[hour]
        else:
            return hours[hour - 1]

def get_random_color():
        color = START_CHAR+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        #print(color)
        return color

def get_contrast_color(colour):
        rgb = int(colour.lstrip('#'), 16)
        complementary_colour = 0xffffff-rgb
        #print(f'{START_CHAR}{complementary_colour:06X}')
        return f'{START_CHAR}{complementary_colour:06X}'

def translate_time(hour, minute, am_or_pm):
        letters = [
            [0,0], [0,1], [0,3], [0,4] # IT IS
        ]

        letters.extend(translate_hour(hour, minute))
        letters.extend(translate_to_or_past(minute))
        letters.extend(translate_minute(minute))

        if (am_or_pm == 'PM'):
            letters.extend([[3,11],[3,12]]) # PM
        else:
            letters.extend([[3,8],[3,9]]) # AM

        if (0 <= minute < 3) or (57 < minute <= 60):
            letters.extend([[8,7],[8,8],[8,9],[8,10],[8,11],[8,12]]) # OCLOCK

        return letters

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 
    y=top
    #draw_weather()
    array_to_print=update_time()
    index = 0
    get_contrast_color(get_random_color())
    if buttonA.value==True:
        #print("value of button B is",buttonB.value)
        disablebackgroundletter=False
    else:
        disablebackgroundletter=True

    if buttonB.value==False:
        back_text_color=get_random_color()
        fore_text_color=get_contrast_color(back_text_color)
    while index < len(array_to_print):
        if disablebackgroundletter==False:
            _str1=" ".join(letters[index])
            #print("back is: "+back_text_color)
            draw.text((x,y),_str1,font=font,fill=back_text_color)
        x=0
        _str=" ".join(array_to_print[index])
        draw.text((x,y),_str,font=font,fill=fore_text_color)
        #print("text is: "+fore_text_color)
        y += font.getsize(_str)[1]
        index += 1
    y=top

    # Display image.
    disp.image(image, rotation)
    #disp.image(weather)
    time.sleep(1)    

