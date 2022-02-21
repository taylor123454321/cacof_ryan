 #SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

#!/usr/bin/python
#
# NOTE - Only for use on Raspberry Pi or other SBC.
#
import time
import atexit
import threading
import random
import board
from adafruit_motor import stepper as STEPPER
from adafruit_motorkit import MotorKit

# create a default object, no changes to I2C address or frequency
kit = MotorKit(i2c=board.I2C())

# create empty threads (these will hold the stepper 1 and 2 threads)
st1 = threading.Thread()  # pylint: disable=bad-thread-instantiation
st2 = threading.Thread()  # pylint: disable=bad-thread-instantiation


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    kit.stepper1.release()
    kit.stepper2.release()


atexit.register(turnOffMotors)

stepstyles = [STEPPER.SINGLE, STEPPER.DOUBLE, STEPPER.INTERLEAVE, STEPPER.MICROSTEP]


def stepper_worker(stepper, numsteps, direction, style):
    # print("Steppin!")
    for _ in range(numsteps):
        stepper.onestep(direction=direction, style=style)
    # print("Done")


while True:
    if not st1.is_alive():
        randomdir = random.randint(0, 1)
        if randomdir == 0:
            move_dir = STEPPER.FORWARD
        else:
            move_dir = STEPPER.BACKWARD
        randomsteps = 20
        print("%d steps" % randomsteps)
        st1 = threading.Thread(
            target=stepper_worker,
            args=(
                kit.stepper1,
                randomsteps,
                move_dir,
                stepstyles[3],
            ),
        )
        st1.start()

  

    time.sleep(0.3)  # Small delay to stop from constantly polling threads
    # see: https://forums.adafruit.com/viewtopic.php?f=50&t=104354&p=562733#p562733
