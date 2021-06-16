import cv2
import numpy as np
import time
from playsound import playsound
import threading


class Thread1(threading.Thread):
    def run(self) -> None:
        green_light_time = 9
        max_green_light_time = 100
        red_light_time = 40

        isGreen = True
        lights = ['./light/greenlight0.png','./light/greenlight1.png','./light/greenlight2.png','./light/greenlight3.png','./light/greenlight4.png','./light/greenlight5.png','./light/greenlight6.png','./light/greenlight7.png','./light/greenlight8.png','./light/greenlight9.png','./light/greenlight10.png','./light/redlight.png',"./light/orangelight0.png"]
        idx = 0
        is_person_inside = False
        increase_green_light_time = False
        green_light_remaining_time = 1
        isFirst = True
        frame_count_for_blinking_green_light = 0
        minimum_size = 1000

        object_detector = cv2.createBackgroundSubtractorKNN(dist2Threshold=5000) #원래는 1000이였음.
        kernel1 = np.ones((3, 3), np.uint8)
        kernel2 = np.ones((5, 2), np.uint8)
        cap = cv2.VideoCapture("C:/Users/dyl01/OneDrive/바탕 화면/횡단보도 비디오6_Trim.mp4")
        crosswalk_pts = np.array([[166,175],[161,219],[129,255],[77,293],[-4,323],[900,336],[846,298],[820,245],[840,220]])    


        while True:
            ret, frame = cap.read()

            if not ret:
                break          

            frame_count_for_blinking_green_light += 1
            frame = cv2.resize(frame,(960,544))
            mask = object_detector.apply(frame)
            _, mask = cv2.threshold(mask, 200, 255,cv2.THRESH_BINARY)
            mask = cv2.erode(mask, kernel1, iterations = 1)
            mask = cv2.dilate(mask, kernel2, iterations = 8)
            contours, _ = cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if (is_person_inside and increase_green_light_time):
                isGreen=True
                isFirst = False
            
            # 초록불일 때:
            if isGreen:
                cv2.polylines(frame,[crosswalk_pts],isClosed=True,color=(0,255,0),thickness=2) 
                if isFirst:
                    green_start_time = time.time()
                    isFirst = False
                
                green_elapsed_time = time.time() - green_start_time
                # print(green_elapsed_time)

                if (green_elapsed_time < green_light_time) :
                    isGreen = True
                    isFirst = False
                    increase_green_light_time = True
                    green_light_remaining_time = green_light_time - green_elapsed_time

                elif (is_person_inside and (green_elapsed_time <= max_green_light_time)):
                    isGreen = True
                    isFirst = False
                    increase_green_light_time = True
                    green_light_remaining_time = 0

                elif (is_person_inside and (green_elapsed_time > max_green_light_time)):
                    isGreen = False
                    isFirst = True
                    increase_green_light_time = False

                else:
                    isGreen = False
                    isFirst = True
                    increase_green_light_time = False
                
                # 
                isInside =False
                number_of_inside_person = 0
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    x,y,w,h = cv2.boundingRect(cnt)
                    if(area > minimum_size):
                        foot_point = (int((x+x+w)/2),int(y+h)-30)
                        center_point = (int((x+x+w)/2),int((y+y+h)/2))
                        head_point = (int((x+x+w)/2),int(y)+30)               

                        foot_inside = cv2.pointPolygonTest(crosswalk_pts,foot_point,False)
                        center_inside = cv2.pointPolygonTest(crosswalk_pts,center_point,False)
                        head_inside = cv2.pointPolygonTest(crosswalk_pts,head_point,False)

                        isInside = ((foot_inside>=0)or(center_inside>=0)or(head_inside>=0))

                    if (isInside == False):
                        continue
                    else: 
                        number_of_inside_person += 1

                if (number_of_inside_person > 0):
                    is_person_inside = True
                else:
                    is_person_inside = False
        
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    x,y,w,h = cv2.boundingRect(cnt)
                    if(area > minimum_size):
                        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                        foot_point = (int((x+x+w)/2),int(y+h)-30)
                        center_point = (int((x+x+w)/2),int((y+y+h)/2))
                        head_point = (int((x+x+w)/2),int(y)+30)

                        cv2.circle(frame,foot_point,4,(0,255,0),-1)
                        cv2.circle(frame,center_point,4,(0,255,0),-1)
                        cv2.circle(frame,head_point,4,(0,255,0),-1)

                        resized_size = area // int((y+y+h)/2)
                        resized_w = w * 50 // int((y+y+h)/2)
                        resized_h = h * 50 // int((y+y+h)/2)
                        wh_ratio = int(h/w)

                        if (resized_size >= 45) and (wh_ratio < 1):
                            text = str("car")
                        elif (resized_size >= 45) and (wh_ratio >= 1):
                            if (resized_size >= 100):
                                text = str("multiple cars")
                            else:
                                text = str("car")
                        elif (resized_size < 45) and (wh_ratio < 1):
                            text = str("noise")
                        elif (resized_size < 45) and(wh_ratio >= 1):
                            text = str("person")
                        else:
                            text = str("noise")   
                        org = (x,y)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(frame,text,org,font,1,(255,0,0),2) 
                # 


            # 빨간불일 때:
            else:
                cv2.polylines(frame,[crosswalk_pts],isClosed=True,color=(0,0,255),thickness=2) 
                if isFirst:
                    red_start_time = time.time()
                    isFirst = False
                
                red_elapsed_time = time.time() - red_start_time
                # print(red_elapsed_time)

                # 빨간불의 시간이 아직 안 지나간 경우.
                if(red_elapsed_time < red_light_time):
                    isGreen = False
                    isFirst = False
                
                # 빨간불의 시간이 다 지나간 경우.
                else:
                    isGreen = True
                    isFirst = True

            if isGreen:
                if green_light_remaining_time > 9:
                    idx = 10
                elif green_light_remaining_time > 8:
                    idx = 9
                elif green_light_remaining_time > 7:
                    idx = 8
                elif green_light_remaining_time > 6:
                    idx = 7
                elif green_light_remaining_time > 5:
                    idx = 6
                elif green_light_remaining_time > 4:
                    idx = 5
                elif green_light_remaining_time > 3:
                    idx = 4
                elif green_light_remaining_time > 2:
                    idx = 3
                elif green_light_remaining_time > 1:
                    idx = 2
                elif green_light_remaining_time > 0:
                    idx = 1
                else:
                    global sound_player_on 
                    sound_player_on = True
                    if (frame_count_for_blinking_green_light % 20 >= 10):
                        idx = 0
                    else:
                        idx = 12
            else:
                idx = 11

            signal_img =cv2.imread(lights[idx])
            cv2.imshow('signal',signal_img)
        # 
            cv2.imshow("Mask",mask)
            cv2.imshow("Frame",frame)
            
            key = cv2.waitKey(20)
            if key == 27:
                break

        cap.release()
        cap.destroyAllWindows()

class Thread2(threading.Thread):
    def run(self) -> None:
        for i in range(4):
            playsound("./timeout.mp3")

t1 = Thread1()
t1.start()
t2 = Thread2()
t2.start()