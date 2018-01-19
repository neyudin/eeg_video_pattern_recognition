#workon cv
import cv2
import numpy as np
import scipy as sp
#import matplotlib.pyplot as plt
#import matplotlib.animation
#import time
#plt.ion()
#plt.axis([0,240,0,4000])


#def normcorrcoef(img1, img2):
#    leny = min(len(img1), len(img2))
#    lenx = min(len(img1[0]), len(img2[0]))
#    a = img1[(len(img1)-leny)/2:(len(img1)+leny)/2, (len(img1[0])-lenx)/2:(len(img1[0])+lenx)/2]
#    b = img2[(len(img2)-leny)/2:(len(img2)+leny)/2, (len(img2[0])-lenx)/2:(len(img2[0])+lenx)/2]
#    product = np.mean((a - a.mean()) * (b - b.mean()))
#    stds = a.std() * b.std()
#    if stds == 0:
#        return 0
#    else:
#        product /= stds
#        return product

#faceCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_frontalface_alt.xml')
#faceCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_frontalface_alt2.xml')
#faceCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_frontalface_alt_tree.xml')

video = video_capture = cv2.VideoCapture(0)
fps = video.get(cv2.CAP_PROP_FPS)
first = 1
r_opened = 1
l_opened = 1
r_count = 0
l_count = 0


#ight_template = [[0]]
#left_template = [[0]]
#right_corr = 1.0
#left_corr = 1.0
#threshold = 0.74
threshold = 74

