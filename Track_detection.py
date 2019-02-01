# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 03:38:12 2018

@author: 94779
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 17:59:19 2018

@author: 94779
"""

import cv2  
import numpy as np
import queue
import serial

cha=10#偏差值
oldx=0
oldy=0
flag=0

vel = serial.Serial('/dev/ttyUSB0',9600,timeout=0.05)

def nummake(num):
    hnum=hex(num)
    shnum=str(hnum)
    a=shnum[2:]
    b=a.zfill(2)
    return b
    
    
def gofw(num):
    b=nummake(num)
    vel.write('55 55 05 06 01'+b+'00')
        
def goleft(num):
    b=nummake(num)
    vel.write('55 55 05 06 03'+b+'00')
    
def goright(num):
    b=nummake(num)
    vel.write('55 55 05 06 04'+b+'00')
        

cap = cv2.VideoCapture(0)

width = int(cap.get(3))
height = int(cap.get(4))

print(width,height)


firstFrame = None
lastDec = None
firstThresh = None

feature_params = dict( maxCorners =50 ,
                       qualityLevel = 0.1,
                       minDistance = 7,
                       blockSize = 7 )
 
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
 
color = np.random.randint(0,255,(100,3))
num = 0
 
q_x = queue.Queue(maxsize = 10)
q_y = queue.Queue(maxsize = 10)

while True:
    gofw(2)
    # get a frame
    (grabbed, frame) = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9,9), 3)
    
    
    if firstFrame is None:
        firstFrame = gray
        continue
    # 对两帧图像进行 absdiff 操作
    frameDelta = cv2.absdiff(firstFrame, gray)
    # diff 之后的图像进行二值化
   
    thresh = cv2.adaptiveThreshold(frameDelta,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,7,3)
   
    thresh = cv2.dilate(thresh, None, iterations=2)
 
    # 识别角点
 
    p0 = cv2.goodFeaturesToTrack(thresh, mask = None, **feature_params)
   
    
    if p0 is not None:
        x_sum = 0
        y_sum = 0
        for i, old in enumerate(p0):
            x, y = old.ravel()
            x_sum += x
            y_sum += y
        x_avg = x_sum / len(p0)
        y_avg = y_sum / len(p0)
        if flag!=1:
            while(abs(oldx-x_avg)>=cha):
                if(oldx-x_avg>=0):
                    goleft(1)
                    gofw(1)
                else:
                    goright(1)
                    gofw(1)
                
        oldx=x_avg
        oldy=y_avg
        #print (int(x_avg),int(y_avg))
        #frame = cv2.circle(thresh,(int(x_avg),int(y_avg)),5,(0,255,0),-1)
  
    #cv2.imshow("Security Feed", frame)
    #    firstFrame = gray.copy()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 