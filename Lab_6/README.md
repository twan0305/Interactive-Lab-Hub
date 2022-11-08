# Little Interactions Everywhere


# Team
1. Ravi Niteesh Voleti <rv279@cornell.edu>
2. Tony Wan <tw482@cornell.edu>

## Prep

1. Pull the new changes from the class interactive-lab-hub. (You should be familiar with this already!)
2. Install [MQTT Explorer](http://mqtt-explorer.com/) on your laptop.
3. Readings before class:
   * [MQTT](#MQTT)
   * [The Presence Table](https://dl.acm.org/doi/10.1145/1935701.1935800) and [video](https://vimeo.com/15932020)


## Overview

The point of this lab is to introduce you to distributed interaction. We have included some Natural Language Processing (NLP) and Generation (NLG) but those are not really the emphasis. Feel free to dig into the examples and play around the code which you can integrate into your projects if wanted. However, we want to emphasize that the grading will focus on your ability to develop interesting uses for messaging across distributed devices. Here are the four sections of the lab activity:

A) [MQTT](#part-a)

B) [Send and Receive on your Pi](#part-b)

C) [Streaming a Sensor](#part-c)

D) [The One True ColorNet](#part-d)

E) [Make It Your Own](#part-)

## Part 1.

### Part A
### MQTT

MQTT is a lightweight messaging portal invented in 1999 for low bandwidth networks. It was later adopted as a defacto standard for a variety of [Internet of Things (IoT)](https://en.wikipedia.org/wiki/Internet_of_things) devices. 

#### The Bits

* **Broker** - The central server node that receives all messages and sends them out to the interested clients. Our broker is hosted on the far lab server (Thanks David!) at `farlab.infosci.cornell.edu/8883`. Imagine that the Broker is the messaging center!
* **Client** - A device that subscribes or publishes information to/on the network.
* **Topic** - The location data gets published to. These are *hierarchical with subtopics*. For example, If you were making a network of IoT smart bulbs this might look like `home/livingroom/sidelamp/light_status` and `home/livingroom/sidelamp/voltage`. With this setup, the info/updates of the sidelamp's `light_status` and `voltage` will be store in the subtopics. Because we use this broker for a variety of projects you have access to read, write and create subtopics of `IDD`. This means `IDD/ilan/is/a/goof` is a valid topic you can send data messages to.
*  **Subscribe** - This is a way of telling the client to pay attention to messages the broker sends out on the topic. You can subscribe to a specific topic or subtopics. You can also unsubscribe. Following the previouse example of home IoT smart bulbs, subscribing to `home/livingroom/sidelamp/#` would give you message updates to both the light_status and the voltage.
* **Publish** - This is a way of sending messages to a topic. Again, with the previouse example, you can set up your IoT smart bulbs to publish info/updates to the topic or subtopic. Also, note that you can publish to topics you do not subscribe to. 


**Important note:** With the broker we set up for the class, you are limited to subtopics of `IDD`. That is, to publish or subcribe, the topics will start with `IDD/`. Also, setting up a broker is not much work, but for the purposes of this class, you should all use the broker we have set up for you!


#### Useful Tooling

Debugging and visualizing what's happening on your MQTT broker can be helpful. We like [MQTT Explorer](http://mqtt-explorer.com/). You can connect by putting in the settings from the image below.


![input settings](imgs/mqtt_explorer.png?raw=true)


Once connected, you should be able to see all the messages under the IDD topic. , go to the **Publish** tab and try publish something! From the interface you can send and plot messages as well. Remember, you are limited to subtopics of `IDD`. That is, to publish or subcribe, the topics will start with `IDD/`.

![publish settings](imgs/mqtt_explorer_2.png?raw=true)


### Part B
### Send and Receive on your Pi

[sender.py](./sender.py) and and [reader.py](./reader.py) show you the basics of using the mqtt in python. Let's spend a few minutes running these and seeing how messages are transferred and shown up. Before working on your Pi, keep the connection of `farlab.infosci.cornell.edu/8883` with MQTT Explorer running on your laptop.

**Running Examples on Pi**

* Install the packages from `requirements.txt` under a virtual environment, we will continue to use the `circuitpython` environment we setup earlier this semester:
  ```
  pi@ixe00:~ $ source circuitpython/bin/activate
  (circuitpython) pi@ixe00:~ $ cd Interactive-Lab-Hub/Lab\ 6
  (circuitpython) pi@ixe00:~ Interactive-Lab-Hub/Lab 6 $ pip install -r requirements.txt
  ```
* Run `sender.py`, fill in a topic name (should start with `IDD/`), then start sending messages. You should be able to see them on MQTT Explorer.
  ```
  (circuitpython) pi@ixe00:~ Interactive-Lab-Hub/Lab 6 $ python sender.py
  pi@ReiIDDPi:~/Interactive-Lab-Hub/Lab 6 $ python sender.py
  >> topic: IDD/ReiTesting
  now writing to topic IDD/ReiTesting
  type new-topic to swich topics
  >> message: testtesttest
  ...
  ```
* Run `reader.py`, and you should see any messages being published to `IDD/` subtopics.
  ```
  (circuitpython) pi@ixe00:~ Interactive-Lab-Hub/Lab 6 $ python reader.py
  ...
  ```

**\*\*\*Consider how you might use this messaging system on interactive devices, and draw/write down 5 ideas here.\*\*\***

### 1. Safe Driving Alert System: 
Our Idea is to ensure that the driver uses both his hands while driving. This system will send an alert to the family if the family member drives with a single hand for a specific amount of time or more. To achieve it, We setup 2 touch sensors on the steering wheel, as the driver keeps using both the hands the sensors keeps receiving data. When one hand is removed for a specific amount of time, one of the sensors does not return data. This will trigger an alert to the family.

### Driving with both the hands
<img width="573" alt="Screenshot 2022-11-07 at 10 35 36 PM" src="https://user-images.githubusercontent.com/111998430/200469666-3ac873b5-a746-4ad8-851c-f0aac3ee55cd.png">

### Driving with a single hand

<img width="576" alt="Screenshot 2022-11-07 at 10 35 47 PM" src="https://user-images.githubusercontent.com/111998430/200469665-77891c36-979f-4d0f-9ec9-72f32a39a78f.png">

### Family receives an alert!

<img width="567" alt="Screenshot 2022-11-07 at 10 36 02 PM" src="https://user-images.githubusercontent.com/111998430/200469662-562d3e22-3da3-4fd6-a2d1-755290cdb18c.png">



### 2. EarthQuake Detection System
The idea of this system is to alert all the people in the region before a potential earthquake.Here we setup a device with an accelerometer sensor and place it outside the house. The device keeps receving data and an overall accelaration is calculated. If this value is more than the threshold the system would trigger a high priority alert to all the people, which will help them evacuate during a potential earthquake.

<img width="532" alt="Screenshot 2022-11-07 at 10 41 46 PM" src="https://user-images.githubusercontent.com/111998430/200470319-1b595718-8d4b-4b13-9e36-a60ef2240264.png">

### 3. Trepasser Detection

The idea of this system is to alert the residents of the house when an intruder tries to enter into a house. To achieve this we build a device using a distance sensor which keeps track of the moving objects near the house. If an object keeps coming close and crosses the threshold limit a burglar alert is triggered.

### When an unknown person tries to come close to the house
<img width="577" alt="Screenshot 2022-11-07 at 10 47 39 PM" src="https://user-images.githubusercontent.com/111998430/200470655-3107c117-bc55-4ede-812c-b8070401ceaa.png">

### An alert is sent to the residents

<img width="554" alt="Screenshot 2022-11-07 at 10 48 20 PM" src="https://user-images.githubusercontent.com/111998430/200470733-1e51cfc4-8228-4ccf-a99f-345bf2ad6795.png">


### 4. Patient fall detection in a hospital

The idea is the detect when a patient accidentally falls from their bed and inform the hosiptal staff about the incident. We will use a touch sensor and place it under the bed of the patient. As long as the patient is on the bed there is a constant touch and sensor keep detecting the patient. When they accidentally fall off the sensor does not detect a touch and will send an alert to the hospital staff.

### Patient sleeps on the bed with the sensor

<img width="632" alt="Screenshot 2022-11-07 at 10 54 17 PM" src="https://user-images.githubusercontent.com/111998430/200471448-149035be-10ff-4fc8-9422-a3325284fc76.png">

### When a patient falls off

<img width="614" alt="Screenshot 2022-11-07 at 10 54 30 PM" src="https://user-images.githubusercontent.com/111998430/200471446-3cf6097d-2700-478e-82e8-f7e7eca4406e.png">

### Hospital staff notified

<img width="603" alt="Screenshot 2022-11-07 at 10 54 42 PM" src="https://user-images.githubusercontent.com/111998430/200471444-fdb88632-8a01-480f-bede-fbb538f8a31b.png">

### 5. Military Hands
The idea is that in certain combat enviroments i.e. reconnaissance, silence is a must. Communication with your unit is through standardized hand signals. Our device would be able to recognize the hand signals and give a verbal cues to the rest of the team. 

### Military hand shake

<img width="440" alt="Screenshot 2022-11-08 at 12 35 22 AM" src="https://user-images.githubusercontent.com/111998430/200483569-29b11af8-d05a-43f5-ba1e-a139c69c4d86.png">

### Signalling 

<img width="429" alt="Screenshot 2022-11-08 at 12 35 28 AM" src="https://user-images.githubusercontent.com/111998430/200483579-e5847347-a987-4aec-81c3-ed9cb3268c9a.png">

### Army to react for the signal

<img width="417" alt="Screenshot 2022-11-08 at 12 35 35 AM" src="https://user-images.githubusercontent.com/111998430/200483587-8a45bc7f-a541-479e-bb4c-329b17480db7.png">


### Part C
### Streaming a Sensor

We have included an updated example from [lab 4](https://github.com/FAR-Lab/Interactive-Lab-Hub/tree/Fall2021/Lab%204) that streams the [capacitor sensor](https://learn.adafruit.com/adafruit-mpr121-gator) inputs over MQTT. We will also be running this example under `circuitpython` virtual environment.

Plug in the capacitive sensor board with the Qwiic connector. Use the alligator clips to connect a Twizzler (or any other things you used back in Lab 4) and run the example script:

<p float="left">
<img src="https://cdn-learn.adafruit.com/assets/assets/000/082/842/large1024/adafruit_products_4393_iso_ORIG_2019_10.jpg" height="150" />
<img src="https://cdn-shop.adafruit.com/970x728/4210-02.jpg" height="150">
<img src="https://cdn-learn.adafruit.com/guides/cropped_images/000/003/226/medium640/MPR121_top_angle.jpg?1609282424" height="150"/>
<img src="https://media.discordapp.net/attachments/679721816318803975/823299613812719666/PXL_20210321_205742253.jpg" height="150">
</p>

 ```
 (circuitpython) pi@ixe00:~ Interactive-Lab-Hub/Lab 6 $ python distributed_twizzlers_sender.py
 ...
 ```

**\*\*\*Include a picture of your setup here: what did you see on MQTT Explorer?\*\*\***
![image](https://user-images.githubusercontent.com/111998430/200370650-37ffac66-7991-4cc6-bd58-3f497ac18552.png)


**\*\*\*Pick another part in your kit and try to implement the data streaming with it.\*\*\***


### Part D
### The One True ColorNet

It is with great fortitude and resilience that we shall worship at the altar of the *OneColor*. Through unity of the collective RGB, we too can find unity in our heart, minds and souls. With the help of machines, we can overthrow the bourgeoisie, get on the same wavelength (this was also a color pun) and establish [Fully Automated Luxury Communism](https://en.wikipedia.org/wiki/Fully_Automated_Luxury_Communism).

The first step on the path to *collective* enlightenment, plug the [APDS-9960 Proximity, Light, RGB, and Gesture Sensor](https://www.adafruit.com/product/3595) into the [MiniPiTFT Display](https://www.adafruit.com/product/4393). You are almost there!

<p float="left">
  <img src="https://cdn-learn.adafruit.com/assets/assets/000/082/842/large1024/adafruit_products_4393_iso_ORIG_2019_10.jpg" height="150" />
  <img src="https://cdn-shop.adafruit.com/970x728/4210-02.jpg" height="150">
  <img src="https://cdn-shop.adafruit.com/970x728/3595-03.jpg" height="150">
</p>


The second step to achieving our great enlightenment is to run `color.py`. We have talked about this sensor back in Lab 2 and Lab 4, this script is similar to what you have done before! Remember to ativate the `circuitpython` virtual environment you have been using during this semester before running the script:

 ```
 (circuitpython) pi@ixe00:~ Interactive-Lab-Hub/Lab 6 $ python color.py
 ...
 ```

By running the script, wou will find the two squares on the display. Half is showing an approximation of the output from the color sensor. The other half is up to the collective. Press the top button to share your color with the class. Your color is now our color, our color is now your color. We are one.

(A message from the previous TA, Ilan: I was not super careful with handling the loop so you may need to press more than once if the timing isn't quite right. Also, I haven't load-tested it so things might just immediately break when everyone pushes the button at once.)

You may ask "but what if I missed class?" Am I not admitted into the collective enlightenment of the *OneColor*?

Of course not! You can go to [https://one-true-colornet.glitch.me/](https://one-true-colornet.glitch.me/) and become one with the ColorNet on the inter-webs. Glitch is a great tool for prototyping sites, interfaces and web-apps that's worth taking some time to get familiar with if you have a chance. Its not super pertinent for the class but good to know either way. 

**\*\*\*Can you set up the script that can read the color anyone else publish and display it on your screen?\*\*\***


### Part E
### Make it your own

Find at least one class (more are okay) partner, and design a distributed application together based on the exercise we asked you to do in this lab.

**\*\*\*1. Explain your design\*\*\*** For example, if you made a remote controlled banana piano, explain why anyone would want such a thing.
We are making a seismograph with a three axis accelerometer. A seismograph will detect seismic changes and will alert all the clients about an earthquake.

**\*\*\*2. Diagram the architecture of the system.\*\*\*** Be clear to document where input, output and computation occur, and label all parts and connections. For example, where is the banana, who is the banana player, where does the sound get played, and who is listening to the banana music?

![image](https://user-images.githubusercontent.com/111998430/200377005-b430d97b-2657-4cd5-9ef5-79dc38c6898b.png)


**\*\*\*3. Build a working prototype of the system.\*\*\*** Do think about the user interface: if someone encountered these bananas somewhere in the wild, would they know how to interact with them? Should they know what to expect?

The user would not need to know anything about the system. it is designed to alert the user and no explicit interaction is needed.

**\*\*\*4. Document the working prototype in use.\*\*\*** It may be helpful to record a Zoom session where you should the input in one location clearly causing response in another location.

<!--**\*\*\*5. BONUS (Wendy didn't approve this so you should probably ignore it)\*\*\*** get the whole class to run your code and make your distributed system BIGGER.-->

### DEFINITION
An accelerometer is a device that measures the vibration, or acceleration of motion of a structure. The force caused by vibration or a change in motion (acceleration) causes the mass to "squeeze" the piezoelectric material which produces an electrical charge that is proportional to the force exerted upon it. Since the charge is proportional to the force, and the mass is a constant, then the charge is also proportional to the acceleration.

### How does it work?

An accelerometer works using an electromechanical sensor that is designed to measure either static or dynamic acceleration. Static acceleration is the constant force acting on a body, like gravity or friction. These forces are predictable and uniform to a large extend. For example, the acceleration due to gravity is constant at 9.8m/s, and the gravitation force is almost the same at every point on earth.

Dynamic acceleration forces are non-uniform, and the best example is vibration or shock. A car crash is an excellent example of dynamic acceleration. Here, the acceleration change is sudden when compared to its previous state. The theory behind accelerometers is that they can detect acceleration and convert it into measurable quantities like electrical signals.

Calculate the total accelaration using the below formula.
![image](https://user-images.githubusercontent.com/111998430/200390886-03c76c34-67d9-47a3-b815-6f6000a321d8.png)
 if the total accelaration is above a threshold, it means there is seismic activity.


https://user-images.githubusercontent.com/111998430/200440264-c5226eb4-740c-4231-86e6-6a136c9c437a.mp4
