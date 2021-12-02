#!/usr/bin/env python
# coding: utf-8

# In[9]:

import subprocess
import os
import cv2
import time
import mediapipe as mp
import math
from gtts import gTTS
from playsound import playsound


# In[10]:


mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

pTime         = 0
eyes_y         = 0
shoulder_y     = 0
waist_y     = 0
knees_y     = 0
feet_y         = 0


# In[11]:


def map_values(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
  
def min_value(last_value, present_value):
    if (present_value < last_value):
        return present_value
    if (present_value > last_value):
        return last_value
        
def max_value(last_value, present_value):
    if (present_value < last_value):
        return present_value
    if (present_value > last_value):
        return last_value


# In[12]:


while True:
    eyes_distance = 0
    shoulder_distance = 0
    waist_distance = 0
    knees_distance = 0
    feet_distance = 0
    minpoint = 0
    success, img = cap.read(0)
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    speech_txt = 'Fallen person detected'
    language = 'en'
    audiobj = gTTS(text=speech_txt, lang=language, slow=False)
    #audiobj.save("fallen.mp3")
    #print(results.pose_landmarks)
    array_lmy = []
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        #print(str(results.pose_landmarks.landmark))
        eyes_z = 0
        for id, lm in enumerate(results.pose_landmarks.landmark):
            if id == 5:
                eyes_z_before = eyes_z
                eyes_z = lm.z
                eyes_y = lm.y
            
            if id == 12: 
                shoulder_z = lm.z
                shoulder_y = lm.y
            
            if id == 24 :
                waist_z = lm.z
                waist_y = lm.y
                
            if id == 26: 
                knees_z = lm.z
                knees_y = lm.y
            
            if id == 32: 
                feet_z = lm.z
                feet_y = lm.y
            array_lmy.append(lm.y) ########################
            #min(results.pose_landmarks.landmark)
            #print("minimum:",results.pose_landmarks.landmark)            
            
            h, w, c = img.shape
            
            cx, cy = int(w), int(lm.y*h)
            cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)
            
            eyes_distance         = eyes_y*h
            shoulder_distance     = shoulder_y*h
            waist_distance         = waist_y*h
            knees_distance         = knees_y*h
            feet_distance         = feet_y*h
            
            #print("id: ",         id)
            #print("eyes",         eyes_distance)
            #print("shoulder",     shoulder_distance)
            #print("waist",         waist_distance)
            #print("knees",         knees_distance)
            #print("feet",         feet_distance)
            #print("lm_y",lm.y)
            #diference = (feet_distance - eyes_distance)
            #if (diference < 200):              
            #     print("Fallen person")   
            #     cv2.putText(img, str("Fallen person"), (150,150), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
            
            #if (id > 4):
                #print("/neyes_z_before",eyes_z_before)
                #print("/neyes_z",eyes_z)
                #value_min = min_value(-1*eyes_z_before, -1*eyes_z)
                #value_max = max_value(-1*eyes_z_before, -1*eyes_z)
                #print("/nvalue_min",value_min)
                #print("/nvalue_max",value_max)                
                #eyes_new_z = 1
                #eyes_new_z = map_values(-1*eyes_z, value_min, value_max, 1, 10)
                #diference = eyes_distance - feet_distance
                #total = diference/eyes_new_z 
                #print("total", total)
    try:
        minpoint=min(array_lmy)
        #print("MINIMO:",min(array_lmy))
        #cv2.putText(img, str("MIN:"+ str(min(array_lmy))), (190,190), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
    except:
        pass
    difference = (feet_distance - eyes_distance)
    if (difference < 200 and minpoint>0.6):              
                 #print("Fallen person")   
                 cv2.putText(img, str("Fallen person detected"), (150,150), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255), 3)
                 try:
                     os.system("echo 'persona caiida detectada' | festival --tts --language spanish")
                 except:
                     pass
    array_lmy.clear()
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0), 3)
    #cv2.imshow("Image", img)
    
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
