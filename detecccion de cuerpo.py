# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 02:27:17 2023

@author: Admin
"""

import cv2
cap = cv2.VideoCapture(0)

human_cascade = cv2.CascadeClassifier('haarcascade_fullbody.Xml')
image = cv2.imread('person.jpg')


while(True):
    ret, frame = cap.read()
    
    if frame is None :
        print("fin del video")
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    humans = human_cascade.detectMultiScale(gray, 1.9, 1)
    
    for(x,y,w,h) in humans:
        cv2.rectangle(frame,(x,y),(x+w,y+h), (0,250,0),2)
        
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
cap.release()
cv2.destroyAllWindows()
            

        
        