import cv2 
import numpy as np 
def onMouse(event,x,y,flags,param): 
    if event==cv2.EVENT_LBUTTONDOWN: # 마우스 왼쪽 버튼 클릭 
        if flags & cv2.EVENT_FLAG_SHIFTKEY: 
            cv2.rectangle(param[0],(x-5,y-5),(x+5,y+5),(255,0,0)) 
        else: 
            cv2.circle(param[0],(x,y),5,(255,0,0),3) 
    elif event==cv2.EVENT_RBUTTONDOWN: 
        cv2.circle(param[0],(x,y),5,(0,0,255),3) 
    elif event==cv2.EVENT_LBUTTONDBLCLK: 
        param[0] = np.zeros(shape=param[0].shape,dtype=np.uint8)+255 
    cv2.imshow('img',param[0]) 

img=np.full(shape=(512,512,3),fill_value=255,dtype=np.uint8) 
cv2.imshow('img',img) 
cv2.setMouseCallback('img',onMouse,[img])
cv2.waitKey() 
cv2.destroyAllWindows()

