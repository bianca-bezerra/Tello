from djitellopy import tello
import numpy as np
import cv2
import math
import asyncio
import time

x, y = 500, 500  # Centraliza o ponto
a = 0
yaw = 0
cmd = 0
drone = tello.Tello()
drone.connect()

pontos = [(0, 0), (0, 0)]
timezinho = 6


def drawSquare(image):
  
    global x, y, yaw, a, cmd,timezinho

    d = 0
    cv2.imshow("tellodelas", image)
    time.sleep(1)

    if cmd == 0:
        drone.takeoff()
        time.sleep(5)
        cmd += 1

    elif cmd == 1:  # Vai pra frente

        if timezinho > 0:
            drone.move_forward(20)
            d = 20
            a = 270
            a += yaw
            x += int(d * math.cos(math.radians(a)))
            y += int(d * math.sin(math.radians(a)))
            timezinho -= 1
        else:
            cmd += 1
            timezinho = 6


    elif cmd == 2:  # Vira esquerda
        
        if timezinho > 0:
            drone.move_left(20)
            d = 20
            a = -180
            a += yaw
            x += int(d * math.cos(math.radians(a)))
            y += int(d * math.sin(math.radians(a)))
            timezinho -= 1
        else:
            cmd += 1
            timezinho = 6

    elif cmd == 3:  # Vai pra tras
        
        if timezinho > 0:
            drone.move_back(20)
            d = 20
            a = 90
            a += yaw
            x += int(d * math.cos(math.radians(a)))
            y += int(d * math.sin(math.radians(a)))
            timezinho -= 1
        else:
            cmd += 1
            timezinho = 6

    elif cmd == 4:  # Vira direita
    
        if timezinho > 0:
            drone.move_right(20)
            d = 20
            a = 360
            a += yaw
            x += int(d * math.cos(math.radians(a)))
            y += int(d * math.sin(math.radians(a)))
            timezinho -= 1
        else:
            cmd += 1
            timezinho = 6
            
    elif cmd == 5:  # Pousa
        drone.land()
        print('Deu bom')
        cmd += 1


def desenharPontos(img, points):
    for point in points:
        cv2.circle(img, point, 7, (0, 0, 255), cv2.FILLED, cv2.LINE_8, 0)
    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED, cv2.LINE_4, 0)

    cv2.putText(
        img,
        f'({(points[-1][0] - 500) / 100},{(points[-1][1] - 500) / 100})m',
        (points[-1][0] + 10, points[-1][1] + 30),
        cv2.FONT_HERSHEY_PLAIN,
        1,
        (255, 0, 255),
        1,
    )


while True:
    image = np.zeros((1000, 1000, 3), np.uint8)
    time.sleep(5)
    drawSquare(image)

    if pontos[-1][0] != x or pontos[-1][1] != y:
                pontos.append((x, y))

    desenharPontos(image, pontos)

    cv2.imshow("tellodelas", image)

    cv2.waitKey(5)