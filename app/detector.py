from ultralytics import YOLO

class YoloDetector:
    def __init__(self, model_path: str, conf: float = 0.45):
        self.model = YOLO(model_path)
        self.conf = conf
        self.names = self.model.names

    def detect(self, frame):
        results = self.model(frame, conf=self.conf, verbose=False)
        outputs = []

        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            name = self.names[cls]
            outputs.append({"xyxy": (x1, y1, x2, y2), "conf": conf, "class_id": cls, "name": name})
        return outputs
