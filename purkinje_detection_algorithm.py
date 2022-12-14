# -*- coding: utf-8 -*-
"""Purkinje_Detection_Algorithm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TjRCc_9bi2d0KY5u1R7VwMmrKtTLRYqM
"""

import cv2
import numpy as np
import openpyxl
import pandas as pd
import os
from os import listdir

all_points=[]
x_array = []
y_array = []

params2 = cv2.SimpleBlobDetector_Params()
params2.filterByArea = True
params2.minArea = 60

params3 = cv2.SimpleBlobDetector_Params()
params3.filterByConvexity = True
params3.minConvexity = 0.5

params4 = cv2.SimpleBlobDetector_Params()
params4.filterByArea = True
params4.minArea = 30

params5 = cv2.SimpleBlobDetector_Params()
params5.filterByConvexity = True
params5.minConvexity = 0.6




rad1 = []
rad2 = []
flag_1 = False
flag_2 = False
diopters=[4,2.86,2.22,1.82,1.54,1.33,1.18,1.05,0.95]

def mousePoints(event,x,y,flags,params):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(x_array) % 4 == 0:
            print('Pupil Center Coordinates: ', x, y)
        if len(x_array) % 4 == 1:
            print('First Purkinje Image Coordinates: ', x, y)
        if len(x_array) % 4 == 2:
            print('Third Purkinje Image Coordinates: ',x,y)
        if len(x_array) % 4 == 3:
            print('Fourth Purkinje Image Coordinates: ',x,y)
        x_array.append(x)
        y_array.append(y)
        if len(x_array)%4 == 0:
            cv2.destroyAllWindows()


