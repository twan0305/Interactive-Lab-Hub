# Team
1. Ravi Niteesh Voleti <rv279@cornell.edu>
2. Tony Wan <tw482@cornell.edu>
# Chatterboxes
**NAMES OF COLLABORATORS HERE**
[![Watch the video](https://user-images.githubusercontent.com/1128669/135009222-111fe522-e6ba-46ad-b6dc-d1633d21129c.png)](https://www.youtube.com/embed/Q8FWzLMobx0?start=19)

In this lab, we want you to design interaction with a speech-enabled device--something that listens and talks to you. This device can do anything *but* control lights (since we already did that in Lab 1).  First, we want you first to storyboard what you imagine the conversational interaction to be like. Then, you will use wizarding techniques to elicit examples of what people might say, ask, or respond.  We then want you to use the examples collected from at least two other people to inform the redesign of the device.

We will focus on **audio** as the main modality for interaction to start; these general techniques can be extended to **video**, **haptics** or other interactive mechanisms in the second part of the Lab.

## Prep for Part 1: Get the Latest Content and Pick up Additional Parts 

### Pick up Web Camera If You Don't Have One

Students who have not already received a web camera will receive their [IMISES web cameras](https://www.amazon.com/Microphone-Speaker-Balance-Conference-Streaming/dp/B0B7B7SYSY/ref=sr_1_3?keywords=webcam%2Bwith%2Bmicrophone%2Band%2Bspeaker&qid=1663090960&s=electronics&sprefix=webcam%2Bwith%2Bmicrophone%2Band%2Bsp%2Celectronics%2C123&sr=1-3&th=1) on Thursday at the beginning of lab. If you cannot make it to class on Thursday, please contact the TAs to ensure you get your web camera. 

### Get the Latest Content

As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo. There are 2 ways you can do so:

**\[recommended\]**Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the *personal access token* for this.

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2022
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab3 updates"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your your own GitHub repo, [create pull request](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2022Fall/readings/Submitting%20Labs.md) to get updates from the class Interactive-Lab-Hub. After you have latest updates online, go on your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull` to get updates from your own GitHub repo.

## Part 1.

### Text to Speech 

In this part of lab, we are going to start peeking into the world of audio on your Pi! 

We will be using the microphone and speaker on your webcamera. In the home directory of your Pi, there is a folder called `text2speech` containing several shell scripts. `cd` to the folder and list out all the files by `ls`:

```
pi@ixe00:~/text2speech $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav
```

You can run these shell files by typing `./filename`, for example, typing `./espeak_demo.sh` and see what happens. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`. For instance:

```
pi@ixe00:~/text2speech $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Just what do you think you're doing, Dave?" | festival --tts
```

Now, you might wonder what exactly is a `.sh` file? Typically, a `.sh` file is a shell script which you can execute in a terminal. The example files we offer here are for you to figure out the ways to play with audio on your Pi!

You can also play audio files directly with `aplay filename`. Try typing `aplay lookdave.wav`.

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*
(This shell file should be saved to your own repo for this lab.)

Bonus: If this topic is very exciting to you, you can try out this new TTS system we recently learned about: https://github.com/rhasspy/larynx

### Speech to Text

Now examine the `speech2text` folder. We are using a speech recognition engine, [Vosk](https://alphacephei.com/vosk/), which is made by researchers at Carnegie Mellon University. Vosk is amazing because it is an offline speech recognition engine; that is, all the processing for the speech recognition is happening onboard the Raspberry Pi. 

In particular, look at `test_words.py` and make sure you understand how the vocab is defined. 
Now, we need to find out where your webcam's audio device is connected to the Pi. Use `arecord -l` to get the card and device number:
```
pi@ixe00:~/speech2text $ arecord -l
**** List of CAPTURE Hardware Devices ****
card 1: Device [Usb Audio Device], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```
The example above shows a scenario where the audio device is at card 1, device 0. Now, use `nano vosk_demo_mic.sh` and change the `hw` parameter. In the case as shown above, change it to `hw:1,0`, which stands for card 1, device 0.  

Now, look at which camera you have. Do you have the cylinder camera (likely the case if you received it when we first handed out kits), change the `-r 16000` parameter to `-r 44100`. If you have the IMISES camera, check if your rate parameter says `-r 16000`. Save the file using Write Out and press enter.

Then try `./vosk_demo_mic.sh`

\*\***Write your own shell file that verbally asks for a numerical based input (such as a phone number, zipcode, number of pets, etc) and records the answer the respondent provides.**\*\*

### Serving Pages

In Lab 1, we served a webpage with flask. In this lab, you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to `http://<YourPiIPAddress>:5000`. You should be able to see "Hello World" on the webpage.

### Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.) 

\*\***Post your storyboard and diagram here.**\*\*

Write out what you imagine the dialogue to be. Use cards, post-its, or whatever method helps you develop alternatives or group responses. 

![IMG_718923FEC7CA-1](https://user-images.githubusercontent.com/111998430/192426737-5e499407-36a4-4316-a2f7-69236cb93c9e.jpeg)

\*\***Documentation.**\*\*

Technology in video gaming has exploded in the last few years, but the R&D expense and the complexity in programming keeps video games out of reach of many physically disabled gamers . Here is our attempt to create a voice enabled tetris game.

## Phase 1: Tetris Game
  * Step 1: Initialize the board size
  * Step 2: Define shapes and motion
  * Step 3: Define moves a user can perform ( Left, Right, Rotate Clockwise and anticlockwise, quit game)
  * Step 4: Generate a random piece and define a position( co-ordinates in the array when the piece should start)
  * Step 5: Print the board
  * Step 6: Read user input
  * Step 7: Move the piece ensuring game is not over and it does not go beyond the boundaries.
  * Step 8: Seek user input again and perform Step 7
  * Step 9: if the game is over, quit the game.
## Phase 2: Interaction with Audio
  * Step 1: Initialize a recognizer
  * Step 2: Start an infinite loop
  * Step 3: Listen to microphone for about 200 milliseconds
  * Step 4: Using google API to convert audio into text
## Phase 3: Combining Phase 1 and Phase 2
  * Step 1: Instead of taking the input from the keyboard, listen of the voice of the user for 200-300 milliseconds(Phase 1 - Step 6)
  * Step 2: convert Speech into text 
  * Step 3: Based on the text, decide the action
  * Step 4: continue the above steps iteratively till the game is complete.
  
### Acting out the dialogue

Find a partner, and *without sharing the script with your partner* try out the dialogue you've designed, where you (as the device designer) act as the device you are designing.  Please record this interaction (for example, using Zoom's record feature).



https://user-images.githubusercontent.com/111998430/192415475-84163981-590b-4e19-aaeb-09b342e22a05.mp4



\*\***Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**\*\*

### Wizarding with the Pi (optional)
In the [demo directory](./demo), you will find an example Wizard of Oz project. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser.  You may use this demo code as a template. By running the `app.py` script, you can see how audio and sensor data (Adafruit MPU-6050 6-DoF Accel and Gyro Sensor) is streamed from the Pi to a wizard controller that runs in the browser `http://<YouPiIPAddress>:5000`. You can control what the system says from the controller as well!

\*\***Describe if the dialogue seemed different than what you imagined, or when acted out, when it was wizarded, and how.**\*\*

# Lab 3 Part 2

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.


## Prep for Part 2

1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings...
2. What are other modes of interaction _beyond speech_ that you might also use to clarify how to interact?
3. Make a new storyboard, diagram and/or script based on these reflections.

# Feedback received


Yusef Iskandar 

* ```Well done, Ravi. I like the idea and the execution. Would be nice, if you could let the shape move at a constant speed and then give your command.```


## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

*Document how the system works*

<img width="1177" alt="Flowchart" src="https://user-images.githubusercontent.com/111998430/193675127-e31fc4a6-61dd-4df9-a6e0-d2cb9966acd8.png">

# Step 1: Variable Declaration
Board_size, Movements, display are initialized and the game is started
Pieces in the tetris puzzle is defined as below
```MyText``` holds the move converted from audio. initially is set to null.
PIECES = [

    [[1], [1], [1], [1]],  # ****

    [[1, 0],               # *
     [1, 0],               # *
     [1, 1]],              # **

    [[0, 1],               #  *
     [0, 1],               #  *
     [1, 1]],              # **

    [[0, 1],               # *
     [1, 1],               #**
     [1, 0]],              #*

    [[1, 1],               #**
     [1, 1]]               #**
]

Pieces are sub arrays where 1 represents a * and 0 represents space. Through series of spaces and stars a piece is generated.
# Step 2: Board Initialization
 ```init_board()``` first generates the board array from the board size. Effective board size is also calculated to ensure space occupied by the boundaries of the game area is calculated

# Step 3: Piece generation and placement

a piece is generated randomly generated from ```PIECES``` array. this is done through ```get_random_piece()``` function. Once a piece is generated, it has to be placed in a specific position.

```get_random_position(curr_piece)``` , In this a position for x and y are determined. X is always 0 as a piece starts from the top.
```y = random.randrange(1, EFF_BOARD_SIZE-curr_piece_size)``` a random number from 1 to effective board size (including the boundaries) is generated.
The x and y pair is returned.

# Step 4: Print the Board

once board and piece are ready, the board is printed. Sample image of how the board is printed.

<img width="231" alt="image" src="https://user-images.githubusercontent.com/111998430/193678683-a4fecf97-c2ca-45d4-aa87-c011baf8585a.png">

# Step 5: Init Microphone
A microphone is initialized and is running in the background(on a new thread) to capture a move. Everytime the microphone captures a sound it asynchronously updates the ```MyText``` .

# Step 6: Make the move based on the action.

a Gobal variable ```MyText``` always holds the current move which is converted from the audio. If the user does not speak, it automatically checks if the piece can move downwards and moves the piece. If a valid move is recognized, game checks if the move is feasible and performs the move. Once the move is done is checks if the piece can go down and moves the piece downwards.

```
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
        if  can_move_down(board, curr_piece, piece_pos):
            piece_pos = get_down_move(piece_pos)
```


Feedback suggested is incorporated in the below lines of code.
```
if  can_move_down(board, curr_piece, piece_pos):
            piece_pos = get_down_move(piece_pos)
```
            
Rotation is a key implementation, the game offers clockwise and anti clockwise implementation

CLOCKWISE Implementation

```
piece_copy = deepcopy(piece)
    reverse_piece = piece_copy[::-1]
    return list(list(elem) for elem in zip(*reverse_piece))
```
Example:
```
  *              *
  *    ===>  * * *
  **
 ```
ANTICLOCKWISE Implementation
```
piece_copy = deepcopy(piece)
    # Rotating clockwise thrice will be same as rotating anticlockwise :)
    piece_1 = rotate_clockwise(piece_copy)
    piece_2 = rotate_clockwise(piece_1)
    return rotate_clockwise(piece_2)
```

Example:
```
  *              *         * *       * * *
  *    ===>  * * *   ===>    * ===>  *
  **                         *
             Clock        Clock      Clock
             wise 1       wise 2     wise 3
 ```
# Step 7: Continue with the loop

Continue the process until the game is over of user says quit.



*Include videos or screencaptures of both the system and the controller.*

# Video of game without user's voice


https://user-images.githubusercontent.com/111998430/193690328-3125c278-1076-42dc-a77b-7515d4158a96.MOV

# Video with the users interaction


https://user-images.githubusercontent.com/111998430/193691427-0c8ac9fd-adea-4207-b900-5b69d7d1b25f.mp4


## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

# User 1: Krishna Venkata

https://user-images.githubusercontent.com/111998430/193699222-cb6c375b-d342-4db2-801e-5b9c231607e1.mp4

# User 2: Sneha Suresh


https://user-images.githubusercontent.com/111998430/193708939-dc6e0eee-6ad8-4c44-90c1-21be8a414c5a.mp4



Answer the following:
Below is the Gist of user feedback from 2 users

### What worked well about the system and the controller, and what didn't?
Conversion of user voice into a game move went well. Background noise and conversion is a little slow and sometimes not accurate, which is partially because of the way user pronuounces the words

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

The voice recognition system needs lots of testing to ensure user's accent is properly converted.

### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

Voice enabled systems needs to process lot of accents, also when the text does not match we need to build an AI model smart enough to find the nearest action. Once this is achieved, this can be used in a lot of devices, to ensure people with disability can use a lot of appliances without physical interaction. Apart from voice, we can use gesture recognition through eye movement which help disabled people.
