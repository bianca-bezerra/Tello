# Importação das bibliotecas necessárias
import numpy as np
from utils import ARUCO_DICT, aruco_display
import argparse
import time
import cv2
import sys

# Criação do analisador de argumentos de linha de comando
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--camera", required=True, help="Set to True if using webcam")
ap.add_argument("-v", "--video", help="Path to the video file")
ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="Type of ArUCo tag to detect")
args = vars(ap.parse_args())

# Inicialização da captura de vídeo, dependendo da entrada da câmera ou do arquivo de vídeo
if args["camera"].lower() == "true":
    video = cv2.VideoCapture(0)
    time.sleep(2.0)
else:
    if args["video"] is None:
        print("[Error] Video file location is not provided")
        sys.exit(1)
    video = cv2.VideoCapture(args["video"])

# Verifica se o tipo de marcador ArUco especificado é suportado
if ARUCO_DICT.get(args["type"], None) is None:
    print(f"ArUCo tag type '{args['type']}' is not supported")
    sys.exit(0)

# Obtém o dicionário de marcadores ArUco e define parâmetros de detecção
arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters_create()

# Loop principal para processar quadros de vídeo
while True:
    ret, frame = video.read()
    
    # Verifica se a captura de vídeo foi bem-sucedida
    if ret is False:
        break

    # Redimensiona o quadro para uma largura fixa, mantendo a proporção
    h, w, _ = frame.shape
    width = 1000
    height = int(width * (h / w))
    frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)

    # Detecta os marcadores ArUco no quadro
    corners, ids, rejected = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)

    # Exibe os marcadores detectados no quadro
    detected_markers = aruco_display(corners, ids, rejected, frame)
    cv2.imshow("Image", detected_markers)

    # Aguarda o pressionamento da tecla 'q' para encerrar o programa
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Fecha a janela e libera o vídeo ou a câmera
cv2.destroyAllWindows()
video.release()
