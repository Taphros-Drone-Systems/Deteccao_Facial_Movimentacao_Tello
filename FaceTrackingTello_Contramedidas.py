#Murilo Petegrosso Peres
# Importa-se tudo que está em utlis.py
from utlis import *
import cv2

# Dimensões da imagem
w,h = 360, 240

# Parâmetros kp, kD e kI do PID
pid = [0.5, 0.5, 0]

# Valor inicial do erro anterior
pError = 0

# Para não voar, set o parâmetro abaixo para 1. Para voar, set para 0
startCounter = 0

# Chamamos a função initializeTello dentro de myDrone
myDrone = initializeTello()

# Conecte-se ao Tello via Wifi e execute o script para checar a conexão

# Loop de recepção de frames que darão origem ao vídeo :

while True:
  # Decolagemq
  if startCounter == 0 and myDrone.get_battery() < 20::
    myDrone.takeoff()
    startCounter = 1
  else 
    myDrone.land()
    drone.end
  # Passo 1: Chamada da função que recebe os frames
  img = telloGetFrame(myDrone, w, h)

  # Passo 2: Chamada da função que detecta as faces
  img, info = findFace(img)

  # Passo 3: 
  pError = trackFace(myDrone, info, w, pid, pError)

  # Valor x do nosso ponto central (cx) , assim podemos observá-lo e ver como ele se comporta
  print(info[0][0])

  # Visualização da imagem na tela. O primeiro parâmetro é o nome da janela que irá abrir
  cv2.imshow('Image', img)

  # A tecla Q é usada para cessar a missão
  if cv2.waitKey(1) & 0xFF == ord('q'):
    myDrone.land()
    myDrone.end()
    break
