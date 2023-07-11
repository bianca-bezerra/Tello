import KeypressModule as kp
from djitellopy import tello
import time
import numpy as np
import cv2
import math


######## PARAMETROS ########
forward_vel = 473.5 / 10 #Vel para frente em cm/s (40cm/s)
angular_vel = 360 / 10 #Vel angular por segundo (50°/s)
intervalo = 0.25 #Tempo

dIntervalo = forward_vel * intervalo #Distância percorrida
aIntervalo = angular_vel * intervalo
#############################

x, y = 500, 500 #Centraliza o ponto
a = 0
yaw = 0

kp.init()
drone = tello.Tello()
drone.connect()

pontos = [(0,0), (0,0)]

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0

    speed = 40

    aspeed = 50

    global x, y, yaw, a

    d = 0

    if kp.getKey("LEFT"):

        lr = -speed

        d = dIntervalo

        a = -180

    elif kp.getKey("RIGHT"):

        lr = speed

        d = -dIntervalo

        a = 180

    if kp.getKey("UP"):

        fb = speed

        d = dIntervalo

        a = 270

    elif kp.getKey("DOWN"):

        fb = -speed

        d = -dIntervalo

        a = -90

    if kp.getKey("w"):

        ud = speed

    elif kp.getKey("s"):

        ud = -speed

    if kp.getKey("a"):

        yv = -aspeed

        yaw -= aIntervalo

    elif kp.getKey("d"):

        yv = aspeed

        yaw += aIntervalo

    if kp.getKey("q"): drone.land(); time.sleep(3)

    if kp.getKey("e"): drone.takeoff()

    time.sleep(intervalo)

    a += yaw

    x += int(d * math.cos(math.radians(a)))

    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]


def desenharPontos(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)

    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)

    cv2.putText(img, f'({(points[-1][0] - 500) / 100},{(points[-1][1] - 500) / 100})m',

                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1,

                (255, 0, 255), 1)


while True:

    vals = getKeyboardInput()

    drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    image = np.zeros((1000, 1000, 3), np.uint8)

    if pontos[-1][0] != vals[4] or pontos[-1][1] != vals[5]:
        pontos.append((vals[4], vals[5]))

    desenharPontos(image, pontos)

    cv2.imshow("tellodelas", image)

    cv2.waitKey(1)
