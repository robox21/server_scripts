#!/usr/bin/env python

# INPUT CODES MAPPING
# POWER_ON = 61;
# POWER_OFF = 62;
# LED_LIGHT = 51;
# GRIP_ON = 41;
# GRIP_OFF = 42;
# UPPER_ARM_UP = 31;
# UPPER_ARM_DOWN = 32;       
# ARM_BASE_UP = 21;
# ARM_BASE_DOWN = 22;
# ARM_BASE_LEFT = 22;
# ARM_BASE_RIGHT = 22;
# CAR_UP = 11;
# CAR_DOWN = 12;
# CAR_LEFT = 13;
# CAR_RIGHT = 14;

import time
import sys
import os
import mosquitto
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

print " Starting broker..."

#CAR FORWARD REVERSE
M1A1 = 2
M1A2 = 3 
M1EN = 4

#CAR LEFT RIGHT
M2A1 = 17
M2A2 = 27
M2EN = 22

#GRIP ON OFF
M3A1 = 10
M3A2 = 9
M3EN = 11

#NOT USED
M4A1 = 5
M4A2 = 6
M4EN = 13

#BASE UP DOWN
M5A1 = 21
M5A2 = 26
M5EN = 19

#UPPER ARM UP DOWN
M6A1 = 16
M6A2 = 20
M6EN = 12

#LED
L1=14
L2=15
L3=18

def setupPins() :
    GPIO.setup(M1A1,GPIO.OUT)
    GPIO.setup(M1A2,GPIO.OUT)
    GPIO.setup(M1EN,GPIO.OUT)
    GPIO.setup(M2A1,GPIO.OUT)
    GPIO.setup(M2A2,GPIO.OUT)
    GPIO.setup(M2EN,GPIO.OUT)
    GPIO.setup(M3A1,GPIO.OUT)
    GPIO.setup(M3A2,GPIO.OUT)
    GPIO.setup(M3EN,GPIO.OUT)
    GPIO.setup(M4A1,GPIO.OUT)
    GPIO.setup(M4A2,GPIO.OUT)
    GPIO.setup(M4EN,GPIO.OUT)
    GPIO.setup(M5A1,GPIO.OUT)
    GPIO.setup(M5A2,GPIO.OUT)
    GPIO.setup(M5EN,GPIO.OUT)
    GPIO.setup(M6A1,GPIO.OUT)
    GPIO.setup(M6A2,GPIO.OUT)
    GPIO.setup(M6EN,GPIO.OUT)
    GPIO.setup(L1,GPIO.OUT)
    GPIO.setup(L2,GPIO.OUT)
    GPIO.setup(L3,GPIO.OUT)
    
def motorExecute(Pin1,Pin2,Pin3) :
    GPIO.output(Pin1,GPIO.HIGH)
    GPIO.output(Pin2,GPIO.LOW)
    GPIO.output(Pin3,GPIO.HIGH)
    sleep(1)
    GPIO.output(Pin1,GPIO.LOW)
    GPIO.output(Pin2,GPIO.LOW)
    GPIO.output(Pin3,GPIO.LOW)
    print "Enable %d" % (Pin1);
    print "LOW  : %d" % (Pin2);
    print "HIGH : %d" % (Pin3);
   

def ledExecute(PinNum) :
    print "LED : ";
    print PinNum;

power = 0

#Motor Move execution function
def trigger(x, y):
 GPIO.output(x, 1)
 time.sleep(y)
 GPIO.output(x, 0)
 GPIO.cleanup()
 
def on_message(mqtts, userd, msg):
 topic_payload = []
 topic_payload.append(msg.payload)
 

 if topic_payload[0] == "PowerOn":
  if power == 0:
    print "Bringing up motors" ;
    power = 1
  elif power == 1:
    print " powering down"
    power = 0
 elif topic_payload[0] == "51":
     print " Led toggle"
     
 elif topic_payload[0] == "41":
     print " Grip  on"
     motorExecute(M3EN,M3A1,M3A2)
 elif topic_payload[0] == "42":
     print " Grip off"
     motorExecute(M3EN,M3A2,M3A1)
 elif topic_payload[0] == "31":
     print " uArmUp"
     motorExecute(M6EN,M6A1,M6A2)
 elif topic_payload[0] == "32":
     print " uArmDown"
     motorExecute(M6EN,M6A2,M6A1)
 elif topic_payload[0] == "21":
     print " baseUp"
     motorExecute(M5EN,M5A1,M5A2)
 elif topic_payload[0] == "22":
     print " baseDown"
     motorExecute(M5EN,M5A2,M5A1)
 elif topic_payload[0] == "baseLeft":
     print " baseLeft"
 elif topic_payload[0] == "baseRight":
     print " baseRight"
 elif topic_payload[0] == "11":
     print " carUp"
     motorExecute(M1EN,M1A1,M1A2)
 elif topic_payload[0] == "12":
     print " carDown"
     motorExecute(M1EN,M1A2,M1A1)
 elif topic_payload[0] == "13":
     print " carLeft"
     motorExecute(M2EN,M2A1,M2A2)
 elif topic_payload[0] == "14":
     print " carRight"
     motorExecute(M2EN,M2A2,M2A1)



def main():
 broker = "127.0.0.1"
 port = 1883
 topic = "robox/control"
 setupPins()

 mypid = os.getpid()
 sub_uniq = "subclient_"+str(mypid)
 mqtts = mosquitto.Mosquitto(sub_uniq)
 mqtts.on_message = on_message
 mqtts.connect(broker, port, 60)
 mqtts.subscribe(topic, 0)

 try:
  rc = 0
  while rc == 0:
   rc = mqtts.loop()
  GPIO.cleanup()
  return 0
 except KeyboardInterrupt:
  GPIO.cleanup()             
  return 4

if __name__ == "__main__":
 sys.exit(main())
