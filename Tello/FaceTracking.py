import cv2
import numpy as np
from djitellopy import tello
import time

drone = tello.Tello()
drone.connect()
drone.streamon()
drone.takeoff()
drone.send_rc_control(0,0,25,0)
time.sleep(2.2)


w,h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0


def acharFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/haar_cascade.xml")
    imgCinza = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgCinza, 1.2, 8)

    myFaceListCenter = []
    myFaceListArea = []

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x + w,y + h),(0,0,255),2)
        cx = x + w//2
        cy = y + h//2
        area = w * h
        cv2.circle(img,(cx,cy),4, (0,255,0), cv2.FILLED)
        myFaceListCenter.append([cx,cy])
        myFaceListArea.append(area)

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))

        return img, [myFaceListCenter[i], myFaceListArea[i]]
    else:

        return img, [ [0,0] , 0]
    
def trackFace(info, w, pid, pError):
    area = info[1]
    x,y = info[0]
    fb = 0
    
    error = x - w//2
    velocidade  = pid[0] * error + pid[1] * (error - pError)
    velocidade = int(np.clip(velocidade,-100,100))

    if area > fbRange[0] and area < fbRange[1]: #Stay stacionary
        fb = 0
    elif area > fbRange[1]: #Se tiver muito perto, ele recua
        fb -= 20
    elif area < fbRange[0] and area != 0: #Se estiver longe, continua pra frente
        fb = 20

    #print(velocidade, fb)

    if x == 0:
        velocidade = 0
        error = 0

    drone.send_rc_control(0,fb,0,velocidade)
    return error

#cap = cv2.VideoCapture(0)

while True:
    #_, img = cap.read()
    img = drone.get_frame_read().frame
    frame_colorido = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = cv2.resize(frame_colorido,(w,h))
    img, info = acharFace(img)
    pError = trackFace(info, w, pid, pError)
    #print("Center", info[0], "Area", info[1])
    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        drone.land()
        break