# Importação das bibliotecas necessárias
import numpy as np
import argparse  # Biblioteca para lidar com argumentos de linha de comando
from utils import ARUCO_DICT  # Importa um dicionário de tipos de tags ArUCo pré-definidos
import cv2  # OpenCV, uma biblioteca para processamento de imagem
import sys

# Criação de um objeto ArgumentParser para lidar com os argumentos de linha de comando
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True, help="caminho para a pasta de saída para salvar a tag ArUCo")
ap.add_argument("-i", "--id", type=int, required=True, help="ID da tag ArUCo a ser gerada")
ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="tipo de tag ArUCo a ser gerada")
ap.add_argument("-s", "--size", type=int, default=200, help="Tamanho da tag ArUCo")
args = vars(ap.parse_args())

# Verifica se o tipo de tag ArUCo especificado é suportado
if ARUCO_DICT.get(args["type"], None) is None:
    print(f"Tipo de tag ArUCo '{args['type']}' não é suportado")
    sys.exit(0)

# Obtém o dicionário de ArUCo correspondente ao tipo especificado
arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[args["type"]])

# Exibe uma mensagem informando o tipo e o ID da tag ArUCo que está sendo gerada
print("Gerando tag ArUCo do tipo '{}' com ID '{}'".format(args["type"], args["id"]))
tag_size = args["size"]

# Cria uma imagem em branco para a tag ArUCo
tag = np.zeros((tag_size, tag_size, 1), dtype="uint8")

# Gera a imagem da tag ArUCo com base no dicionário, ID e tamanho especificados
cv2.aruco.generateImageMarker(arucoDict, args["id"], tag_size, tag, 1)

# Salva a tag gerada em um arquivo
tag_name = f'{args["output"]}/{args["type"]}_id_{args["id"]}.png'
cv2.imwrite(tag_name, tag)

# Exibe a tag ArUCo gerada em uma janela (pode ser fechada com uma tecla)
cv2.imshow("Tag ArUCo", tag)
cv2.waitKey(0)
cv2.destroyAllWindows()
