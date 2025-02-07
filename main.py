import cv2  # Displays an image or video frame.
import numpy as np
import pyautogui # Moves the mouse to screen coordinates.
import HandTrackingModule as htm
import time

# Set screen width and height
wCam, hCam = 640, 480
frameR = 100  # Reduction frame size
smoothening = 5  # Smooth factor

prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.HandDetector(maxHands=1)

wScr, hScr = pyautogui.size()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Index Finger Tip
        x2, y2 = lmList[12][1:]  # Middle Finger Tip

        fingers = []
        if lmList[8][2] < lmList[6][2]:  # Index Finger Up
            fingers.append(1)
        else:
            fingers.append(0)

        if lmList[12][2] < lmList[10][2]:  # Middle Finger Up
            fingers.append(1)
        else:
            fingers.append(0)

        # Moving Mode (Only Index Finger Up)
        if fingers[0] == 1 and fingers[1] == 0:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            curr_x = prev_x + (x3 - prev_x) / smoothening
            curr_y = prev_y + (y3 - prev_y) / smoothening

            pyautogui.moveTo(wScr - curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

        # Clicking Mode (Both Index and Middle Fingers Up)
        if fingers[0] == 1 and fingers[1] == 1:
            length = np.linalg.norm(np.array([x1, y1]) - np.array([x2, y2]))
            if length < 40:
                pyautogui.click()
                time.sleep(0.2)

    cv2.imshow("Virtual Mouse", img)
    cv2.waitKey(1)
