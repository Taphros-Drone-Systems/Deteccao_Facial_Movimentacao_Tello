# Importa-se tudo que está em utlis.py
from utlis import *
import cv2

# Dimensões da imagem
w,h = 360, 240

# Chamamos a função initializeTello dentro de myDrone
myDrone = initializeTello()

# Conecte-se ao Tello via Wifi e execute o script para checar a conexão

# Loop de recepção de frames que darão origem ao vídeo :

while True:

    # Chamada da função que recebe os frames
    img = telloGetFrame(myDrone, w, h)

    # Chamada da função que detecta as faces
    img = findFace(img)

    # Visualização da imagem na tela. O primeiro parâmetro é o nome da janela que irá abrir
    cv2.imshow('Image', img)

    # A tecla Q é usada para cessar a missão
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
    break