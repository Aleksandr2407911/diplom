import cv2


def initTrack():
	return cv2.TrackerCSRT_create()


def drawTracking(img, tracker):
	ok, bbox = tracker.update(img)

	if ok:
		p1 = (int(bbox[0]), int(bbox[1]))
		p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
		cv2.rectangle(img, p1, p2, (255, 0, 0), 2, 1)
		return True
	else:
		cv2.putText(img, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
		return False