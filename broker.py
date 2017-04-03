#!/usr/bin/env python

import time
import sys
import os
import mosquitto
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
print " Starting broker..."
#GPIO pins setup
#GPIO.setup(7, GPIO.OUT)
#GPIO.setup(22, GPIO.OUT)

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
    print "Bringing up motors"
    power = 1
  elif power == 1:
    print " powering down"
    power = 0
 elif topic_payload[0] == "led":
     print " Led toggle"
 elif topic_payload[0] == "GripOn":
     print " Grip  on"
 elif topic_payload[0] == "GripOff":
     print " Grip off"
 elif topic_payload[0] == "uArmOn":
     print " uArmOn"
 elif topic_payload[0] == "uArmOff":
     print " uArmOff"
 elif topic_payload[0] == "baseUp":
     print " baseUp"
 elif topic_payload[0] == "baseDown":
     print " baseDown"
 elif topic_payload[0] == "baseLeft":
     print " baseLeft"
 elif topic_payload[0] == "baseRight":
     print " baseRight"
 elif topic_payload[0] == "carUp":
     print " carUp"
 elif topic_payload[0] == "carDown":
     print " carDown"
 elif topic_payload[0] == "carLeft":
     print " carLeft"
 elif topic_payload[0] == "carRight":
     print " carRight"

def main():
 broker = "127.0.0.1"
 port = 1883
 topic = "robox/control"

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
  #CTRL+C keyboard interrupt
 except KeyboardInterrupt:
  # resets all GPIO ports used
  GPIO.cleanup()             
  return 4

if __name__ == "__main__":
 sys.exit(main())
