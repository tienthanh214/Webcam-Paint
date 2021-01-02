import cv2
import numpy as np

webcam = cv2.VideoCapture(0)

def nothing(x):
    pass

# cv2.namedWindow("Trackbars", 1)
cv2.createTrackbar("Lower H", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Lower S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Lower V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("Upper H", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Upper S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Upper V", "Trackbars", 255, 255, nothing)

canvas = None
paintColor = [255, 179, 222]


while True:
    ret, frame = webcam.read()
    if not ret:
        print("Can't receive frame from camera!")
        break
    if canvas is None:
        canvas = np.zeros_like(frame)
        #canvas = 255 - canvas
    frame = cv2.flip(frame, 1)
    # cv2.imshow('Origin image', frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lowerH = cv2.getTrackbarPos("Lower H", "Trackbars")
    lowerS = cv2.getTrackbarPos("Lower S", "Trackbars")
    lowerV = cv2.getTrackbarPos("Lower V", "Trackbars")
    upperH = cv2.getTrackbarPos("Upper H", "Trackbars")
    upperS = cv2.getTrackbarPos("Upper S", "Trackbars")
    upperV = cv2.getTrackbarPos("Upper V", "Trackbars")

    lower_range = np.array([lowerH, lowerS, lowerV], dtype = "uint8")
    upper_range = np.array([upperH, upperS, upperV], dtype = "uint8")

    lower_range = np.array([160, 120, 80])
    upper_range = np.array([189, 255, 255])
    mask1 = cv2.inRange(hsv, lower_range, upper_range)
    lower_range = np.array([0, 100, 0])
    upper_range = np.array([10, 255, 255])
    mask2 = cv2.inRange(hsv, lower_range, upper_range)
    # mask = cv2.inRange(hsv, lower_range, upper_range)
    mask = mask1

    mask = cv2.morphologyEx(mask, cv2.MORPH_ERODE, np.ones((3, 3), np.uint8), iterations = 1)

    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((5, 5), np.uint8), iterations = 2)

    res = cv2.bitwise_and(frame, frame, mask = mask)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    pen = None
    if contours:
        pen = max(contours, key = cv2.contourArea)
        for pen in contours:
            if cv2.contourArea(pen) > 500:
                x, y, w, h = cv2.boundingRect(pen)
                canvas = cv2.circle(canvas, (x, y), 1, paintColor, 5)
                # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 25, 255), 2)
    # mask_canvas = cv2.inRange(canvas, np.array(paintColor), np.array(paintColor))
    # cv2.imshow('Canvas res', mask_canvas)
    # frame = cv2.bitwise_not(frame, frame, mask = mask_canvas)
    _ , mask = cv2.threshold(cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY), 20, 255, cv2.THRESH_BINARY)
    foreground = cv2.bitwise_and(canvas, canvas, mask = mask)
    background = cv2.bitwise_and(frame, frame, mask = cv2.bitwise_not(mask))
    cv2.imshow('foreground', foreground)
    cv2.imshow('backgroudn', background)
    cv2.imshow('mask', mask)
    frame = cv2.add(foreground,background)


    #frame = cv2.bitwise_or(frame, frame, mask = mask_canvas)
    #frame = cv2.bitwise_and(frame, frame, mask = mask_canvas)
    # cv2.imshow('Mask', res)
    stacked = np.hstack((canvas, frame))
    cv2.imshow('Webcam paint', cv2.resize(stacked, None, fx = 1, fy = 1))

    key_pressed = cv2.waitKey(1) & 0xFF
    if key_pressed == ord(' '):
        canvas = None
    if key_pressed == 27: # press ESC to exit
        break


webcam.release()
cv2.destroyAllWindows()

