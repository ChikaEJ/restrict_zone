from app.core.config import settings
from app.utils import save_zones, load_zones

from typing import List, Tuple


class ZoneEditor:
    def __init__(self, frame, zones_file):
        self.frame = frame.copy()
        self.clone = frame.copy()
        self.zones_file = zones_file
        self.current_pts: List[Tuple[int, int]] = []
        self.saved_zones = load_zones(zones_file)

    def click_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.current_pts.append((x, y))
            cv2.circle(self.frame, (x, y), 3, (0, 255, 0), -1)
            if len(self.current_pts) > 1:
                cv2.line(self.frame, self.current_pts[-2],
                         self.current_pts[-1], (0, 255, 0), 2)

    def run(self):
        win = "Zone Editor - press s to save zone, c to commit zone, r to reset last, q to quit"
        print(f"\033[92m{win}\033[0m")
        cv2.namedWindow(win, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(win, self.click_event)
        while True:
            disp = self.frame.copy()
            if len(self.current_pts) > 1:
                pts = self.current_pts
                for i in range(len(pts) - 1):
                    cv2.line(disp, pts[i], pts[i + 1], (0, 255, 0), 2)
            cv2.imshow(win, disp)
            key = cv2.waitKey(20) & 0xFF
            if key == ord('r'):
                if self.current_pts:
                    self.current_pts.pop()
                    self.frame = self.clone.copy()
                    for p in self.current_pts:
                        cv2.circle(self.frame, p, 3, (0, 255, 0), -1)
                    for i in range(len(self.current_pts) - 1):
                        cv2.line(self.frame, self.current_pts[i],
                                 self.current_pts[i + 1], (0, 255, 0), 2)
            elif key == ord('c'):
                if len(self.current_pts) >= 3:
                    zid = f"zone_{len(self.saved_zones) + 1}"
                    self.saved_zones.append({"id": zid, "name": zid,
                                             "points": self.current_pts.copy()})
                    print(f"Committed zone {zid}")
                    self.current_pts = []
                    self.frame = self.clone.copy()
            elif key == ord('s'):
                save_zones(self.zones_file, self.saved_zones)
                print(
                    f"Saved {len(self.saved_zones)} zones to {self.zones_file}")
            elif key == ord('q') or key == 27:
                break
        cv2.destroyAllWindows()


if __name__ == "__main__":
    import sys
    import cv2

    video = settings.VIDEO_SOURCE
    capture = cv2.VideoCapture(video)
    ret, frame = capture.read()
    if not ret:
        print("Не удалось открыть видео")
        sys.exit(1)
    editor = ZoneEditor(frame, settings.ZONES_FILE)
    editor.run()
