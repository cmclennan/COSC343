#!/usr/bin/env python3
from ev3dev.ev3 import *
import time as tm

btn = Button()  # will use any button to stop script

ussr = UltrasonicSensor('4')

mB = LargeMotor('outB')
mC = LargeMotor('outC')

mB.run_to_rel_pos(position_sp = 360, speed_sp = 100)
mC.run_to_rel_pos(position_sp = 360, speed_sp = 100)
tm.sleep(2)
mC.run_to_rel_pos(position_sp = 360, speed_sp=200, stop_action="hold")


ts1 = TouchSensor('1')
ts2 = TouchSensor('2')
# Connect EV3 color sensor.
cl = ColorSensor()
colour = 0
count = 1
lock_on = 0
vodka_bottle = 150

Sound.set_volume(100)

# Put the infrared sensor into proximity mode.
ussr.mode = 'US-DIST-CM'
# Put the color sensor into COL-REFLECT mode
# to measure reflected light intensity.
cl.mode = 'COL-REFLECT'

blk = cl.value()
Sound.speak('black is' + str(blk))
tm.sleep(0.5)
# Attach large motors to ports B and C

mB.run_to_rel_pos(position_sp = 240, speed_sp = 100)
mC.run_to_rel_pos(position_sp = 240, speed_sp = 100)
mB.wait_while('running')
mC.wait_while('running')
wht = cl.value()
Sound.speak('white is' + str(wht))
tm.sleep(0.5)

def move_one_blk():
    clr = cl.value()
    while clr <= (blk+8):
        clr = cl.value()
    tm.sleep(0.15)

def move_one_wht():
    clr = cl.value()
    while clr >= (wht-8):
        clr = cl.value()
    tm.sleep(0.15)

#we taught it to count... now it needs to learn to stop
for x in range(2,16):  # exit loop when any button presses
    mB.run_forever(speed_sp=200)
    mC.run_forever(speed_sp=200)
    move_one_blk()
    move_one_wht()
    Sound.speak(str(x))
    if(btn.any()):
        break


mB.stop(stop_action='brake')
mC.stop(stop_action='brake')
tm.sleep(1)
#turn right(or the other right)
mB.run_to_rel_pos(position_sp = 360, speed_sp = -120)
tm.sleep(3)

Sound.speak("I've gotta go fast")
tm.sleep(2)
mB.run_to_rel_pos(position_sp = 3*5*240, speed_sp = 900)
mC.run_to_rel_pos(position_sp = 3**240, speed_sp = 900)
tm.sleep(3)

while not (ts1.value() or ts2.value()):
    distance = ussr.value() / 10
    if distance < vodka_bottle:
        if lock_on == 0:
            Sound.speak('American spy spotted')
            lock_on = 1
        mB.run_forever(speed_sp=200)
        mC.run_forever(speed_sp=200)
    else:
        mB.stop(stop_action='brake')
        mC.stop(stop_action='brake')
        while distance > vodka_bottle:
            distance = ussr.value() / 10
            mC.run_to_rel_pos(position_sp=1080, speed_sp=200, stop_action="hold")
        mC.stop(stop_action='brake')
        lock_on = 0
    tm.sleep(0.1)
Sound.beep()
mB.stop(stop_action='brake')
mC.stop(stop_action='brake')
tm.sleep(1)
Sound.speak("I bring glory to the motherland")
tm.sleep(3)




On Fri, Mar 23, 2018 at 2:24 PM, Mitchie Maluschnig <midgetpie21@gmail.com> wrote:
#!/usr/bin/env python3
# so that script can be run from Brickman
import time as tm
from ev3dev.ev3 import *

us = UltrasonicSensor('4')

ts1 = TouchSensor('1')
ts2 = TouchSensor('2')

mB = LargeMotor('outB')
mC = LargeMotor('outC')
lock_on = 0

# Put the infrared sensor into proximity mode.
us.mode = 'US-DIST-CM'

while not (ts1.value() or ts2.value()):
    distance = us.value()/10
    if distance < 1500:
        if lock_on == 0:
            Sound.speak('Locked on')
            lock_on = 1
        mB.run_forever(speed_sp=200)
        mC.run_forever(speed_sp=200)
    else:
        while distance > 1500:
            mB.run_to_rel_pos(position_sp=1080, speed_sp=200, stop_action="hold")
        mB.stop(stop_action='brake')
        lock_on = 0
    tm.sleep(0.1)
    


On 23 March 2018 at 14:06, Ned Stuitje <ned.stuitje@gmail.com> wrote:
#!/usr/bin/env python3
# so that script can be run from Brickman
import time as tm
from ev3dev.ev3 import *

us = UltrasonicSensor('4')

ts = TouchSensor('1')

mB = LargeMotor('outB')
mC = LargeMotor('outC')

# Put the infrared sensor into proximity mode.
us.mode = 'US-DIST-CM'

while not ts.value():    # Stop program by pressing touch sensor button
    # Infrared sensor in proximity mode will measure distance to the closest
    # object in front of it.
    distance = us.value()/10
    if distance < 10:
        Sound.beep()
    else:
        mB.run_to_rel_pos(position_sp=90, speed_sp=200, stop_action="hold")
        mC.run_to_rel_pos(position_sp=90, speed_sp=200, stop_action="hold")
    tm.sleep(0.1)

