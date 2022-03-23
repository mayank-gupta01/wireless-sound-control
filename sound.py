import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


cap=cv2.VideoCapture(0)
mphands= mp.solutions.hands
hands=mphands.Hands()
mpDraw=mp.solutions.drawing_utils

while True:
    success,img = cap.read()
    imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results= hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lmList=[]
            for id,lm in enumerate (handLms.landmark):
                #print(id,lm)
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                #print(id, cx ,cy)
                lmList.append([id, cx, cy])
                #print(lmList)
            mpDraw.draw_landmarks(img, handLms,mphands.HAND_CONNECTIONS)

        if lmList:
            x1,y1=lmList[4][1], lmList[4][2]
            x2,y2=lmList[8][1], lmList[8][2]

            cv2.circle(img,(x1,y1),10,(255,5,2),cv2.FILLED)
            cv2.circle(img,(x2,y2),10,(255,5,2),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(24,54,72),3)

            length=math.hypot(x2-x1 , y2-y1)
            print(length)

            if length < 50:
                z1=(x1+x2)//2
                z2=(y1+y2)//2

                cv2.circle(img,(z1,z2),10,(255,5,2),cv2.FILLED)

        volRange=volume.GetVolumeRange()
        minVol=volRange[0]
        maxVol=volRange[1]
        vol=np.interp(length, [50,300],[minVol,maxVol])
        volume.SetMasterVolumeLevel(vol, None)

    cv2.imshow("Image",img)
    cv2.waitKey(1)