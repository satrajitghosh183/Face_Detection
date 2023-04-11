import cv2
import mediapipe as mp 
import csv


class FaceDetector:
    def __init__(self):
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection()
        self.unique_faces = []

    def detect_faces(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.faceDetection.process(imgRGB)
        bboxes = []
        if results.detections:
            for id, detection in enumerate(results.detections):
                bboxC = detection.location_data.relative_bounding_box
                h, w, c = img.shape
                bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
                bboxes.append(bbox)
                self.mpDraw.draw_detection(img, detection)
                cv2.rectangle(img, bbox, (255, 0, 255), 2)
                cv2.putText(img, f'{int(detection.score[0]*100)}%', (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        return img, bboxes

    def track_unique_faces(self, bboxes):
        for bbox in bboxes:
            found_match = False
            for i, face_data in enumerate(self.unique_faces):
                # Calculate the distance between the current face and the previous face
                distance = abs(bbox[0] - face_data[0][0]) + abs(bbox[1] - face_data[0][1]) + \
                           abs(bbox[2] - face_data[0][2]) + abs(bbox[3] - face_data[0][3])
                if distance < 100:
                    # This face matches a previously detected face
                    self.unique_faces[i][0] = bbox
                    self.unique_faces[i][1] += 1
                    found_match = True
                    print(f"Welcome back, visitor {i + 1}! This is your {self.unique_faces[i][1]} visit.")
                    break
            if not found_match:
                # This is a new face
                self.unique_faces.append([bbox, 1])
                print(f"Welcome, new visitor {len(self.unique_faces)}!")

    def save_detections(self, path, img_name, bboxes):
        with open(path, mode='a') as file:
            writer = csv.writer(file)
            for i, bbox in enumerate(bboxes):
                writer.writerow([img_name, i+1, bbox])


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    detector = FaceDetector()
    img_counter = 0

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture camera input. Exiting...")
            break

        img, bboxes = detector.detect_faces(img)
        detector.track_unique_faces(bboxes)
        detector.save_detections('detections.csv', img_counter, bboxes)
        img_counter += 1

        cv2.imshow("Face Detection", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


                

    