#!/usr/bin/env python

import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import time
import os

#Read image
def getPlate(pic):
    
    res = None
    img = cv2.imread(pic)
    print("Unpack ", pic)
    #Convert to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    #Show image
    plt.imshow(cv2.cvtColor(gray,cv2.COLOR_BGR2RGB))
    
    #Bilateral filter -> removes intensity peaks
    bfilter = cv2.bilateralFilter(gray,11,17,17)

    #Edge detection -> only image no points
    edged = cv2.Canny(bfilter, 30, 200)

    #Show image
    #convert from RGB to BGR
    plt.imshow(cv2.cvtColor(edged,cv2.COLOR_BGR2RGB))

    # Find contour points
    keypoints = cv2.findContours(edged.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea,reverse=True)[:10]

    location = None
    for contour in contours:
        # get an approximate shape of contour
        approx = cv2.approxPolyDP(contour, 10 ,True)
        if len(approx) == 4:
            location = approx
            break
    
    # Prepare mask in case data is missing
    mask = np.zeros(gray.shape, np.uint8)
    if location is not None:

        # Draw basic shape where plate is
        new_image = cv2.drawContours(mask, [location], 0 ,255, -1)

        # Leave image where mask is
        new_image = cv2.bitwise_and(img, img, mask=mask)

        #Show image
        #Convert to RGB
        plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))

        (x,y) = np.where(mask==255) #255 -> white
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))

        #crop image at margins of white
        cropped_image = gray[x1:x2+1, y1:y2+1]

        #Show image
        plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_image)
        if len(result) != 0:
            # Select row
            text = result[0][-2]

            # Select font
            font = cv2.FONT_HERSHEY_SIMPLEX

            #put text and rectangle
            res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
            res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
            print(text)
            #Show image
            plt.imshow(res)
    return res

def main():
    plates = []
    timeL = []
    start_time = time.time()
    for filename in os.listdir("./cars_train/"):
        pic = os.path.join("./cars_train/", filename)
        res = getPlate(pic)
        plates.append(res)
        timeL.append(time.time())
    end_time = time.time()
    print(end_time - start_time)

main()
