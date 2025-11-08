import cv2

from app.alarm_manager import AlarmManager
from app.detector import YoloDetector
from app.core.config import settings
from app.tracker import TrackerWrapper
from app.utils import create_video_writer, draw_zones, load_zones, \
    point_in_poly


def main():
    detector = YoloDetector(model_path=settings.YOLO_MODEL, conf=settings.CONFIDENCE)
    capture = cv2.VideoCapture(settings.VIDEO_SOURCE)
    fps = capture.get(cv2.CAP_PROP_FPS) or 25.0
    tracker = TrackerWrapper()
    zones = load_zones(settings.ZONES_FILE)
    alarm = AlarmManager(settings.ALARM_COOLDOWN_SECONDS)

    writer, out_file = create_video_writer(capture, settings.OUTPUT_PATH, "output.avi", fps)

    while True:
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

        tracks = tracker.update(person_detections, frame=frame)

        draw_zones(frame, zones)

        any_alarm = False
        for track in tracks:
            if not track.is_confirmed():
                continue
            left, top, right, bottom = map(int, track.to_ltrb())
            center_x = int((left + right) / 2)
            center_y = int((top + bottom) / 2)

            in_any_zone = False
            for zone in zones:
                if point_in_poly((center_x, center_y), zone["points"]):
                    in_any_zone = True
                    break

            alarm.update_track(track.track_id, in_any_zone)

            color = (0, 0, 255) if alarm.is_alarm_on(track.track_id) else (
            0, 255, 0)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, f"ID {track.track_id}", (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            cv2.circle(frame, (center_x, center_y), 3, (255, 255, 255), -1)

            if alarm.is_alarm_on(track.track_id):
                any_alarm = True
                cv2.putText(frame, f"ALARM! ID {track.track_id}",
                            (50, 50 + 30 * int(track.track_id)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        if any_alarm:
            cv2.putText(frame, "!!! alarm !!!", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 4)

        cv2.imshow("Тестовое видео", frame)
        if writer:
            writer.write(frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

    capture.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()