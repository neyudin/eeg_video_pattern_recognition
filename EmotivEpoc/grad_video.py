#workon cv
import cv2
import numpy as np
import scipy as sp

#faceCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_frontalface_alt.xml')
#faceCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_frontalface_alt2.xml')
#faceCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_frontalface_alt_tree.xml')
eyeCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_eye.xml')
#eyeCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
#eyeCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_lefteye_2splits.xml')#!
#eyeCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_righteye_2splits.xml')#!

video_capture = cv2.VideoCapture(0)
r_opened = 1
l_opened = 1
width = 0
height = 0

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.equalizeHist(gray, gray)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=8,
        minSize=(200, 200),
        maxSize=(1000,1000),
        flags=cv2.CASCADE_SCALE_IMAGE)

    # Draw a rectangle around the faces and eyes
    faces_num = 0
    for (x, y, w, h) in faces:
        faces_num += 1
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y+0.2*h:y+0.55*h, x:x+w]

        ######
        roi = roi_gray.copy()
        roi = cv2.GaussianBlur(roi, (3,3), 0)
        #cv2.medianBlur(roi, 7, roi)
        gradx_roi = cv2.convertScaleAbs(cv2.Sobel(roi, -1, 1, 0, ksize = 3))
        grady_roi = cv2.convertScaleAbs(cv2.Sobel(roi, -1, 0, 1, ksize = 3))
        gradx_roi = cv2.Sobel(roi, -1, 1, 0, ksize = 3)
        grady_roi = cv2.Sobel(roi, -1, 0, 1, ksize = 3)
        roi = cv2.addWeighted(gradx_roi, 1.0, grady_roi, 1.0, 0)
        #thresh = roi.mean() + 0.3 * roi.std()
        #ret, roi = cv2.threshold(roi, thresh, 255, type = 3)
        cv2.imshow('ROI', roi)
        ######
        
        roi_color = frame[y+0.2*h:y+0.55*h, x:x+w]
        eyes = eyeCascade.detectMultiScale(roi_gray,
                                        scaleFactor=1.05,
                                        minNeighbors=8,
                                        minSize=(44, 44),
                                        maxSize=(200,200),
                                        flags=cv2.CASCADE_SCALE_IMAGE)
        if len(eyes) == 2:
            #eyes_num = 02
            r_num = 1
            if eyes[0][0] < eyes[1][0]:
                r_num = 0
            width = max(eyes[0][2], eyes[1][2])
            height = max(eyes[0][3], eyes[1][3])
            width = max(width, height)
            height = width
            yr = max(eyes[r_num][1]+eyes[r_num][3]/2-height/2,0)
            xr = max(eyes[r_num][0]+eyes[r_num][2]/2-width/2,0)
            right_eye_region = roi_gray[yr:yr+height, xr:xr+width]
            yl = max(eyes[1-r_num][1]+eyes[1-r_num][3]/2-height/2,0)
            xl = max(eyes[1-r_num][0]+eyes[1-r_num][2]/2-width/2,0)
            left_eye_region = roi_gray[yl:yl+height, xl:xl+width]
            cv2.rectangle(roi_color,
                    (eyes[r_num][0], eyes[r_num][1]),
                    (eyes[r_num][0] + eyes[r_num][2], eyes[r_num][1] + eyes[r_num][3]),
                    (255, 255, 0),
                    2)#right eye
            cv2.rectangle(roi_color,
                    (eyes[1 - r_num][0], eyes[1 - r_num][1]),
                    (eyes[1 - r_num][0] + eyes[1 - r_num][2], eyes[1 - r_num][1] + eyes[1 - r_num][3]),
                    (255, 0, 255),
                    2)#left eye

            ######
            #Bluring
            right_eye_region = cv2.GaussianBlur(right_eye_region, (3,3), 0)#cv2.getGaussianKernel()
            left_eye_region = cv2.GaussianBlur(left_eye_region, (3,3), 0)#cv2.getGaussianKernel()

            #Sobel operator
            gradx_rer = cv2.convertScaleAbs(cv2.Sobel(right_eye_region, -1, 1, 0, ksize = 3))
            grady_rer = cv2.convertScaleAbs(cv2.Sobel(right_eye_region, -1, 0, 1, ksize = 3))
            gradx_ler = cv2.convertScaleAbs(cv2.Sobel(left_eye_region, -1, 1, 0, ksize = 3))
            grady_ler = cv2.convertScaleAbs(cv2.Sobel(left_eye_region, -1, 0, 1, ksize = 3))
            right_eye_region = cv2.addWeighted(gradx_rer, 0.5, grady_rer, 0.5, 0)
            left_eye_region = cv2.addWeighted(gradx_ler, 0.5, grady_ler, 0.5, 0)
            #thresh = right_eye_region.mean() + 0.3 * right_eye_region.std()
            #ret, right_eye_region = cv2.threshold(right_eye_region, thresh, 255, type = 3)
            #thresh = left_eye_region.mean() + 0.3 * left_eye_region.std()
            #ret, left_eye_region = cv2.threshold(left_eye_region, thresh, 255, type = 3)

            #data = [0 for i in range(len(right_eye_region[0]))]
            #for i in range(len(right_eye_region[0])):
            #    for j in range(len(right_eye_region)):
            #        data[i] += right_eye_region[j][i]
            #print data
            #plt

            cv2.imshow('right', right_eye_region)
            cv2.imshow('left', left_eye_region)
            ######

        if faces_num == 1:
            break

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
