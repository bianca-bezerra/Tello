import KeypressModule as kp
from djitellopy import tello
import time
import cv2

kp.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()
global img

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    vel = 50

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

    if kp.getKey("z"): 
        cv2.imwrite(f'Resources/Imagens/{time.time()}.jpg',img)
        time.sleep(0.3)

    return [lr, fb, ud, yv]

while True:
    vals = getKeyboardInput()
    drone.send_rc_control(vals[0],vals[1],vals[2],vals[3])

    img = drone.get_frame_read().frame
    frame_colorido = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = cv2.resize(frame_colorido,(360,240))
    cv2.imshow("Imagem",img)
    cv2.waitKey(10)

    time.sleep(0.05)
    