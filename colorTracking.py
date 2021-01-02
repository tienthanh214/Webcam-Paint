# xoa anh mau xanh - trang

import cv2
import numpy as np
import time

webcam = cv2.VideoCapture(0)

def nothing(x):
    pass

cv2.namedWindow("Trackbars", 1)
cv2.createTrackbar("Lower H", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Lower S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Lower V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Upper H", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Upper S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Upper V", "Trackbars", 255, 255, nothing)

# time.sleep(3)
ret, background = webcam.read()

# fi = open("temp.txt", "w")
# for i in range(background.shape[0]):
#     for j in range(background.shape[1]):
#         for k in range(3):
#             fi.write(str(background[i][j][k]) + " ")
#         fi.write("\n")
# fi.close()

# fi = open("temp.txt")
# for i in range(background.shape[0]):
#     for j in range(background.shape[1]):
#         x = fi.readline()[:-1]
#         x = x.split(' ')[:-1]
#         # print(x)
#         for abc in range(3):
#             x[abc] = int(x[abc])
#         background[i][j] = x
# fi.close()

background = cv2.flip(background, 1)

while True:
    ret, frame = webcam.read()
    if not ret:
        print("Can't receive frame from camera!")
        break
    frame = cv2.flip(frame, 1)
    cv2.imshow('Origin image', frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # print(hsv)
    lowerH = cv2.getTrackbarPos("Lower H", "Trackbars")
    lowerS = cv2.getTrackbarPos("Lower S", "Trackbars")
    lowerV = cv2.getTrackbarPos("Lower V", "Trackbars")
    upperH = cv2.getTrackbarPos("Upper H", "Trackbars")
    upperS = cv2.getTrackbarPos("Upper S", "Trackbars")
    upperV = cv2.getTrackbarPos("Upper V", "Trackbars")

    lower_range = np.array([lowerH, lowerS, lowerV], dtype = "uint8")
    upper_range = np.array([upperH, upperS, upperV], dtype = "uint8")

    lower_range = np.array([0, 125,70])
    upper_range = np.array([10,255,255])
    mask1 = cv2.inRange(hsv, lower_range, upper_range)
    lower_range = np.array([170, 120, 70])
    upper_range = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_range, upper_range)
    mask = cv2.inRange(hsv, lower_range, upper_range)

    mask = mask1 + mask2

    mask1 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    mask2 = cv2.bitwise_not(mask1)

    res1 = cv2.bitwise_and(frame, frame, mask = mask2)
    res2 = cv2.bitwise_and(background, background, mask = mask1)
    res  = cv2.bitwise_and(frame, frame, mask = mask)
    final_res = cv2.addWeighted(res1, 1, res2, 1, 0)

    cv2.imshow('Mask', mask)
    # cv2.imshow('Res', res)
    # cv2.imshow('ahihi', res1)
    cv2.imshow('magic', final_res)
    if cv2.waitKey(1) == 27: # press ESC to exit
        break

webcam.release()
cv2.destroyAllWindows()

