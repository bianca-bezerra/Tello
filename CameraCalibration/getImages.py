import cv2

captura = cv2.VideoCapture(0)

num = 0

while captura.isOpened():

    succes, img = captura.read()

    k = cv2.waitKey(5)

    if k == 27:
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('images/img' + str(num) + '.png', img)
        print("image saved!")
        num += 1

    cv2.imshow('Img',img)

# Release and destroy all windows before termination
captura.release()

cv2.destroyAllWindows()