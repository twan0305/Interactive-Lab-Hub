# Contributors
1. Ravi Niteesh Voleti(rv279)
2. Tony Wan(tw482)
# Interactive Prototyping: The Clock of Pi

Does it feel like time is moving strangely during this semester?

For our first Pi project, we will pay homage to the [timekeeping devices of old](https://en.wikipedia.org/wiki/History_of_timekeeping_devices) by making simple clocks.

It is worth spending a little time thinking about how you mark time, and what would be useful in a clock of your own design.

**Please indicate anyone you collaborated with on this Lab here.**
Be generous in acknowledging their contributions! And also recognizing any other influences (e.g. from YouTube, Github, Twitter) that informed your design. 

## Prep

Lab Prep is extra long this week. Make sure to start this early for lab on Thursday.

1. ### Set up your Lab 2 Github

Before the start of lab Thursday, [pull changes from the Interactive Lab Hub](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2021Fall/readings/Submitting%20Labs.md#to-pull-lab-updates) so that you have your own copy of Lab 2 on your own lab hub.


  If you are organizing your Lab Hub through folder in local machine, go to terminal, cd into your Interactive-Lab-Hub folder and run:

  ```
  Interactive-Lab-Hub $ git remote add upstream https://github.com/FAR-Lab/Interactive-Lab-Hub.git
  Interactive-Lab-Hub $ git pull upstream Fall2022
  ```
  
  The reason why we are adding a upstream with **course lab-hub** instead of yours is because the local Interactive-Lab-Hub folder is linked with your own git repo already. Try typing ``git remote -v`` and you should see there is the origin branch with your own git repo. We here add the upstream to get latest updates from the teaching team by pulling the **course lab-hub** to your local machine. After your local folder got the latest updates, push them to your remote git repo by running:
  
  ```
  Interactive-Lab-Hub $ git add .
  Interactive-Lab-Hub $ git commit -m "message"
  Interactive-Lab-Hub $ git push
  ```
  Your local and remote should now be up to date with the most recent files.


2. ### Get Kit and Inventory Parts
Prior to the lab session on Thursday, taken inventory of the kit parts that you have, and note anything that is missing:

***Update your [parts list inventory](partslist.md)***

3. ### Prepare your Pi for lab this week
[Follow these instructions](prep.md) to download and burn the image for your Raspberry Pi before lab Thursday.




## Overview
For this assignment, you are going to 

A) [Connect to your Pi](#part-a)  

B) [Try out cli_clock.py](#part-b) 

C) [Set up your RGB display](#part-c)

D) [Try out clock_display_demo](#part-d) 

E) [Modify the code to make the display your own](#part-e)

F) [Make a short video of your modified barebones PiClock](#part-f)

G) [Sketch and brainstorm further interactions and features you would like for your clock for Part 2.](#part-g)

## The Report
This readme.md page in your own repository should be edited to include the work you have done. You can delete everything but the headers and the sections between the \*\*\***stars**\*\*\*. Write the answers to the questions under the starred sentences. Include any material that explains what you did in this lab hub folder, and link it in the readme.

Labs are due on Mondays. Make sure this page is linked to on your main class hub page.

## Part A. 
### Connect to your Pi
Just like you did in the lab prep, ssh on to your pi. Once you get there, create a Python environment by typing the following commands.

```
ssh pi@<your Pi's IP address>
...
pi@ixe00:~ $ virtualenv circuitpython
pi@ixe00:~ $ source circuitpython/bin/activate
(circuitpython) pi@ixe00:~ $ 

```
### Setup Personal Access Tokens on GitHub
The support for password authentication of GitHub was removed on August 13, 2021. That is, in order to link and sync your own lab-hub repo with your Pi, you will have to set up a "Personal Access Tokens" to act as the password for your GitHub account on your Pi when using git command, such as `git clone` and `git push`.

Following the steps listed [here](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) from GitHub to set up a token. Depends on your preference, you can set up and select the scopes, or permissions, you would like to grant the token. This token will act as your GitHub password later when you use the terminal on your Pi to sync files with your lab-hub repo.


## Part B. 
### Try out the Command Line Clock
Clone your own lab-hub repo for this assignment to your Pi and change the directory to Lab 2 folder (remember to replace the following command line with your own GitHub ID):

```
(circuitpython) pi@ixe00:~$ git clone https://github.com/<YOURGITID>/Interactive-Lab-Hub.git
(circuitpython) pi@ixe00:~$ cd Interactive-Lab-Hub/Lab\ 2/
```
Depends on the setting, you might be asked to provide your GitHub user name and password. Remember to use the "Personal Access Tokens" you just set up as the password instead of your account one!


Install the packages from the requirements.txt and run the example script `cli_clock.py`:

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ pip install -r requirements.txt
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ python cli_clock.py 
02/24/2021 11:20:49
```

The terminal should show the time, you can press `ctrl-c` to exit the script.
If you are unfamiliar with the Python code in `cli_clock.py`, have a look at [this Python refresher](https://hackernoon.com/intermediate-python-refresher-tutorial-project-ideas-and-tips-i28s320p). If you are still concerned, please reach out to the teaching staff!


## Part C. 
### Set up your RGB Display
We have asked you to equip the [Adafruit MiniPiTFT](https://www.adafruit.com/product/4393) on your Pi in the Lab 2 prep already. Here, we will introduce you to the MiniPiTFT and Python scripts on the Pi with more details.

<img src="https://cdn-learn.adafruit.com/assets/assets/000/082/842/large1024/adafruit_products_4393_iso_ORIG_2019_10.jpg" height="200" />

The Raspberry Pi 3 has a variety of interfacing options. When you plug the pi in the red power LED turns on. Any time the SD card is accessed the green LED flashes. It has standard USB ports and HDMI ports. Less familiar it has a set of 20x2 pin headers that allow you to connect a various peripherals.

<img src="https://maker.pro/storage/g9KLAxU/g9KLAxUiJb9e4Zp1xcxrMhbCDyc3QWPdSunYAoew.png" height="400" />

To learn more about any individual pin and what it is for go to [pinout.xyz](https://pinout.xyz/pinout/3v3_power) and click on the pin. Some terms may be unfamiliar but we will go over the relevant ones as they come up.

### Hardware (you have done this in the prep)

From your kit take out the display and the [Raspberry Pi 3](https://cdn-shop.adafruit.com/970x728/3775-07.jpg)

Line up the screen and press it on the headers. The hole in the screen should match up with the hole on the raspberry pi.

<p float="left">
<img src="https://cdn-learn.adafruit.com/assets/assets/000/087/539/medium640/adafruit_products_4393_quarter_ORIG_2019_10.jpg?1579991932" height="200" />
<img src="https://cdn-learn.adafruit.com/assets/assets/000/082/861/original/adafruit_products_image.png" height="200">
</p>

### Testing your Screen

The display uses a communication protocol called [SPI](https://www.circuitbasics.com/basics-of-the-spi-communication-protocol/) to speak with the raspberry pi. We won't go in depth in this course over how SPI works. The port on the bottom of the display connects to the SDA and SCL pins used for the I2C communication protocol which we will cover later. GPIO (General Purpose Input/Output) pins 23 and 24 are connected to the two buttons on the left. GPIO 22 controls the display backlight.

We can test it by typing 
```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ python screen_test.py
```

You can type the name of a color then press either of the buttons on the MiniPiTFT to see what happens on the display! You can press `ctrl-c` to exit the script. Take a look at the code with
```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ cat screen_test.py
```

#### Displaying Info with Texts
You can look in `stats.py` for how to display text on the screen!

#### Displaying an image

You can look in `image.py` for an example of how to display an image on the screen. Can you make it switch to another image when you push one of the buttons?



## Part D. 
### Set up the Display Clock Demo
Work on `screen_clock.py`, try to show the time by filling in the while loop (at the bottom of the script where we noted "TODO" for you). You can use the code in `cli_clock.py` and `stats.py` to figure this out.

### How to Edit Scripts on Pi
Option 1. One of the ways for you to edit scripts on Pi through terminal is using [`nano`](https://linuxize.com/post/how-to-use-nano-text-editor/) command. You can go into the `screen_clock.py` by typing the follow command line:
```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ nano screen_clock.py
```
You can make changes to the script this way, remember to save the changes by pressing `ctrl-o` and press enter again. You can press `ctrl-x` to exit the nano mode. There are more options listed down in the terminal you can use in nano.

Option 2. Another way for you to edit scripts is to use VNC on your laptop to remotely connect your Pi. Try to open the files directly like what you will do with your laptop and edit them. Since the default OS we have for you does not come up a python programmer, you will have to install one yourself otherwise you will have to edit the codes with text editor. [Thonny IDE](https://thonny.org/) is a good option for you to install, try run the following command lines in your Pi's ternimal:

  ```
  pi@ixe00:~ $ sudo apt install thonny
  pi@ixe00:~ $ sudo apt update && sudo apt upgrade -y
  ```

Now you should be able to edit python scripts with Thonny on your Pi.



## Part E.
### Modify the barebones clock to make it your own

Does time have to be linear?  How do you measure a year? [In daylights? In midnights? In cups of coffee?](https://www.youtube.com/watch?v=wsj15wPpjLY)

Can you make time interactive? You can look in `screen_test.py` for examples for how to use the buttons.

Please sketch/diagram your clock idea. (Try using a [Verplank digram](http://www.billverplank.com/IxDSketchBook.pdf)!

**We strongly discourage and will reject the results of literal digital or analog clock display.**


\*\*\***A copy of your code should be in your Lab 2 Github repo.**\*\*\*

After you edit and work on the scripts for Lab 2, the files should be upload back to your own GitHub repo! You can push to your personal github repo by adding the files here, commiting and pushing.

```
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ git add .
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ git commit -m 'your commit message here'
(circuitpython) pi@ixe00:~/Interactive-Lab-Hub/Lab 2 $ git push
```

After that, Git will ask you to login to your GitHub account to push the updates online, you will be asked to provide your GitHub user name and password. Remember to use the "Personal Access Tokens" you set up in Part A as the password instead of your account one! Go on your GitHub repo with your laptop, you should be able to see the updated files from your Pi!


## Part F. 
## Make a short video of your modified barebones PiClock

Word clocks are an interesting way to display the time, because they use a clever grid of letters to convert time into words instead of conventional numeric digits. So, for example, if the time is 11:55 am ,it might say “IT IS FIVE MINUTES TO PM TWELVE.” For obvious reasons, that’s more complex then simply showing some numbers. 

#Under the Hood
 STEP 1: INIT
 We first create a 2D array of the letters and leverage the grid system to identify the letters. We call it the "Master Letter Grid"
 
 ```
   0 1 2 3 4 5 6 7 8 9 10 11 12
0  I T R I S U H A L F  T  E  N
1  Q U A R T E R T W E  N  T  Y
2  F I V E Q M I N U T  E  S  T
3  P A S T M T O S A M  O  P  M
4  O N E N T W O Z T H  R  E  E
5  F O U R F I V E S E  V  E  N
6  S I X E I G H T Y N  I  N  E
7  T E N E L E V E N P  H  I  L
8  T W E L V E L O C L  O  C  K
 ```
 For example, if we want to refer the word "IT IS", we would choose (0,0) for I, (0,1) for T , (0,3) for I and (0,4) for S.
 
STEP 2: CONVERT TEXT TO STRING
We extract hours, minutes, am or pm from time and convert them into letters in the array. The minutes are rounded to their near 5th,10th, 15th, 20th , 25th or 30 minute.
  - Until the 33 minute, time is converted reltive to the current hour. From 33rd minute, it is converted relative to the next hour. For example, if the time is 2:17, it would be rendered as "Fifteen Minutes Past PM TWO". If the time is 3:55, it would be rendered as "IT IS FIVE MINUTES TO PM 4".
  - For the first 3 minutes or the last 3 minutes of the hour, the time hour would be appended with the word "OCLOCK". For example: if the time is 4:02 pm, it is represented as "IT IS PM FOUR OCLOCK". The corresponding letters to the time is pushed into a separate array. We call it the "Array To Print"

STEP 3: DISPLAY:
Display is rendered in a two staged process. For example, the time is "4:20pm"

  Stage 1: For every tick we render the "Master Letter Array" in white color 
   ```
   0 1 2 3 4 5 6 7 8 9 10 11 12
0  I T R I S U H A L F  T  E  N
1  Q U A R T E R T W E  N  T  Y
2  F I V E Q M I N U T  E  S  T
3  P A S T M T O S A M  O  P  M
4  O N E N T W O Z T H  R  E  E
5  F O U R F I V E S E  V  E  N
6  S I X E I G H T Y N  I  N  E
7  T E N E L E V E N P  H  I  L
8  T W E L V E L O C L  O  C  K
 ```
  
  Stage 2: Then we superimpose the the "Array To Print" in red color. The overlapping will create the affect.

 ```diff
-    0 1 2 3 4 5 6 7 8 9 10 11 12
- 0  I T   I S                   
- 1                T W E  N  T  Y
- 2            M I N U T  E  S   
- 3  P A S T                 P  M
- 4                              
- 5  F O U R                     
- 6                              
- 7                              
- 8                              
 ```
 Final result is
 
 ![IMG_7334](https://user-images.githubusercontent.com/111998430/189753330-017f5581-9fd8-43ee-b260-5b7e0d02be18.jpg)

Few examples of how time is shown

EXAMPLE 1: when the time is 3:35 pm
![IMG_7330](https://user-images.githubusercontent.com/111998430/189756220-b6146350-4b3f-48a2-9f49-6ff4de936d80.jpg)

EXAMPLE 2: when the time is 4 pm
![IMG_7333](https://user-images.githubusercontent.com/111998430/189756575-731e3216-633a-4650-9f3e-de6bd91a73c3.jpg)

Here is the Video of our clock: https://drive.google.com/file/d/1eYPh8WvP0N6_Vf61NNlKcQ_PHiRWDX21/view?usp=sharing
 
\*\*\***Take a video of your PiClock.**\*\*\*

## Part G. 
## Sketch and brainstorm further interactions and features you would like for your clock for Part 2.
 To ehance this capability further 
 - we want to integrate a button click to change the color of the letters that represent time(on every click a color is chosen from a range of colors).
 - We want to integrate a button click to the change the base color of the letters that do not represent the time (on every click a color is chosen from a range of colors).

# Prep for Part 2

1. Pick up remaining parts for kit on Thursday lab class. Check the updated [parts list inventory](partslist.md) and let the TA know if there is any part missing.
  

2. Look at and give feedback on the Part G. for at least 2 other people in the class (and get 2 people to comment on your Part G!)

# Lab 2 Part 2

Pull Interactive Lab Hub updates to your repo.

Modify the code from last week's lab to make a new visual interface for your new clock. You may [extend the Pi](Extending%20the%20Pi.md) by adding sensors or buttons, but this is not required.

As always, make sure you document contributions and ideas from others explicitly in your writeup.

You are permitted (but not required) to work in groups and share a turn in; you are expected to make equal contribution on any group work you do, and N people's group project should look like N times the work of a single person's lab. What each person did should be explicitly documented. Make sure the page for the group turn in is linked to your Interactive Lab Hub page. 

Gist of the Feedback we received
1. Ability to customize colors
2. Color combinations to be  conteasting
3. ability to remove background letters and only see the time in letters

# Our Approach for incorporating the above feedback

1. We wanted to have a user interaction to let them choose different color combinations based on click on Button B - Tony and Ravi
2. The color combinations that show up needs to contrasting so that user can easily read - Tony

Tony decided to come up with a logic so that the color combination generated is always contrasting.
  - First, we generate a 6 random characters from ```0123456789ABCDEF``` and append them with ```#``` to generate a color
  - Second, we make sure a color is selected from the opp side of the color wheel. To achieve this , we subtract the generated color from ```0xffffff```
  
![Comp _horizontal (1)](https://user-images.githubusercontent.com/111998430/191116544-2bb860ac-e206-4e7b-a24e-6b1109fe39b1.jpg)
 Pic Credits: https://copic.too.com/blogs/educational/analogous-complimentary-and-split-complementary-color-schemes
 
3. On click of button A we only render the "Array To Print" and do not render the "Master Letter Array", persisting the color selection previously made


# Recording of our Lab

https://user-images.githubusercontent.com/111998430/191161713-2de91b91-9303-4c52-ae8d-a58829397a3c.mp4

# User Testing 
User 1: Yongky Arief Kristando <yak6@cornell.edu>

https://user-images.githubusercontent.com/111998430/191157541-d08a9f72-3067-42cc-8d1b-2b36194dee42.mp4

User 2: Rohit George <rg645@cornell.edu>

https://user-images.githubusercontent.com/111998430/191160661-3df3a3b5-fa65-4a79-856a-11a692086a18.mp4



