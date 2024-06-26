# Importação de bibliotecas necessárias
import numpy as np
import cv2
import sys
from utils import ARUCO_DICT
import argparse
import time

# Função para estimar a pose dos marcadores ArUco
def pose_esitmation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients):
    '''
    frame - Frame from the video stream
    matrix_coefficients - Intrinsic matrix of the calibrated camera
    distortion_coefficients - Distortion coefficients associated with your camera

    return:-
    frame - The frame with the axis drawn on it
    '''
    # Converte a imagem colorida em escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Obtém o dicionário ArUco com base no tipo especificado
    cv2.aruco_dict = cv2.aruco.Dictionary_get(aruco_dict_type)

    # Configuração dos parâmetros de detecção ArUco
    parameters = cv2.aruco.DetectorParameters_create()

    # Detecta marcadores ArUco na imagem
    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(
        gray,
        cv2.aruco_dict,
        parameters=parameters,
        cameraMatrix=matrix_coefficients,
        distCoeff=distortion_coefficients
    )

    # Se marcadores são detectados
    if len(corners) > 0:
        for i in range(0, len(ids)):
            # Estima a pose de cada marcador
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(
                corners[i],
                0.02,  # Tamanho real do marcador em metros
                matrix_coefficients,
                distortion_coefficients
            )

            # Desenha um quadrado ao redor dos marcadores
            cv2.aruco.drawDetectedMarkers(frame, corners)

            # Desenha um sistema de coordenadas tridimensional nos marcadores
            cv2.aruco.drawAxis(frame, matrix_coefficients, distortion_coefficients, rvec, tvec, 0.01)

    return frame

if __name__ == '__main__':
    # Configuração de argumentos de linha de comando
    ap = argparse.ArgumentParser()
    ap.add_argument("-k", "--K_Matrix", required=True, help="Path to calibration matrix (numpy file)")
    ap.add_argument("-d", "--D_Coeff", required=True, help="Path to distortion coefficients (numpy file)")
    ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="Type of ArUCo tag to detect")
    args = vars(ap.parse_args())

    # Verifica se o tipo de marcador ArUco especificado é suportado
    if ARUCO_DICT.get(args["type"], None) is None:
        print(f"ArUCo tag type '{args['type']}' is not supported")
        sys.exit(0)

    # Obtém o tipo de dicionário ArUco
    aruco_dict_type = ARUCO_DICT[args["type"]]
    calibration_matrix_path = args["K_Matrix"]
    distortion_coefficients_path = args["D_Coeff"]

    # Carrega a matriz de calibração e os coeficientes de distorção da câmera
    k = np.load(calibration_matrix_path)
    d = np.load(distortion_coefficients_path)

    # Inicializa a captura de vídeo da câmera
    video = cv2.VideoCapture(0)

    # Aguarda 2 segundos para a câmera estabilizar
    time.sleep(2.0)

    while True:
        # Lê um quadro da câmera
        ret, frame = video.read()

        if not ret:
            break

        # Chama a função para estimar a pose dos marcadores ArUco
        output = pose_esitmation(frame, aruco_dict_type, k, d)

        # Exibe o resultado na janela
        cv2.imshow('Estimated Pose', output)

        # Aguarda uma tecla pressionada e verifica se é 'q' para sair
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    # Libera a captura de vídeo e fecha a janela
    video.release()
    cv2.destroyAllWindows()
