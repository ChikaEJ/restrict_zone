import json
import os
from typing import List, Tuple

import cv2
import numpy as np


def draw_zones(frame, zones):
    for z in zones:
        pts = np.array(z["points"], dtype=np.int32)
        cv2.polylines(frame, [pts], isClosed=True, color=(0,0,255), thickness=2)
        x, y = pts[0]
        cv2.putText(frame, z.get("name", z["id"]), (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

def load_zones(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("zones", [])
    except FileNotFoundError:
        return []

def point_in_poly(pt: Tuple[int,int], poly_points: List[Tuple[int,int]]):
    contour = np.array(poly_points, dtype=np.int32)
    return cv2.pointPolygonTest(contour, pt, False) >= 0

def save_zones(path: str, zones):
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"zones": zones}, f, ensure_ascii=False, indent=2)

def create_video_writer(capture, output_path: str, filename: str = "output.avi", fps: float = 25.0):

    os.makedirs(output_path, exist_ok=True)
    out_file = os.path.join(output_path, filename)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer = cv2.VideoWriter(out_file, fourcc, fps, (width, height))
    return writer, out_file