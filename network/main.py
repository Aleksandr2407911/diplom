import cv2
import numpy as np
from yoolaNetTest import findNetwork



cap = cv2.VideoCapture('20230609_150644.mp4')

# fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
# out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640,480))


def correctCoordinate(x, y, width, height, **kwargs):
    return (int(x), int(y)), (int(x + width), int(y + height)), (int(x), int(y + height + 10))


def drow(img, coordinate):
    for oneCoordinate in coordinate:
        pivotH, pivotL, textCoordinate = correctCoordinate(**oneCoordinate)

        print(textCoordinate)
        try:
            cv2.rectangle(img, pivotH, pivotL, typeFigure[oneCoordinate.get('class')].get("color") or [255, 255, 255], thickness=5, lineType=cv2.LINE_8)
            cv2.putText(img, typeFigure[oneCoordinate.get('class')].get("title"), textCoordinate, cv2.FONT_HERSHEY_PLAIN, 2.3, (0, 255, 0), 2, cv2.LINE_8)
        except Exception as e:
            print(e)
            img = img
    return img
    
while True:
    ret, img = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    img = findNetwork(img)

    # frame = cv2.flip(img, 0)
    cv2.imshow('Camera', cv2.resize(img, (480, 600)))

    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
# out.release()

cv2.destroyAllWindows()



