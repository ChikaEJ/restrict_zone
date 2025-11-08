import cv2

from app.detector import YoloDetector
from app.core.config import settings


def main():
    detector = YoloDetector(model_path=settings.YOLO_MODEL, conf=0.4)
    capture = cv2.VideoCapture(settings.VIDEO_SOURCE)
    i = 0
    while True:
        i = i + 1
        ret, frame = capture.read()
        if not ret:
            break

        detections = detector.detect(frame)
        person_detections = []
        for detection in detections:
            if detection["name"] == "person":
                x1, y1, x2, y2 = detection["xyxy"]
                width = x2 - x1
                height = y2 - y1
                person_detections.append([[x1, y1, width, height], detection["conf"], "person"])
                print(person_detections)

if __name__ == '__main__':
    main()