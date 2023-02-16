
'''
Every line is been marked with # at the end of lines, for better understanding the flow
'''

import cv2 #1
import numpy as np #2

def nothing(x):#20
    pass#21

# 0 for first webcame, 1 for second webcam
cap=cv2.VideoCapture(0)#3

#lets create trackbar to adjust the hsv
cv2.namedWindow("Trackbars")#18
#lower hue, with min and max vales of array and call function
cv2.createTrackbar("L-H", "Trackbars", 0, 180, nothing)#19
cv2.createTrackbar("L-S", "Trackbars", 104, 255, nothing)#22 values found using trackbar
cv2.createTrackbar("L-V", "Trackbars", 175, 255, nothing)#23
cv2.createTrackbar("U-H", "Trackbars", 180, 255, nothing)#24
cv2.createTrackbar("U-S", "Trackbars", 226, 255, nothing)#25
cv2.createTrackbar("U-V", "Trackbars", 255, 255, nothing)#26

font = cv2.FONT_HERSHEY_COMPLEX

while True:#4
    # Now we load the frames from webcam
    _, frame = cap.read()#5
    #To converet the color BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#13

    #To vary valuse of trackbacrs 
    l_h =cv2.getTrackbarPos("L-H", "Trackbars")#27
    l_s =cv2.getTrackbarPos("L-S", "Trackbars")#28
    l_v =cv2.getTrackbarPos("L-V", "Trackbars")#29
    u_h =cv2.getTrackbarPos("U-H", "Trackbars")#30
    u_s =cv2.getTrackbarPos("U-S", "Trackbars")#31
    u_v =cv2.getTrackbarPos("U-V", "Trackbars")#32
    
    # Now we need to define the range of hsv, we need to create array (min & max)
    lower_red = np.array([l_h,l_s,l_v])#14
    upper_red = np.array([u_h,u_s,u_v])#15

    #now set the range
    mask = cv2.inRange(hsv,lower_red, upper_red)#16
    kernel = np.ones((5,5), np.uint8)#37 this is just 5x5 smallest pixel to remove noise
    mask = cv2.erode(mask, kernel)#36

    # contour detection after setting HSV for red
    #function returns 2 values we dont need 2nd

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#33

    #we can draw them
    for cnt in contours:#34
        #Area of mask to skip if it is noise
        area = cv2.contourArea(cnt)#43 after this, 35, 40,41,42 will go inside condition 44
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True),True)#39 0.02 will have less side than 0.01 ratio
        x=approx.ravel()[0]#47
        y=approx.ravel()[1]#48
        if area > 400:#44
            #on the frame (0,0,0, is black contour) 5 is thickness ([approx] was cnt before #39
            cv2.drawContours(frame, [approx], 0,(0,0,0),5)#35, afte this we need to remove noise using erroion method on the mask

            print(len(approx))#40
            if len(approx)==3:#51
                cv2.putText(frame, "Triangle",(x,y), font, 1, (0,0,0))#52
                
            elif len(approx)==4:#41
                print("it is a rectangle")#42 if it prints even before deecting then will remove noise by area of mask
                #to put text inside rectangle and x,y pos of 10,10 with font 1 and black color
                cv2.putText(frame, "Rectangle",(x,y), font, 1, (0,0,0))#45 go up

            elif 6<len(approx)<20:#49
                #print("it is a circle")#42 if it prints even before deecting then will remove noise by area of mask
                #to put text inside rectangle and x,y pos of 10,10 with font 1 and black color
                cv2.putText(frame, "Circle",(x,y), font, 1, (0,0,0))#50 go up
    #To show the frames
    cv2.imshow("Frame", frame)#6
    cv2.imshow("Mask", mask)#17
    #cv2.imshow("kernel", kernel)#38 after this we need to approximate the lines of the contour
    # as we would see multiple connecting of lines so we use approximaion method using fun ofcv2

    #To stop the video by pressing any key on keyboard
    key = cv2.waitKey(1)#8
    if key == 27:#9
        break#10

#once we break the look we relaese the cam
cap.release()#11
cv2.destroyAllwindows()#12