print 'Please, do not close your eyes'
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #byr = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
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
        #ey = y + int(0.3 * h)
        ey = y + int(0.32 * h)
        ew = int(0.24 * w)
        #eh = int(0.2 * h)
        eh = int(0.12 * h)
        eyes1 = [[x+int(0.18*w), ey, ew, eh], [x+int(0.58*w), ey, ew, eh]]
        cv2.rectangle(frame, (eyes1[0][0], eyes1[0][1]), (eyes1[0][0]+eyes1[0][2], eyes1[0][1]+eyes1[0][3]), (255, 0, 254), 2)#right eye
        cv2.rectangle(frame, (eyes1[1][0], eyes1[1][1]), (eyes1[1][0]+eyes1[1][2], eyes1[1][1]+eyes1[1][3]), (255, 255, 0), 2)#left eye
        cv2.rectangle(frame, (eyes1[0][0]+ew/2-ew/10, eyes1[0][1]+eh/2-eh/10), (eyes1[0][0]+ew/2+ew/10, eyes1[0][1]+eh/2+eh/10), (255, 0, 254), 2)

        #eyes_num = 02
        right_eye_region = gray[eyes1[0][1]:eyes1[0][1]+eyes1[0][3], eyes1[0][0]:eyes1[0][0]+eyes1[0][2]]
        left_eye_region = gray[eyes1[1][1]:eyes1[1][1]+eyes1[1][3], eyes1[1][0]:eyes1[1][0]+eyes1[1][2]]
        right_byr = right_eye_region#byr[eyes1[0][1]:eyes1[0][1]+eyes1[0][3], eyes1[0][0]:eyes1[0][0]+eyes1[0][2]]#TEST
        if first == 0:
            #threshold = 10#right_byr[eh/2-eh/10:eh/2+eh/10, ew/2-ew/10:ew/2+ew/10].mean()
            result = np.array([0])
            if (r_count < 10):
                threshold = 10
                while result.sum() < int(150 * ew/4 * eh/4):
                    threshold += 1
                    ret, result = cv2.threshold(right_byr, threshold, 150, cv2.THRESH_BINARY_INV)
                    #threshold += 5
            #right_byr = cv2.adaptiveThreshold(right_byr, 150, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 0)
            ret, result = cv2.threshold(right_byr, threshold, 150, cv2.THRESH_BINARY_INV)
            #ret, result = cv2.threshold(right_byr, 0, 150, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
            result = cv2.medianBlur(result, 5)
            #r_count += 1
        #for j in range(len(right_byr)):
        #    for i in range(len(right_byr[0])):
        #        if right_byr[j][i] > 120:
        #            right_byr[j][i] = 0
        #        else:
        #            right_byr[j][i] = 150
        #for j in range(len(right_byr)):
        #    for i in range(len(right_byr[0])):
        #        if right_byr[j][i][0] > right_byr[j][i][2]:
        #            right_eye_region[j][i] = 255
        #        else:
        #            right_eye_region[j][i] = 0
            cv2.imshow('RER', result)
            count = 0
            for i in range(len(result)):
                for j in range(len(result[0])):
                    if result[i][j] > 0:
                        count += 1
            print count

        #if first == 0:
        #    right_corr = normcorrcoef(right_eye_region, right_template)
        #    left_corr = normcorrcoef(left_eye_region, left_template)
        #    string = ""
        #    if abs(right_corr) < threshold:
        #        r_opened = 0
        #        r_count += 1
        #        string += "r: right blink "
        #    else:
        #        r_opened = 1
        #        r_count = 0
        #        string += "r: "
        #    if abs(left_corr) < threshold:
        #        l_opened = 0
        #        l_count += 1
        #        string += "l: left blink "
        #    else:
        #        l_opened = 1
        #        l_count = 0
        #        string += "l: "
            #print string

        #if r_opened == 1 and abs(right_corr) > 0.88 or r_count > 10:
        #if r_opened == 1 or r_count > 10:
        #    r_count = 0
        #    right_template = right_eye_region.copy()
        #if l_opened == 1 and abs(left_corr) > 0.88 or l_count > 10:
        #if l_opened == 1 or l_count > 10:
        #    l_count = 0
        #    left_template = left_eye_region.copy()

        if first == 1:
            first = 0
            #threshold = right_byr[eh/2-eh/10:eh/2+eh/10, ew/2-ew/10:ew/2+ew/10].mean() + 10
            print 'Now you can close and open your eyes'

        #Bluring
        #right_eye_region = cv2.GaussianBlur(right_eye_region, (3,3), 0)#cv2.getGaussianKernel()
        #left_eye_region = cv2.GaussianBlur(left_eye_region, (3,3), 0)#cv2.getGaussianKernel()
        #ret, right_eye_region = cv2.threshold(right_eye_region, 0, 255, type = cv2.THRESH_TOZERO_INV | cv2.THRESH_OTSU)
        #right_eye_region = cv2.GaussianBlur(right_eye_region, (3,3), 0)#cv2.getGaussianKernel()
        #Sobel operator
        #gradx_rer = cv2.convertScaleAbs(cv2.Sobel(right_eye_region, -1, 1, 0, ksize = 3))
        #grady_rer = cv2.convertScaleAbs(cv2.Sobel(right_eye_region, -1, 0, 1, ksize = 3))
        #gradx_ler = cv2.convertScaleAbs(cv2.Sobel(left_eye_region, -1, 1, 0, ksize = 3))
        #grady_ler = cv2.convertScaleAbs(cv2.Sobel(left_eye_region, -1, 0, 1, ksize = 3))
        #right_eye_region = cv2.addWeighted(gradx_rer, 0.5, grady_rer, 0.5, 0)
        #left_eye_region = cv2.addWeighted(gradx_ler, 0.5, grady_ler, 0.5, 0)
        #thresh = right_eye_region.mean() + 0.3 * right_eye_region.std()
        #ret, right_eye_region = cv2.threshold(right_eye_region, 0, 255, type = cv2.THRESH_TOZERO | cv2.THRESH_OTSU)
        #thresh = left_eye_region.mean() + 0.3 * left_eye_region.std()
        #ret, left_eye_region = cv2.threshold(left_eye_region, thresh, 255, type = 3)

        #data = [0 for i in range(len(right_eye_region[0]))]
        #for i in range(len(right_eye_region[0])):
        #    for j in range(len(right_eye_region)):
        #        data[i] += right_eye_region[j][i]
        #print max(data)
        #bins = [i for i in range(len(data))]
        #plt.clf()
        #plt.axis([0,240,0,4000])
        #plt.plot(bins, data)
        #plt.draw()
        #time.sleep(0.001)

        #cv2.imshow('right', right_eye_region)
        #cv2.imshow('left', left_eye_region)

        if faces_num == 1:
            break

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
