
from djitellopy import tello
import time
import numpy as np
import cv2
import math


######## PARAMETROS ########
forward_vel = 473.5 / 10 #Vel para frente em cm/s (40cm/s)
angular_vel = 360 / 10 #Vel angular por segundo (36°/s)
intervalo = 1 #Tempo

dIntervalo = forward_vel * intervalo #Distância percorrida
aIntervalo = angular_vel * intervalo
#############################

x, y = 500, 500 #Centraliza o ponto
a = 0
yaw = 0
cmd = 0
drone = tello.Tello()
drone.connect()

pontos = [(0,0), (0,0)]
while cmd != 8:
    cmd
def drawSquare():
    lr, fb, ud, yv = 0, 0, 0, 0

    speed = 50

    aspeed = 40

    global x, y, yaw, a, cmd

    d = 0
    
    if cmd == 1:
     drone.takeoff() 
     time.sleep(3)   
     cmd += 1

    elif cmd == 2: #Vai pra frente
        fb = speed
        d = dIntervalo
        a = 270
        cmd += 1
    
    elif cmd == 3: #Vira anti-horário
        yv = -aspeed
        yaw -= aIntervalo
        cmd += 1

    elif cmd == 4: #Vai pra frente
        fb = speed
        d = dIntervalo
        a = 270
        cmd += 1

    elif cmd == 5: #Vira anti-horário
        yv = -aspeed
        yaw -= aIntervalo
        cmd += 1
    
    elif cmd == 6: #Vai pra frente
        fb = speed
        d = dIntervalo
        a = 270
        cmd += 1
    
    elif cmd == 7: #Vira anti-horário
        yv = -aspeed
        yaw -= aIntervalo
        cmd += 1
    
    elif cmd == 8: #Pousa
        drone.land()

    else:
        drone.land()     
 
    a += yaw

    x += int(d * math.cos(math.radians(a)))

    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]


def desenharPontos(img, points):
    index = 0
    for point in points:
        if index == 2:
            cv2.circle(img, point, 8, (0, 255, 0), cv2.FILLED)
        elif index == (len(points)-1):
            cv2.circle(img, point, 8, (0, 0, 255), cv2.FILLED)
        elif index == 0 or index ==1:
            cv2.circle(img, point, 8, (0, 0, 0), cv2.FILLED)
        else:
            cv2.circle(img, point, 7, (255, 0, 0), cv2.FILLED)
        index += 1
      
    cv2.putText(img, f'({(points[-1][0] - 500) / 100},{(points[-1][1] - 500) / 100})m',

                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1,

                (255, 0, 255), 1)

while True:

    vals = drawSquare()

    image = np.zeros((1000, 1000, 3), np.uint8)

    if pontos[-1][0] != vals[4] or pontos[-1][1] != vals[5]:
        pontos.append((vals[4], vals[5]))

    desenharPontos(image, pontos)

    cv2.imshow("tellodelas", image)

    cv2.waitKey(1)
