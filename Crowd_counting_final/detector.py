import cv2
import mediapipe as mp
import time
import csv
from collections import deque

class CrowdDetector:
    def __init__(self):
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)

        self.prev_faces = deque(maxlen=30)
        self.crowd_count = 0
        self.start_time = time.time()

        self.csv_filename = 'crowd_count.csv'
        self.initialize_csv()

    def initialize_csv(self):
        with open(self.csv_filename, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['timestamp', 'crowd_count'])
            writer.writeheader()

    def update_csv(self):
        with open(self.csv_filename, mode='a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['timestamp', 'crowd_count'])
            writer.writerow({
                'timestamp': time.time() - self.start_time,
                'crowd_count': self.crowd_count
            })

    def detect_faces(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(image_rgb)

        faces = []
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = image.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                       int(bboxC.width * iw), int(bboxC.height * ih)
                faces.append(bbox)

                self.mp_drawing.draw_detection(image, detection)

        return faces, image

    def update_crowd_count(self, faces):
        if not self.prev_faces:
            self.crowd_count = len(faces)
        else:
            new_faces = 0
            for face in faces:
                if not any(self.bbox_overlap(face, prev_face)
                           for prev_frame in self.prev_faces
                           for prev_face in prev_frame):
                    new_faces += 1
            self.crowd_count += new_faces

        self.prev_faces.append(faces)

    @staticmethod
    def bbox_overlap(bbox1, bbox2):
        x1, y1, w1, h1 = bbox1
        x2, y2, w2, h2 = bbox2
        return (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2)
