from djitellopy import tello
import cv2

drone = tello.Tello()
drone.connect()
drone.streamon()

while True:
    img = drone.get_frame_read().frame
    frame_colorido = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = cv2.resize(frame_colorido,(360,240))
    cv2.imshow("Imagem",img)
    cv2.waitKey(15)