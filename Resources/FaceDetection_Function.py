import base64
import time
import cv2
import mediapipe as mp
import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['face_db']
collection = db['faces']

mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection()


def detect_faces(img):
    print("The function is alive")
    results = faceDetection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    detected_faces = []
    if results.detections:
        for detection in results.detections:
            if detection.score[0] > 0.8:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                detected_faces.append({
                    'bbox': bbox,
                    'keypoints': detection.location_data.relative_keypoints,
                    'score': detection.score[0]
                })
                mpDraw.draw_detection(img, detection)
                cv2.rectangle(img, bbox, (255, 0, 255), 3)
                cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                            3, (255, 0, 255), 3)
    return detected_faces, img
 

def repeat_face_detection():
    cap = cv2.VideoCapture(0)
    pTime = 0
    while True:
        success, img = cap.read()
        detected_faces, img = detect_faces(img)
        if detected_faces:
            for face in detected_faces:
                stored_data = collection.find_one({'keypoints': face['keypoints']})
                if stored_data is not None:
                    print('Second visit!')
                else:
                    data = {
                        'keypoints': face['keypoints'],
                    }
                    store_to_db(data, img)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS : {int(fps)}', (20, 75), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.imshow("Image", img)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break


def store_to_db(data, img):
    img_str = cv2.imencode('.jpg', img)[1].tostring()
    encoded_image = base64.b64encode(img_str)
    data['image'] = encoded_image.decode('utf-8')
    result = collection.insert_one(data)
    print(f"Inserted with ID: {result.inserted_id}")

# To run the code,  just need to call the repeat_face_detection() function.
