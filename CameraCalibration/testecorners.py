import cv2
import numpy as np
import glob

# Carregue a imagem que contém o tabuleiro de xadrez
images = glob.glob('images2teste/*.jpg')

for image in images:
    img = cv2.imread(image)

# Converta a imagem para tons de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Tente encontrar os cantos do tabuleiro de xadrez
    ret, corners = cv2.findChessboardCorners(gray, (7, 9), None)

if ret:
    # Obtenha as dimensões do tabuleiro
    chessboardSize = (corners.shape[1], corners.shape[0])
    print("Chessboard Size:", chessboardSize)
else:
    print("Corners not found.")
