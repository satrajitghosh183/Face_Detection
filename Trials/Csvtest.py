import cv2
import mediapipe as mp 
import time 
import csv

cap = cv2.VideoCapture(0)
pTime = 0
print("This function is alive ")

mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection()

# Initialize variables to store the previous detection score and bounding box
prev_score = None
prev_bbox = None

with open('detections.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'score', 'bounding_box'])

while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)

    if results.detections:
        for id, detection in enumerate(results.detections):
            mpDraw.draw_detection(img, detection)
            bboxC = detection.location_data.relative_bounding_box
            bbox = int(bboxC.xmin * img.shape[1]), int(bboxC.ymin * img.shape[0]), int(bboxC.width * img.shape[1]), int(bboxC.height * img.shape[0])
            cv2.rectangle(img, bbox, (255, 0, 255), 3)
            cv2.putText(img, f'{int(detection.score[0]*100)}%', (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

            # Check if the new score is similar to the previous score
            if prev_score is not None and abs(detection.score[0] - prev_score) / prev_score >= 0.1:
                print(f"Detected face {id+1} is {int((1 - abs(detection.score[0] - prev_score))*100)}% similar to the previous detection.")

            with open('detections.csv', mode='a') as file:
                writer = csv.writer(file)
                writer.writerow([id, detection.score, bboxC])

            # Update the previous score and bounding box
            prev_score = detection.score[0]
            prev_bbox = bboxC

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime 
    cv2.putText(img, f'FPS : {int(fps)}', (20, 75), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)

    cv2.imshow("Image", img)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
