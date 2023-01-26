import cv2
import mediapipe as mp
import numpy as np
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands()
mpDraw = mp.solutions.drawing_utils

#pycaw##############################################################
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
#print(volume.GetVolumeRange())
volRange = (volume.GetVolumeRange())
#print(volRange[0])
minVol = volRange[0]
maxVol = volRange[1]
vol=0
volBar=400 
#pycaw################################################################

pTime = 0
cTime = 0


while True:

    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                #print(results.multi_hand_landmarks)
                #print(id,lm)
                # h, w, c = img.shape
                # cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)
                # if id == 0:
                #     cv2.circle(img, (cx, cy), 20, (255, 0 , 255), cv2.FILLED)
                mpDraw.draw_landmarks(img, handLms, mphands.HAND_CONNECTIONS)
        h, w, c = img.shape
        #print(x1,y1)
        x1, y1 = int(handLms.landmark[8].x*w), int(handLms.landmark[8].y*h)
        x2, y2 = int(handLms.landmark[4].x*w), int(handLms.landmark[4].y*h)
        xm, ym = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (xm, ym), 10, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)

        lenght = math.hypot( x2-x1 ,y2-y1)
        #print(lenght)

        vol = np.interp(lenght, [50,300],[minVol,maxVol])
        volBar = np.interp(lenght, [50,300],[400,150])
        print(int(lenght), vol)
        volume.SetMasterVolumeLevel(vol, None)  

        if lenght < 50:
            cv2.circle(img, (xm, ym), 10, (0,255,0), cv2.FILLED)
        if lenght > 300:
            cv2.line(img, (x1,y1), (x2,y2), (0,100,255), 3)

    cv2.rectangle(img, (50,150), (85,400), (0,255,0), 3)
    cv2.rectangle(img, (50,int(volBar)), (85,400), (0,255,0), cv2.FILLED)  
        
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)


    cv2.imshow('Result', img)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break


   