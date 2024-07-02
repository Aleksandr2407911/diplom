import cv2
import numpy as np
from settingTracker import initTrack, drawTracking


trackPivot = []
lastPivot = []

findBox = False


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()


def filterConter(box: np.array) -> bool:
    return cv2.contourArea(box) > 100.0


def drawNewCoutours(img, contours, color):
    global trackPivot
    boxMax = max(contours, key=cv2.contourArea)

    rect = cv2.minAreaRect(boxMax)  # пытаемся вписать прямоугольник
    box = cv2.boxPoints(rect)  # поиск четырех вершин прямоугольника
    box = np.intp(box)

    trackPivot = np.array(box, copy=True)
    filterConter(box) and cv2.drawContours(img, [box], 0, color, 2)

    return img


"""  init  """
rgb = (255, 0, 0)
hsv_red = cv2.cvtColor(np.uint8([[rgb]]), cv2.COLOR_RGB2HSV)[0][0]

hue_range = 5
saturation_range = 50
value_range = 50

lower_color_pink = np.array([hsv_red[0] - hue_range, hsv_red[1] - saturation_range, hsv_red[2] - value_range])
upper_color_pink = np.array([hsv_red[0] + hue_range, hsv_red[1] + saturation_range, hsv_red[2] + value_range])
"""  init close """

tracker = initTrack()

while True:
    ret, img = cap.read()

    timer = cv2.getTickCount()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_pink = cv2.inRange(hsv, lower_color_pink, upper_color_pink)
    contours_red, hierarchy_red = cv2.findContours(mask_pink, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    img = drawNewCoutours(img, contours_red, (0, 0, 255)) if len(contours_red) != 0 and not findBox else img
    findBox = findBox and drawTracking(img, tracker)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    print(img)
    cv2.putText(img, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

    cv2.imshow('Camera', img)


    if cv2.waitKey(1) == ord('q'):
        break
    if cv2.waitKey(2) == ord('k') and len(trackPivot) > 0 :
        findBox = not findBox

        if findBox:
            tracker = initTrack() if not tracker else tracker

            initBB = [*trackPivot[0]]
            initBB.extend(trackPivot[2] - trackPivot[0])

            print(initBB)
            tracker.init(img, initBB)



cap.release()
cv2.destroyAllWindows()



