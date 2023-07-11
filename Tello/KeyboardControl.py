import KeypressModule as kp
from djitellopy import tello
from time import sleep

kp.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    vel = 100

    if kp.getKey("LEFT"): lr = -vel
    elif kp.getKey("RIGHT"): lr = vel

    if kp.getKey("UP"): fb = vel
    elif kp.getKey("DOWN"): fb = -vel

    if kp.getKey("w"): ud = vel
    elif kp.getKey("s"): ud = -vel

    if kp.getKey("a"): yv = vel
    elif kp.getKey("d"): yv = -vel

    if kp.getKey("q"): drone.land()
    if kp.getKey("e"): drone.takeoff()

    return [lr, fb, ud, yv]

while True:
    vals = getKeyboardInput()
    drone.send_rc_control(vals[0],vals[1],vals[2],vals[3])
    sleep(0.05)
    