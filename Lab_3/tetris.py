import time
import subprocess
import digitalio
import board
import copy
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime
import random
import os
import sys
import speech_recognition as sr


from copy import deepcopy
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
height = disp.height  # we swap height/width to rotate it to landscape!
width = disp.width
image = Image.new("RGB", (disp.width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
#draw.rectangle((width, 0, disp.height, height), outline=0, fill=(0, 0, 0))
disp.image(image)
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


#Colors
disablebackgroundletter=False
number_of_colors = 128
START_CHAR='#'
back_text_color="#FFFFFF"
fore_text_color="#FF0000"


# DECLARE ALL THE CONSTANTS
BOARD_SIZE = 8
# Extra two are for the walls, playing area will have size as BOARD_SIZE
EFF_BOARD_SIZE = BOARD_SIZE + 2

PIECES = [

    [[1], [1], [1], [1]],

    [[1, 0],
     [1, 0],
     [1, 1]],

    [[0, 1],
     [0, 1],
     [1, 1]],

    [[0, 1],
     [1, 1],
     [1, 0]],

    [[1, 1],
     [1, 1]]

]
# Constants for user input
MOVE_LEFT = 'a'
MOVE_RIGHT = 'd'
ROTATE_ANTICLOCKWISE = 'w'
ROTATE_CLOCKWISE = 's'
NO_MOVE = 'e'
QUIT_GAME = 'q'
r = sr.Recognizer()
MyText = "null"

def print_board(board, curr_piece, piece_pos, error_message=''):
    """
    Parameters:
    -----------
    board - matrix of the size of the board
    curr_piece - matrix for the piece active in the game
    piece_pos - [x,y] co-ordinates of the top-left cell in the piece matrix
                w.r.t. the board

    Details:
    --------
    Prints out the board, piece and playing instructions to STDOUT
    If there are any error messages then prints them to STDOUT as well
    """
    os.system('cls' if os.name=='nt' else 'clear')
    print("Text mode version of the TETRIS game\n\n")
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    x=0
    y=top

    board_copy = deepcopy(board)
    curr_piece_size_x = len(curr_piece)
    curr_piece_size_y = len(curr_piece[0])
    _str="hello"
    for i in range(curr_piece_size_x):
        for j in range(curr_piece_size_y):
            board_copy[piece_pos[0]+i][piece_pos[1]+j] = curr_piece[i][j] | board[piece_pos[0]+i][piece_pos[1]+j]

    # Print the board to STDOUT
    for i in range(EFF_BOARD_SIZE):
        x=0
        for j in range(EFF_BOARD_SIZE):
            if board_copy[i][j] == 1:
                #print("*", end='')
                draw.text((x,y),"*",font=font,fill=back_text_color)
                #print("x and y are: ",x,y)
                x += font.getsize("*")[1]
            else:
                #print(" ", end='')
                draw.text((x,y)," ",font=font,fill=back_text_color)
                #print("x and y are: ",x,y)
                #y += font.getsize(" ")[1]
                x += font.getsize(" ")[1]
        #print("")
        y += font.getsize("*")[1]
        #draw.text((x,y),"",font=font,fill=back_text_color)
    disp.image(image)
    #print("Quick play instructions:\n")
    #print(" - a (return): move piece left")
    #print(" - d (return): move piece right")
    #print(" - w (return): rotate piece counter clockwise")
    #print(" - s (return): rotate piece clockwise")

    # In case user doesn't want to alter the position of the piece
    # and he doesn't want to rotate the piece either and just wants to move
    # in the downward direction, he can choose 'f'
    #print(" - e (return): just move the piece downwards as is")
    #print(" - q (return): to quit the game anytime")

    if error_message:
        print(error_message)
    print("value of text is",MyText)



def init_board():
    """
    Parameters:
    -----------
    None

    Returns:
    --------
    board - the matrix with the walls of the gameplay
    """
    board = [[0 for x in range(EFF_BOARD_SIZE)] for y in range(EFF_BOARD_SIZE)]
    for i in range(EFF_BOARD_SIZE):
        board[i][0] = 1
    for i in range(EFF_BOARD_SIZE):
        board[EFF_BOARD_SIZE-1][i] = 1
    for i in range(EFF_BOARD_SIZE):
        board[i][EFF_BOARD_SIZE-1] = 1
    return board


def get_random_piece():
    """
    Parameters:
    -----------
    None

    Returns:
    --------
    piece - a random piece from the PIECES constant declared above
    """
    idx = random.randrange(len(PIECES))
    return PIECES[idx]


def get_random_position(curr_piece):
    """
    Parameters:
    -----------
    curr_piece - piece which is alive in the game at the moment

    Returns:
    --------
    piece_pos - a randomly (along x-axis) chosen position for this piece
    """
    curr_piece_size = len(curr_piece)

    # This x refers to rows, rows go along y-axis
    x = 0
    # This y refers to columns, columns go along x-axis
    y = random.randrange(1, EFF_BOARD_SIZE-curr_piece_size)
    return [x, y]


def is_game_over(board, curr_piece, piece_pos):
    """
    Parameters:
    -----------
    board - matrix of the size of the board
    curr_piece - matrix for the piece active in the game
    piece_pos - [x,y] co-ordinates of the top-left cell in the piece matrix
                w.r.t. the board
    Returns:
    --------
    True - if game is over
    False - if game is live and player can still move
    """
    # If the piece cannot move down and the position is still the first row
    # of the board then the game has ended
    if not can_move_down(board, curr_piece, piece_pos) and piece_pos[0] == 0:
        return True
    return False


def get_left_move(piece_pos):
    """
    Parameters:
    -----------
    piece_pos - position of piece on the board

    Returns:
    --------
    piece_pos - new position of the piece shifted to the left
    """
    # Shift the piece left by 1 unit
    new_piece_pos = [piece_pos[0], piece_pos[1] - 1]
    return new_piece_pos


def get_right_move(piece_pos):
    """
    Parameters:
    -----------
    piece_pos - position of piece on the board

    Returns:
    --------
    piece_pos - new position of the piece shifted to the right
    """
    # Shift the piece right by 1 unit
    new_piece_pos = [piece_pos[0], piece_pos[1] + 1]
    return new_piece_pos


def get_down_move(piece_pos):
    """
    Parameters:
    -----------
    piece_pos - position of piece on the board

    Returns:
    --------
    piece_pos - new position of the piece shifted downward
    """
    # Shift the piece down by 1 unit
    new_piece_pos = [piece_pos[0] + 1, piece_pos[1]]
    return new_piece_pos


def rotate_clockwise(piece):
    """
    Paramertes:
    -----------
    piece - matrix of the piece to rotate

    Returns:
    --------
    piece - Clockwise rotated piece

    Details:
    --------
    We first reverse all the sub lists and then zip all the sublists
    This will give us a clockwise rotated matrix
    """
    piece_copy = deepcopy(piece)
    reverse_piece = piece_copy[::-1]
    return list(list(elem) for elem in zip(*reverse_piece))


def rotate_anticlockwise(piece):
    """
    Paramertes:
    -----------
    piece - matrix of the piece to rotate

    Returns:
    --------
    Anti-clockwise rotated piece

    Details:
    --------
    If we rotate any piece in clockwise direction for 3 times, we would eventually
    get the piece rotated in anti clockwise direction
    """
    piece_copy = deepcopy(piece)
    # Rotating clockwise thrice will be same as rotating anticlockwise :)
    piece_1 = rotate_clockwise(piece_copy)
    piece_2 = rotate_clockwise(piece_1)
    return rotate_clockwise(piece_2)


def merge_board_and_piece(board, curr_piece, piece_pos):
    """
    Parameters:
    -----------
    board - matrix of the size of the board
    curr_piece - matrix for the piece active in the game
    piece_pos - [x,y] co-ordinates of the top-left cell in the piece matrix
                w.r.t. the board

    Returns:
    --------
    None

    Details:
    --------
    Fixes the position of the passed piece at piece_pos in the board
    This means that the new piece will now come into the play

    We also remove any filled up rows from the board to continue the gameplay
    as it happends in a tetris game
    """
    curr_piece_size_x = len(curr_piece)
    curr_piece_size_y = len(curr_piece[0])
    for i in range(curr_piece_size_x):
        for j in range(curr_piece_size_y):
            board[piece_pos[0]+i][piece_pos[1]+j] = curr_piece[i][j] | board[piece_pos[0]+i][piece_pos[1]+j]

    # After merging the board and piece
    # If there are rows which are completely filled then remove those rows

    # Declare empty row to add later
    empty_row = [0]*EFF_BOARD_SIZE
    empty_row[0] = 1
    empty_row[EFF_BOARD_SIZE-1] = 1

    # Declare a constant row that is completely filled
    filled_row = [1]*EFF_BOARD_SIZE

    # Count the total filled rows in the board
    filled_rows = 0
    for row in board:
        if row == filled_row:
            filled_rows += 1

    # The last row is always a filled row because it is the boundary
    # So decrease the count for that one
    filled_rows -= 1

    for i in range(filled_rows):
        board.remove(filled_row)

    # Add extra empty rows on the top of the board to compensate for deleted rows
    for i in range(filled_rows):
        board.insert(0, empty_row)


def overlap_check(board, curr_piece, piece_pos):
    """
    Parameters:
    -----------
    board - matrix of the size of the board
    curr_piece - matrix for the piece active in the game
    piece_pos - [x,y] co-ordinates of the top-left cell in the piece matrix
                w.r.t. the board

    Returns:
    --------
    True - if piece do not overlap with any other piece or walls
    False - if piece overlaps with any other piece or board walls
    """
    curr_piece_size_x = len(curr_piece)
    curr_piece_size_y = len(curr_piece[0])
    for i in range(curr_piece_size_x):
        for j in range(curr_piece_size_y):
            if board[piece_pos[0]+i][piece_pos[1]+j] == 1 and curr_piece[i][j] == 1:
                return False
    return True


def can_move_left(board, curr_piece, piece_pos):
    """
    Parameters:
    -----------
    board - matrix of the size of the board
    curr_piece - matrix for the piece active in the game
    piece_pos - [x,y] co-ordinates of the top-left cell in the piece matrix
                w.r.t. the board

    Returns:
    --------
    True - if we can move the piece left
    False - if we cannot move the piece to the left,
            means it will overlap if we move it to the left
    """
    piece_pos = get_left_move(piece_pos)
    return overlap_check(board, curr_piece, piece_pos)


def can_move_right(board, curr_piece, piece_pos):
    """
    Parameters:
    -----------
    board - matrix of the size of the board
    curr_piece - matrix for the piece active in the game
    piece_pos - [x,y] co-ordinates of the top-left cell in the piece matrix
                w.r.t. the board

    Returns:
    --------
    True - if we can move the piece left
    False - if we cannot move the piece to the right,
            means it will overlap if we move it to the right
    """
    piece_pos = get_right_move(piece_pos)
    return overlap_check(board, curr_piece, piece_pos)


def can_move_down(board, curr_piece, piece_pos):
    """
    Parameters:
    -----------
    board - matrix of the size of the board
    curr_piece - matrix for the piece active in the game
    piece_pos - [x,y] co-ordinates of the top-left cell in the piece matrix
                w.r.t. the board

    Returns:
    --------
    True - if we can move the piece downwards
    False - if we cannot move the piece to the downward direction
    """
    piece_pos = get_down_move(piece_pos)
    return overlap_check(board, curr_piece, piece_pos)


def can_rotate_anticlockwise(board, curr_piece, piece_pos):
    """
    Parameters:
    -----------
    board - matrix of the size of the board
    curr_piece - matrix for the piece active in the game
    piece_pos - [x,y] co-ordinates of the top-left cell in the piece matrix
                w.r.t. the board

    Returns:
    --------
    True - if we can move the piece anti-clockwise
    False - if we cannot move the piece to anti-clockwise
            might happen in case rotating would overlap with any existing piece
    """
    curr_piece = rotate_anticlockwise(curr_piece)
    return overlap_check(board, curr_piece, piece_pos)


def can_rotate_clockwise(board, curr_piece, piece_pos):
    """
    Parameters:
    -----------
    board - matrix of the size of the board
    curr_piece - matrix for the piece active in the game
    piece_pos - [x,y] co-ordinates of the top-left cell in the piece matrix
                w.r.t. the board

    Returns:
    --------
    True - if we can move the piece clockwise
    False - if we cannot move the piece to clockwise
            might happen in case rotating would overlap with any existing piece
    """
    curr_piece = rotate_clockwise(curr_piece)
    return overlap_check(board, curr_piece, piece_pos)

def callback(recognizer, audio):
    global MyText
    try:
        MyText = recognizer.recognize_google(audio)
        MyText = MyText.lower()
        print("Google Speech Recognition thinks you said " +MyText )
        
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def play_game():
    # Initialize the game board, piece and piece position
    global MyText
    board = init_board()
    curr_piece = get_random_piece()
    piece_pos = get_random_position(curr_piece)
    print_board(board, curr_piece, piece_pos)
    move_text=""
    # Get player move from STDIN
    #player_move = input()
    m = sr.Microphone()
    with m as source2:
     r.adjust_for_ambient_noise(source2)
    stop_listening = r.listen_in_background(m, callback)
    while (not is_game_over(board, curr_piece, piece_pos)):
        #player_move = input()
       # player_move = keyboard.read_key(suppress = True)
        #print("you pressed: ",player_move)
        ERR_MSG = ""
        do_move_down = False
        # with sr.Microphone() as source2:
        #     audio2 = r.listen(source2)
        #     MyText = r.recognize_google(audio2)
        #     MyText = MyText.lower()
        #     #move_text=MyText
        print("text is: "+MyText)
        

        if MyText=='left':
            if can_move_left(board, curr_piece, piece_pos):
                piece_pos = get_left_move(piece_pos)
                do_move_down = True
                MyText="null"

            else:
                ERR_MSG = "Cannot move left!"
        elif MyText=='right':
            if can_move_right(board, curr_piece, piece_pos):
                piece_pos = get_right_move(piece_pos)
                do_move_down = True
                MyText="null"
            else:
                ERR_MSG = "Cannot move right!"
        elif MyText=='anti':
            if can_rotate_anticlockwise(board, curr_piece, piece_pos):
                curr_piece = rotate_anticlockwise(curr_piece)
                do_move_down = True
                MyText="null"
            else:
                ERR_MSG = "Cannot rotate anti-clockwise !"
        elif MyText=='rotate':
            if can_rotate_clockwise(board, curr_piece, piece_pos):
                curr_piece = rotate_clockwise(curr_piece)
                do_move_down = True
                MyText="null"
            else:
                ERR_MSG = "Cannot rotate clockwise!"
        elif MyText=='go':
            do_move_down = True
            MyText="null"
        elif MyText=='quit':
            print("Bye. Thank you for playing!")
            sys.exit(0)
        else:
            ERR_MSG = "That is not a valid move!"

        print("can you move down? ",can_move_down(board, curr_piece, piece_pos))
        if  can_move_down(board, curr_piece, piece_pos):
            piece_pos = get_down_move(piece_pos)

        # This means the current piece in the game cannot be moved
        # We have to fix this piece in the board and generate a new piece
        if not can_move_down(board, curr_piece, piece_pos):
            merge_board_and_piece(board, curr_piece, piece_pos)
            curr_piece = get_random_piece()
            piece_pos = get_random_position(curr_piece)

        # Redraw board
        print_board(board, curr_piece, piece_pos, error_message=ERR_MSG)
        time.sleep(1)
        # Get player move from STDIN
        #player_move = input()

    print("GAME OVER!")

play_game()

time.sleep(1)
   
