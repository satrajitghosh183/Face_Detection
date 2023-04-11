import base64
import time

import cv2
import mediapipe as mp
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['face_db']
collection = db['faces']

cap = cv2.VideoCapture(0)
pTime = 0

mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection()


def store_to_db(data, img):
    img_str = cv2.imencode('.jpg', img)[1].tostring()
    encoded_image = base64.b64encode(img_str)
    data['image'] = encoded_image.decode('utf-8')
    result = collection.insert_one(data)
    print(f"Inserted with ID: {result.inserted_id}")


def search_in_db(results):
    for detection in results.detections:
        if detection.score[0] > 0.8:
            stored_data = collection.find_one({'keypoints': detection.location_data.relative_keypoints})
            if stored_data is not None:
                print('Second visit!')
            else:
                data = {
                    'keypoints': detection.location_data.relative_keypoints,
                }
                store_to_db(data, img)


while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)

    if results.detections:
        for id, detection in enumerate(results.detections):
            mpDraw.draw_detection(img, detection)
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            cv2.rectangle(img, bbox, (255, 0, 255), 3)
            cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 255), 3)
            search_in_db(results)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS : {int(fps)}', (20, 75), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cv2.imshow("Image", img)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
