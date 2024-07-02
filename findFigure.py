import cv2
import numpy as np
from matplotlib import pyplot as plt

typeFigure = {'3':  "Triangle",
              '4': "Quadrilateral",
              '5':  "Circle",
              '6': 'Circle',
              '12': "Crosshair",
              '0': 'Circle'}


def filterConter(box: np.array) -> bool:
    return cv2.contourArea(box) > 10000.0

def showTittle(img, approx, x, y, contour):


    if typeFigure.get(str(len(approx))):
        tittle = typeFigure.get(str(len(approx)))

        cv2.putText(img, tittle, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 5)
        cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)
    elif len(approx) == 0:
        tittle = typeFigure.get('0')
        cv2.putText(img, tittle, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 5)
        cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)


def findConters(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)[1]
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # edges = cv2.Canny(gray, 200, 200)
    # ret3, th3 = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return contours


cap = cv2.VideoCapture('20230609_150644.mp4')
if not cap.isOpened():
    print("Cannot open camera")
    exit()


while True:
    ret, img = cap.read()
    contours = findConters(img)

    iter = 0
    for contour in contours:

        if iter == 0:
            iter = 1
            continue

        # hull = cv2.convexHull(contour)

        if filterConter(contour):
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)

            M = cv2.moments(contour)
            x = approx.ravel()[0]
            y = approx.ravel()[1]

            showTittle(img, approx, x, y, contour)

    if cv2.waitKey(1) == ord('q'):
        break
    cv2.imshow('Camera', cv2.resize(img, (480, 600)))

