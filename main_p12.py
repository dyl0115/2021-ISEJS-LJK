# p3에 모폴로지 변환 적용
# roi 지정. 
# 사람의 shape지정.

import cv2
import numpy as np
import time
from playsound import playsound

# 최소 초록불시간(초) 실제는 20
g=6
# 최대 가능 초록불시간(초) 
max_g=100
# 빨간불시간(초) 실제는 66
r=40
# 연장 단위시간(초)
e=1

isGreen=True
lights=['./light/greenlight.jpg','./light/redlight.jpg']
idx=0
isEx=False
increaseGreen=False

# 
play_timeout = False
# 


# 신호등의 신호시간을 카운트할 때, 처음 신호시간을 재는 것인지 알려주는 변수. 이해하기 어려울듯.
isFirst=True

# cap=cv2.VideoCapture("C:/Users/82107/Desktop/횡단보도 비디오4월14일/횡단보도 비디오6.mov")
# cap=cv2.VideoCapture("C:/Users/82107/Desktop/횡단보도 비디오4월14일/횡단보도 비디오6_trim.mp4")
cap=cv2.VideoCapture("C:/Users/dyl01/OneDrive/바탕 화면/횡단보도 비디오6_Trim.mp4")
# cap=cv2.VideoCapture("http://192.168.35.69:4747/video")
# cap=cv2.VideoCapture(0)

# dist2Threshold=7000이었음.
object_detector=cv2.createBackgroundSubtractorKNN(dist2Threshold=5000) #원래는 1000이였음.
kernel1 = np.ones((3, 3), np.uint8)
# (7,5)
kernel2 = np.ones((5, 2), np.uint8)


pts=np.array([[166,175],[161,219],[129,255],[77,293],[-4,323],[900,336],[846,298],[820,245],[840,220]])

# 처음 나갔을 때.
# pts=np.array([[340,380],[320,420],[290,450],[200,477],[870,500],[840,470],[865,425]])
# pts=pts-[170,160]

# 오늘 시도해 볼.(이게 야외였음.)
# pts=np.array([[452,382],[455,405],[448,427],[409,456],[341,478],[253,494],[1069,516],[1031,500],[1000,482],[990,462],[1000,442],[1031,419]])
# pts=pts-[185,120]

# ivcam은 x축은 185만큼, y축은 -80만큼 제외합니다.
# pts=np.array([[679,89],[694,115],[674,204],[644,224],[685,248],[756,257],[785,225],[780,180],[797,120],[824,95]])

# 시작시간:(new)
# start_time=int(time.time())
# 

