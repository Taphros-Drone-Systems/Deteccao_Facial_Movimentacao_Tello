from djitellopy import Tello
import cv2

def initializeTello():
    Drone = Tello()
    Drone.connect()
    Drone.for_back_velocity = 0 
    Drone.left_right_velocity = 0
    Drone.up_down_velocity = 0
    Drone.yaw_velocity = 0
    Drone.speed = 0
    print(Drone.get_battery())
    Drone.streamoff()
    Drone.streamon()
    return Drone

def telloGetFrame(Drone, w = 360, h = 240):
    myFrame = Drone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame, (w, h))
    return img

def findFace (img):
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 4)
  
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        myFaceListArea.append(area)
        myFaceListC.append([cx, cy])

    

    return img
        
        

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]

