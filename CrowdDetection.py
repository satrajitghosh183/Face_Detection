import cv2
import mediapipe as mp
import time
import csv
def bbox_overlap(bbox1, bbox2):
    """
    Check if two bounding boxes overlap
    """
    x1, y1, w1, h1 = bbox1
    x2, y2, w2, h2 = bbox2
    if (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2):
        return True
    else:
        return False
cap = cv2.VideoCapture(0)
pTime = 0
visitor_count = 0
prev_detections = []

mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection()

with open('visitor_count.csv', mode='w') as csv_file:
    fieldnames = ['timestamp', 'visitor_count']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

while True:
    success, img = cap.read()

    results = faceDetection.process(img)

    curr_detections = []
    if results.detections:
        for id, detection in enumerate(results.detections):
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            cv2.rectangle(img, bbox, (255, 0, 255), 3)
            cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 255), 3)
            curr_detections.append(bbox)

        # Check if any new detections overlap with previous detections
        for bbox in curr_detections:
            overlap = False
            for prev_bbox in prev_detections:
                if bbox_overlap(bbox, prev_bbox):
                    overlap = True
                    break
            if not overlap:
                visitor_count += 1
                prev_detections.append(bbox)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS : {int(fps)}', (20, 75), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    cv2.putText(img, f'Visitors : {visitor_count}', (20, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    cv2.imshow("Image", img)

    # Write visitor count to CSV file
    with open('visitor_count.csv', mode='a') as csv_file:
        fieldnames = ['timestamp', 'visitor_count']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow({'timestamp': time.time(), 'visitor_count': visitor_count})

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