while True:
    count_in=0
    count_out=0

    FPS_start=time.time()

    # 

    # 

    # 만약 사람이 있으면, 초록불을 연장한다.
    if ((isEx==True)and(increaseGreen==True)):
        isGreen=True
        isFirst=False

    ret, frame=cap.read()
    frame=cv2.resize(frame,(960,544))
    # 횡단보도 ROI다각형 그리기
    # cv2.polylines(frame,[pts],isClosed=True,color=(255,0,0),thickness=2)

    if not ret:
        break
    
    roi=frame[:]
    
    mask=object_detector.apply(roi)
    _, mask =cv2.threshold(mask, 200, 255,cv2.THRESH_BINARY)
    mask = cv2.erode(mask, kernel1, iterations = 1)
    mask = cv2.dilate(mask, kernel2, iterations = 8)

    contours, _=cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 초록불일 때:
    if(isGreen):

        if(isFirst==True):
            green_start_time=time.time()
            isFirst=False
        
        green_current_time=time.time()
        green_elapsed_time=green_current_time-green_start_time
        print(green_elapsed_time)

        # 초록불의 시간이 지나지 않은 경우.
        if(green_elapsed_time<g):
            isGreen=True
            isFirst=False
            increaseGreen=True

        # 초록불 시간은 지났지만, 최대가능 시간을 넘기지 않고, 사람이 존재하는 경우. 
        elif((isEx==True)and(green_elapsed_time<=max_g)):
            isGreen=True
            isFirst=False
            increaseGreen=True
            # playsound("./timeout.mp3")

        # 사람이 존재해도 최대가능 시간을 넘긴 경우. 
        elif((isEx==True)and(green_elapsed_time>max_g)):
            isGreen=False
            isFirst=True
            increaseGreen=False

        # 초록불의 시간도 지나고, 최대가능 시간도 넘긴 경우.
        else:
            isGreen=False
            isFirst=True
            increaseGreen=False

        cv2.polylines(frame,[pts],isClosed=True,color=(0,255,0),thickness=2)
        for cnt in contours:
            area=cv2.contourArea(cnt)
            x,y,w,h=cv2.boundingRect(cnt)

            if((area>1000)):

                cv2.polylines(frame,[cnt],isClosed=True,color=(0,255,0),thickness=1)
                # 모든 물체의 cnt를 구한다.
                # text=str(len(cnt))
                # len_cnt=len(cnt)
                # 사람일 확률 person_p
                # text=str(person_p)
                # text=text
                # org=(x,y)
                # font=cv2.FONT_HERSHEY_SIMPLEX
                # cv2.putText(roi,text,org,font,1,(255,0,0),2)
                cv2.rectangle(roi,(x,y),(x+w,y+h),(0,0,255),2)
                foot_point=(int((x+x+w)/2),int(y+h)-30)
                center_point=(int((x+x+w)/2),int((y+y+h)/2))
                head_point=(int((x+x+w)/2),int(y)+30)

                resized_size=area//int((y+y+h)/2)
                resized_w=w*50//int((y+y+h)/2)
                resized_h=h*50//int((y+y+h)/2)
                wh_ratio=int(h/w)

                if (resized_size>=45)and(wh_ratio<1):
                    text=str("car")
                elif (resized_size>=45)and(wh_ratio>=1):
                    if(resized_size>=100):
                        text=str("car Cluster")
                    else:
                        # 자동차가 세로인경우.
                        # 사람이 세로로 뭉쳐있는 경우.
                        text=str("car")
                elif (resized_size<45)and(wh_ratio<1):
                    text=str("noise")
                elif(resized_size<45)and(wh_ratio>=1):
                    text=str("person")
                else:
                    text=str("noise")

                org=(x,y)
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(roi,text,org,font,1,(255,0,0),2)
                
                cv2.circle(roi,foot_point,4,(0,255,0),-1)
                cv2.circle(roi,center_point,4,(0,255,0),-1)
                cv2.circle(roi,head_point,4,(0,255,0),-1)

                foot_inside=cv2.pointPolygonTest(pts,foot_point,False)
                center_inside=cv2.pointPolygonTest(pts,center_point,False)
                head_inside=cv2.pointPolygonTest(pts,head_point,False)

                isInside=((foot_inside>=0)or(center_inside>=0)or(head_inside>=0))
                # 외부: -1
                # 경계: 0
                # 내부: 1

                # 횡단보도 내에 없는 cnt들
            if(isInside==False):
                continue
            else:
                count_in=count_in+1

        if((count_in>0)):
            isEx=True
        else:
            isEx=False
    
    # 빨간 불일때:
    else:
        cv2.polylines(frame,[pts],isClosed=True,color=(0,0,255),thickness=2)

        if (isFirst==True):
            red_start_time=time.time()
            isFirst=False

        red_current_time=time.time()
        red_elapsed_time=red_current_time-red_start_time
        print(red_elapsed_time)

        # 빨간불의 시간이 아직 안지난 경우.
        if(red_elapsed_time<r):
            isGreen=False
            isFirst=False
        
        # 빨간불의 시간이 다 지나간 경우.
        else:
            isGreen=True
            isFirst=True
            

    if(isGreen==True):
        idx=0
    else:
        idx=1
    
    FPS_end=time.time()
    # print("FPS: ",int(1./FPS_end-FPS_start))

    signal_img=cv2.imread(lights[idx])
    cv2.imshow('signal',signal_img)
    cv2.imshow("Mask",mask)
    cv2.imshow("Frame",frame)
    

    key=cv2.waitKey(20)
    if key==27:
        break

cap.release()
cap.destroyAllWindows()

# print가 들어가면 성능차이를 보인다.