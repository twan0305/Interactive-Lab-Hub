import eventlet
eventlet.monkey_patch()

import time
import board
import busio
#import adafruit_mpu6050
from adafruit_msa3xx import MSA311
import json
import socket

import signal
import sys
from queue import Queue
import numpy as np
import paho.mqtt.client as mqtt
import uuid

 
i2c = busio.I2C(board.SCL, board.SDA)
#mpu = adafruit_mpu6050.MPU6050(i2c)
msa = MSA311(i2c)
ATHRESHOLD  = 15.0      # [gal], threshold to detect earthquake

# Every client needs a random ID
client = mqtt.Client(str(uuid.uuid1()))
# configure network encryption etc
client.tls_set()
# this is the username and pw we have setup for the class
client.username_pw_set('idd', 'device@theFarm')

#connect to the broker
client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)
topic = f"IDD/rv279"
while True:
 a_wait = np.zeros(3)
 print(msa.acceleration)
 a_wait[:]=msa.acceleration
 a_wait_total = np.sqrt(np.sum(a_wait**2))
 print(a_wait_total)
 if a_wait_total > 11:
  client.publish(topic, a_wait_total)
  print("published")
 time.sleep(1)
