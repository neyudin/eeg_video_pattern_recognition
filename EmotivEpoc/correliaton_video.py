#workon cv
import cv2
import numpy as np
import scipy as sp
import time

def normcorrcoef(img1, img2):
    leny = min(len(img1), len(img2))
    lenx = min(len(img1[0]), len(img2[0]))
    a = img1[(len(img1)-leny)/2:(len(img1)+leny)/2, (len(img1[0])-lenx)/2:(len(img1[0])+lenx)/2]
    b = img2[(len(img2)-leny)/2:(len(img2)+leny)/2, (len(img2[0])-lenx)/2:(len(img2[0])+lenx)/2]
    product = np.mean((a - a.mean()) * (b - b.mean()))
    stds = a.std() * b.std()
    if stds == 0:
        return 0
    else:
        product /= stds
        return product

#faceCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_frontalface_alt.xml')
#faceCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_frontalface_alt2.xml')
#faceCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_frontalface_alt_tree.xml')

video_capture = cv2.VideoCapture(0)
fps = video_capture.get(cv2.CAP_PROP_FPS)
print "Apriori frames per second: {0}".format(fps)

first = 1
r_opened = 1
l_opened = 1
r_count = 0
l_count = 0
r_blink_count = 0
l_blink_count = 0
negative_count = 0

right_template = np.array([0])
left_template = np.array([0])
right_corr = 1.0
left_corr = 1.0
threshold = 0.70

print 'Please, do not close your eyes'
frames_num = 450
frame_count = 0
start = time.time()
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    frame_count += 1

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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
        eh = int(0.16 * h)
        eyes1 = [[x+int(0.18*w), ey, ew, eh], [x+int(0.58*w), ey, ew, eh]]
        cv2.rectangle(frame, (eyes1[0][0], eyes1[0][1]), (eyes1[0][0]+eyes1[0][2], eyes1[0][1]+eyes1[0][3]), (255, 0, 254), 2)#right eye
        cv2.rectangle(frame, (eyes1[1][0], eyes1[1][1]), (eyes1[1][0]+eyes1[1][2], eyes1[1][1]+eyes1[1][3]), (255, 255, 0), 2)#left eye

        #eyes_num = 02
        right_eye_region = gray[eyes1[0][1]:eyes1[0][1]+eyes1[0][3], eyes1[0][0]:eyes1[0][0]+eyes1[0][2]]
        left_eye_region = gray[eyes1[1][1]:eyes1[1][1]+eyes1[1][3], eyes1[1][0]:eyes1[1][0]+eyes1[1][2]]

        if first == 0:
            right_corr = normcorrcoef(right_eye_region, right_template)
            left_corr = normcorrcoef(left_eye_region, left_template)
            #print right_corr, left_corr
            string = ""
            if abs(right_corr) < threshold:
                r_opened = 0
                r_count += 1
                string += "r: right blink "
                r_blink_count += 1
            else:
                r_opened = 1
                r_count = 0
                string += "r: "
                negative_count += 1
            if abs(left_corr) < threshold:
                l_opened = 0
                l_count += 1
                string += "l: left blink "
                l_blink_count += 1
            else:
                l_opened = 1
                l_count = 0
                string += "l: "
                negative_count += 1
            print string

        if r_opened == 1 and abs(right_corr) > 0.90 or r_count > 5:
            r_count = 0
            right_template = right_eye_region.copy()
        if l_opened == 1 and abs(left_corr) > 0.90 or l_count > 5:
            l_count = 0
            left_template = left_eye_region.copy()

        if first == 1:
            first = 0
            print 'Now you can close and open your eyes'

        if faces_num == 1:
            break

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q')  or  frame_count == frames_num:
        break

end = time.time()

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
print "Estimated frames per second : {0}".format(frames_num / (end - start))
print "Right eye blink count: {0} = FP + TP".format(r_blink_count)
print "Left eye blink count: {0} = FP + TP".format(l_blink_count)
print "Negative count: {0} = FN + TN".format(negative_count)