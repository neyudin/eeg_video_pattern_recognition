import cv2
import numpy as np
import scipy as sp
import time

#faceCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_frontalface_alt.xml')
#faceCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_frontalface_alt2.xml')
#faceCascade = cv2.CascadeClassifier('/home/nikita/opencv/data/haarcascades/haarcascade_frontalface_alt_tree.xml')

r_threshold = 10
l_threshold = 10
test_frames_num = 30
right_upper_bound = 0.3
right_lower_bound = 0.15
left_upper_bound = 0.3
left_lower_bound = 0.15
right_sum = np.array([])
left_sum = np.array([])

video_capture = cv2.VideoCapture(0)
fps = video_capture.get(cv2.CAP_PROP_FPS)
print "Apriori frames per second: {0}".format(fps)

frames_num = 9000
frame_count = 0

for i in range(test_frames_num):
    ret, frame = video_capture.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print 'Training...'

for i in range(test_frames_num):
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=8,
        minSize=(200, 200),
        maxSize=(1000,1000),
        flags=cv2.CASCADE_SCALE_IMAGE)

    faces_num = 0
    for (x, y, w, h) in faces:
        faces_num += 1
        ey = y + int(0.32 * h)
        ew = int(0.24 * w)
        eh = int(0.12 * h)
        eyes1 = [[x+int(0.18*w), ey, ew, eh], [x+int(0.58*w), ey, ew, eh]]

        right_eye_region = gray[eyes1[0][1]:eyes1[0][1]+eyes1[0][3], eyes1[0][0]:eyes1[0][0]+eyes1[0][2]]
        threshold = 10
        result = np.array([0])
        while result.sum() < int(150 * ew/4 * eh/4):
            threshold += 1
            ret, result = cv2.threshold(right_eye_region, threshold, 150, cv2.THRESH_BINARY_INV)
        r_threshold = threshold
        ret, right_eye_region = cv2.threshold(right_eye_region, r_threshold, 150, cv2.THRESH_BINARY_INV)
        right_eye_region = cv2.medianBlur(right_eye_region, 5)

        left_eye_region = gray[eyes1[1][1]:eyes1[1][1]+eyes1[1][3], eyes1[1][0]:eyes1[1][0]+eyes1[1][2]]
        threshold = 10
        result = np.array([0])
        while result.sum() < int(150 * ew/4 * eh/4):
            threshold += 1
            ret, result = cv2.threshold(left_eye_region, threshold, 150, cv2.THRESH_BINARY_INV)
        l_threshold = threshold
        ret, left_eye_region = cv2.threshold(left_eye_region, l_threshold, 150, cv2.THRESH_BINARY_INV)
        left_eye_region = cv2.medianBlur(left_eye_region, 5)

        len_i = len(right_eye_region[0])
        data = np.array([0 for i in range(len_i)])
        len_j = len(right_eye_region)
        for i in range(len_i):
            for j in range(len_j):
                if right_eye_region[j][i] > 0:
                    data[i] += 1
        count = 0
        data_mean = data.mean()
        len_data = len(data)
        for i in range(len_data):
            if data[i] > data_mean:
                count += 1

        right_sum = np.append(right_sum, (count * 1.0)/len_data)

        len_i = len(left_eye_region[0])
        data = np.array([0 for i in range(len_i)])
        len_j = len(left_eye_region)
        for i in range(len_i):
            for j in range(len_j):
                if left_eye_region[j][i] > 0:
                    data[i] += 1
        count = 0
        data_mean = data.mean()
        len_data = len(data)
        for i in range(len_data):
            if data[i] > data_mean:
                count += 1

        left_sum = np.append(left_sum, (count * 1.0)/len_data)

        if faces_num == 1:
            break

right_lower_bound = right_sum.mean() - 3 * right_sum.std()
right_upper_bound = right_sum.mean() + 3 * right_sum.std()
left_lower_bound = left_sum.mean() - 3 * left_sum.std()
left_upper_bound = left_sum.mean() + 3 * left_sum.std()

print right_lower_bound
print right_upper_bound
print left_lower_bound
print left_upper_bound

print 'Complete...'

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

    # Draw a rectangle around the eyes
    faces_num = 0
    for (x, y, w, h) in faces:
        faces_num += 1
        ey = y + int(0.32 * h)
        ew = int(0.24 * w)
        eh = int(0.12 * h)
        eyes1 = [[x+int(0.18*w), ey, ew, eh], [x+int(0.58*w), ey, ew, eh]]
        #cv2.rectangle(frame, (eyes1[0][0], eyes1[0][1]), (eyes1[0][0]+eyes1[0][2], eyes1[0][1]+eyes1[0][3]), (255, 0, 254), 2)#right eye
        #cv2.rectangle(frame, (eyes1[1][0], eyes1[1][1]), (eyes1[1][0]+eyes1[1][2], eyes1[1][1]+eyes1[1][3]), (255, 255, 0), 2)#left eye

        #eyes_num = 02
        right_eye_region = gray[eyes1[0][1]:eyes1[0][1]+eyes1[0][3], eyes1[0][0]:eyes1[0][0]+eyes1[0][2]]
        ret, right_eye_region = cv2.threshold(right_eye_region, r_threshold, 150, cv2.THRESH_BINARY_INV)
        right_eye_region = cv2.medianBlur(right_eye_region, 5)

        left_eye_region = gray[eyes1[1][1]:eyes1[1][1]+eyes1[1][3], eyes1[1][0]:eyes1[1][0]+eyes1[1][2]]
        ret, left_eye_region = cv2.threshold(left_eye_region, l_threshold, 150, cv2.THRESH_BINARY_INV)
        left_eye_region = cv2.medianBlur(left_eye_region, 5)

        cv2.imshow('RER', right_eye_region)
        cv2.imshow('LER', left_eye_region)

        string = ""

        len_i = len(right_eye_region[0])
        data = np.array([0 for i in range(len_i)])
        len_j = len(right_eye_region)
        for i in range(len_i):
            for j in range(len_j):
                if right_eye_region[j][i] > 0:
                    data[i] += 1
        count = 0
        data_mean = data.mean()
        len_data = len(data)
        for i in range(len_data):
            if data[i] > data_mean:
                count += 1
        #print (count * 1.0)/len_data
        if ((count * 1.0)/len_data > right_upper_bound) or ((count * 1.0)/len_data < right_lower_bound):
            string += "r: blink "
        else:
            string += "r: "

        len_i = len(left_eye_region[0])
        data = np.array([0 for i in range(len_i)])
        len_j = len(left_eye_region)
        for i in range(len_i):
            for j in range(len_j):
                if left_eye_region[j][i] > 0:
                    data[i] += 1
        count = 0
        data_mean = data.mean()
        len_data = len(data)
        for i in range(len_data):
            if data[i] > data_mean:
                count += 1
        #print (count * 1.0)/len_data
        if ((count * 1.0)/len_data > left_upper_bound) or ((count * 1.0)/len_data < left_lower_bound):
            string += "l: blink "
        else:
            string += "l: "

        print string

        if faces_num == 1:
            break

    # Display the resulting frame
    #cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or frame_count == frames_num:
        break

end = time.time()

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

print "Estimated frames per second : {0}".format(frames_num / (end - start))
