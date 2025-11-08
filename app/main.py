import cv2

from app.detector import YoloDetector
from app.core.config import settings


def main():
    print('Start')
    detector = YoloDetector(model_path=settings.YOLO_MODEL, conf=0.4)
    print('Detected')
    capture = cv2.VideoCapture(settings.VIDEO_SOURCE)
    print('Start While Loop')
    i = 0
    while True:
        i = i + 1
        print(f"Loop{i}")
        ret, frame = capture.read()
        print(f"{ret=}")
        if not ret:
            break

        detections = detector.detect(frame)
        print(f"{detections=}")
        for detection in detections:
            if detection:
                print(detection['name'])

if __name__ == '__main__':
    main()