folder_dir = "/Users/ardagulersoy/Downloads/Detector Viewer Screenshots 2"
for images in os.listdir(folder_dir):
        try:
            rad1 = []
            rad2 = []
            flag_1 = False
            flag_2 = False
            print(images)
            frame = cv2.imread(folder_dir+images)
            frame = frame[:-350,:]
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


            # First Point
            mask2 = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)[1]
            mask2 = cv2.erode(mask2, None, iterations=5)
            mask2 = cv2.dilate(mask2, None, iterations=8)
            detector2 = cv2.SimpleBlobDetector_create(params2)
            keypoints2 = detector2.detect(mask2)

            x2 = keypoints2[0].pt[0]
            y2 = keypoints2[0].pt[1]

            new_roi = gray[int(y2) - 180:int(y2) + 350, int(x2) - 400:int(x2) + 400]

            temp= cv2.drawKeypoints(mask2, keypoints2, mask2, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DEFAULT)
            
            # First point

            # Map to the first frame
            mask2 = cv2.threshold(new_roi, 200, 255, cv2.THRESH_BINARY_INV)[1]
            mask2 = cv2.erode(mask2, None, iterations=5)

            mask2 = cv2.dilate(mask2, None, iterations=8)

            detector2 = cv2.SimpleBlobDetector_create(params2)
            keypoints2 = detector2.detect(mask2)
            x3 = keypoints2[0].pt[0]
            y3 = keypoints2[0].pt[1]

            temp= cv2.drawKeypoints(mask2, keypoints2, mask2, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DEFAULT)
            # Map to the first frame

            # Second and Third images

            kernel_sharp = np.array([[0, -1, 0], [-1, 6.6, -1], [0, -1, 0]])
            new_roi_gray = cv2.GaussianBlur(new_roi, (3, 3), 0)
            clahe_img = cv2.filter2D(new_roi_gray, -1, kernel_sharp)


            clahe = cv2.createCLAHE(clipLimit=20, tileGridSize=(18, 18))
            clahe_img = clahe.apply(clahe_img) + 100
            
            clahe_img = cv2.dilate(clahe_img, None, iterations=4)
            clahe_img = cv2.erode(clahe_img, None, iterations=3)
            # _, clahe_img_new = cv2.threshold(clahe_img, 49, 100, cv2.THRESH_BINARY)
            clahe_img_new = cv2.adaptiveThreshold(clahe_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                                cv2.THRESH_BINARY, 65, 65)


            detector3 = cv2.SimpleBlobDetector_create(params3)
            keypoints3 = detector3.detect(clahe_img_new)
            pts3 = cv2.KeyPoint.convert(keypoints3)

            clahe_img_new = cv2.drawKeypoints(clahe_img_new, keypoints3, clahe_img_new, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DEFAULT)
            temp = clahe_img
            # Second and Third images



            print(x2,y2)
            cv2.imshow('Detected',temp)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            
            

            # kernel = np.ones((3, 3), np.uint8)
            # kernel1 = np.ones((3, 3), np.uint8)
            # kernel_sharp = np.array([[0, -1, 0], [-1, 6.6, -1], [0, -1, 0]])
            # kernel_grad = np.ones((8, 8), np.uint8)
            # closing = cv2.morphologyEx(frame, cv2.MORPH_CLOSE, kernel)

            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # height = frame.shape[0]
            # width = frame.shape[1]

            # mask2 = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)[1]

            # mask2 = cv2.erode(mask2, None, iterations=5)
            # mask2 = cv2.dilate(mask2, None, iterations=8)

            # detector2 = cv2.SimpleBlobDetector_create(params2)
            # keypoints2 = detector2.detect(mask2)

            # if (keypoints2==()):
            #     continue
            # # Second image
            # x2 = keypoints2[0].pt[0]
            # y2 = keypoints2[0].pt[1]

            # print(x2,y2)



            # new_roi = gray[int(y2) - 180:int(y2) + 350, int(x2) - 400:int(x2) + 400]

            # mask2 = cv2.threshold(new_roi, 200, 255, cv2.THRESH_BINARY_INV)[1]
            # mask2 = cv2.erode(mask2, None, iterations=5)

            # mask2 = cv2.dilate(mask2, None, iterations=8)

            # detector2 = cv2.SimpleBlobDetector_create(params2)
            # keypoints2 = detector2.detect(mask2)
            # x3 = keypoints2[0].pt[0]
            # y3 = keypoints2[0].pt[1]


            # new_roi_gray = cv2.GaussianBlur(new_roi, (3, 3), 0)
            # clahe_img = cv2.filter2D(new_roi_gray, -1, kernel_sharp)


            # clahe = cv2.createCLAHE(clipLimit=30, tileGridSize=(18, 18))
            # clahe_img = clahe.apply(clahe_img) + 30

            # # _, clahe_img_new = cv2.threshold(clahe_img, 49, 100, cv2.THRESH_BINARY)
            # clahe_img_new = cv2.adaptiveThreshold(clahe_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
            #                                     cv2.THRESH_BINARY, 65, 65)





            # detector3 = cv2.SimpleBlobDetector_create(params3)
            # keypoints3 = detector3.detect(clahe_img_new)
            # pts3 = cv2.KeyPoint.convert(keypoints3)

            # clahe_img_new = cv2.drawKeypoints(clahe_img_new, keypoints3, clahe_img_new, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DEFAULT)

            # new_roi_gray = cv2.GaussianBlur(new_roi, (7, 7), 0)
            # final_img = cv2.dilate(new_roi_gray, kernel1, iterations=2)
            # threshold = cv2.adaptiveThreshold(final_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
            #                                 cv2.THRESH_BINARY_INV, 75, 5)
            # threshold = cv2.erode(threshold, kernel, iterations=4)



            # contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

            # for cnt in contours:
            #     (x, y, w, h) = cv2.boundingRect(cnt)
            #     cv2.ellipse(new_roi, (x + int(w / 2), y + int(h / 2)), (int(w / 2), int(h / 2)), 0., 0., 360, (255, 255, 255))
            #     rad1.append(float(w / 2))
            #     rad2.append(float(h / 2))

            #     break

            # all_points_current=[]
            # all_points_current.append(diopters[d])
            # new_roi = frame[int(y2) - 180:int(y2) + 350, int(x2) - 400:int(x2) + 400]
            # new_roi = cv2.circle(new_roi, ((x + int(w / 2)), (y + int(h / 2))), 4, (255, 0, 0), 1)
            # all_points_current.append(x + int(w / 2))
            # all_points_current.append(y + int(h / 2))
            # new_roi = cv2.circle(new_roi, (int(x3), int(y3)), 10, (0, 0, 255), 1)
            # all_points_current.append(int(x3))
            # all_points_current.append(int(y3))
            # three_four_current=[]



            # for i in range(0, int(pts3.size / 2)):
            #     if ((((int(pts3[i][0]) - (x + int(w / 2))) ** 2) / (rad1[0] ** 2) + ((int(pts3[i][1]) - (y + int(h / 2))) ** 2) / (
            #             rad2[0] ** 2)) < 1 and y3 <= int(pts3[i][1])):

            #         three_four_current.append(int(pts3[i][0]))
            #         three_four_current.append(int(pts3[i][1]))
            # cv2.imshow('Detected',new_roi)
            

            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # all_of=[]
            # if len(three_four_current)!=4:
            #     continue
            # else:
            #     for i in range(0, int(len(three_four_current) / 2)):
            #         new_roi_cropped = clahe_img_new[int(three_four_current[2*i])-20: int(three_four_current[2*i])+20,int(three_four_current[2*i+1])-20: int(three_four_current[2*i+1])+20]
            #         all_of.append(np.mean(new_roi_cropped))
            # min_value=min(all_of)
            # four = all_of.index(min_value)

            # three=1-four
            # new_roi = cv2.circle(new_roi, (int(three_four_current[2*three]), int(three_four_current[2*three+1])), 4, (0, 255, 0), 1)
            # all_points_current.append(three_four_current[2*three])
            # all_points_current.append(three_four_current[2*three+1])
            # new_roi = cv2.circle(new_roi, (int(three_four_current[2*four]), int(three_four_current[2*four+1])), 4, (0, 255, 255), 1)
            # all_points_current.append(three_four_current[2*four])
            # all_points_current.append(three_four_current[2*four+1])

            # print(k)

            # all_points.append(all_points_current)
            # print(all_points_current)

            # cv2.putText(img=new_roi, text="Near distance", org=(40, 60), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(255, 255, 255),thickness=1)
            # cv2.putText(img=new_roi, text="Pupil Center", org=(40, 80), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(255, 0, 0),thickness=1)
            # cv2.putText(img=new_roi, text="First Purkinje", org=(40, 100), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(0, 0, 255),thickness=1)
            # cv2.putText(img=new_roi, text="Third Purkinje", org=(40, 120), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(0, 255, 0),thickness=1)
            # cv2.putText(img=new_roi, text="Fourth Purkinje", org=(40, 140), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(0, 255, 255),thickness=1)
        

        except:
            continue
        
        



