#!/usr/bin/python3

import time
from gpiozero import MotionSensor
pir = MotionSensor(17)

time.sleep(5)
pir.wait_for_motion()
print("Sneaky Person Alert!!")

