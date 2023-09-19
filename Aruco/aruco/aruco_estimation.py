'''
Sample Usage:-
python pose_estimation.py --K_Matrix calibration_matrix.npy --D_Coeff distortion_coefficients.npy --type DICT_5X5_100
'''


import numpy as np
import cv2
import sys
from utils import ARUCO_DICT
import argparse
import time
image = np.zeros((320, 240, 3), np.uint8)
cv2.imshow('Estimated Pose', image)
from djitellopy import tello

w,h = 480,360 
fbRange = [6200, 6800]
udRange = [360, 480]
pid = [0.4, 0.4, 0]
pError = 0

def trackAruco(info, w, pid, pError): #Em tese, não precisa modificar essa função
    area = info[1]
    x,y = info[0]
    fb = 0
    ud = 0
    
    error = x - w//2
    velocidade  = pid[0] * error + pid[1] * (error - pError)
    velocidade = int(np.clip(velocidade,-100,100))

    if area > fbRange[0] and area < fbRange[1]: #Stay stacionary
        fb = 0
    elif area > fbRange[1]: #Se tiver muito perto, ele recua
        fb -= 20
    elif area < fbRange[0] and area != 0: #Se estiver longe, continua pra frente
        fb = 20
    
    if area > udRange[0] and area < udRange[1]:
        ud = 0
    elif area > udRange[1]:
        ud -= 20
    elif area < udRange[0]:
        ud += 20

    if x == 0:
        velocidade = 0
        error = 0

    drone.send_rc_control(0,fb,ud,velocidade)
    return error

def pose_estimation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients):

    '''
    frame - Frame from the video stream
    matrix_coefficients - Intrinsic matrix of the calibrated camera
    distortion_coefficients - Distortion coefficients associated with your camera

    return:-
    frame - The frame with the axis drawn on it
    '''

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.aruco_dict = cv2.aruco.getPredefinedDictionary(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters()


    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict,parameters=parameters)
    info = [ [0,0] , 0]
    
        # If markers are detected
    if len(corners) > 0:
        for i in range(0, len(ids)):
            # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, matrix_coefficients,
                                                                       distortion_coefficients)
            # Draw a square around the markers
            cv2.aruco.drawDetectedMarkers(frame, corners)

            '''
            -> Rascunho para identiicar centro e area de cada marcador detectado
            arucoCenter = []
            arucoArea = []
            
            tvec_valores = str(tvec)
            
            tvec_numeros = tvec_valores.strip("[").strip("]").split()
            
            x = float(tvec_numeros[0])
            y = float(tvec_numeros[1])

            cx = x * 10 + w//2
            cy = y * 10 + h//2
            
            area = w * h
            arucoCenter .append([cx,cy])
            arucoArea.append(area)

            if len(arucoArea) != 0:
                i = arucoArea.index(max(arucoArea))

                info = [arucoCenter[i], arucoArea[i]]
            else:

                info = [ [0,0] , 0]
            '''

            
            print("Tvec",tvec)

        for (markerID) in zip(corners, ids):
            print("Marcador detectado: ",markerID)

    return frame


if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-k", "--K_Matrix", required=True, help="Path to calibration matrix (numpy file)")
    ap.add_argument("-d", "--D_Coeff", required=True, help="Path to distortion coefficients (numpy file)")
    ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="Type of ArUCo tag to detect")
    args = vars(ap.parse_args())

    
    if ARUCO_DICT.get(args["type"], None) is None:
        print(f"ArUCo tag type '{args['type']}' is not supported")
        sys.exit(0)

    aruco_dict_type = ARUCO_DICT[args["type"]]
    calibration_matrix_path = args["K_Matrix"]
    distortion_coefficients_path = args["D_Coeff"]
    
    k = np.load(calibration_matrix_path)
    d = np.load(distortion_coefficients_path)

    drone = tello.Tello()
    drone.connect()
    drone.streamon()

    time.sleep(2.0)

    while True:
        frame = drone.get_frame_read().frame

        output = pose_estimation(frame, aruco_dict_type, k, d)


        output_resized = cv2.resize(output,(480,360))
        output_final = cv2.cvtColor(output_resized,cv2.COLOR_BGR2RGB)
        #info = output[1]
        #print(info)
        #pError = trackFace(info, w, pid, pError)

        cv2.imshow('Estimated Pose', output_final)


        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            #drone.land()
            break
            

    cv2.destroyAllWindows()