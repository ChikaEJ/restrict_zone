import cv2

from app.detector import YoloDetector
from app.core.config import settings
from app.tracker import TrackerWrapper
from app.utils import draw_zones, load_zones


def main():
    detector = YoloDetector(model_path=settings.YOLO_MODEL, conf=0.4)
    capture = cv2.VideoCapture(settings.VIDEO_SOURCE)
    tracker = TrackerWrapper() if settings.USE_DEEPSORT else None
    zones = load_zones(settings.ZONES_FILE)


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

        tracks = []
        if settings.USE_DEEPSORT and tracker is not None:
            tracks = tracker.update(person_detections, frame=frame)
        else:
            tracks = []
            for i, d in enumerate(person_detections):
                class Tmp:
                    pass

                t = Tmp()
                t.track_id = i
                l, t_y, w, h = d[0]
                t.to_ltrb = lambda ltrb=(l, t_y, l + w, t_y + h): ltrb
                t.is_confirmed = lambda: True
                tracks.append(t)

        draw_zones(frame, zones)

if __name__ == '__main__':
    main()