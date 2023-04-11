import cv2
import mediapipe as mp 
import time 
import csv
from flask import Flask, Response
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)
mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection()

# Initialize a list to keep track of the unique faces
unique_faces = []
@app.route('/')
def hello_world():
   return "Hello World"

  
@app.route('/Face')
def index():
     return json.dumps({'url': '/video_feed'})
@app.route('/video_feed')
def video_feed():
    return Response(process_video(), mimetype='multipart/x-mixed-replace; boundary=frame')   

def process_video():
    cap = cv2.VideoCapture(0)
    pTime = 0
    
    print("This function is alive ")

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

            # Check if this face detection has been seen before
            found_match = False
            for i, face_data in enumerate(unique_faces):
                # Calculate the distance between the current face and the previous face
                distance = abs(bbox[0] - face_data[0][0]) + abs(bbox[1] - face_data[0][1]) + \
                           abs(bbox[2] - face_data[0][2]) + abs(bbox[3] - face_data[0][3])
                if distance < 100:
                    # This face matches a previously detected face
                    unique_faces[i][0] = bbox
                    unique_faces[i][1] += 1
                    found_match = True
                    print(f"Welcome back, visitor {i + 1}! This is your {unique_faces[i][1]} visit.")
                    break
            
            if not found_match:
                # This is a new face
                unique_faces.append([bbox, 1])
                print(f"Welcome, new visitor {len(unique_faces)}!")
                
            with open('detections.csv', mode='a') as file:
                writer = csv.writer(file)
                writer.writerow([id, detection.score, bboxC])

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime 
            cv2.putText(img, f'FPS : {int(fps)}', (20, 75), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,00), 3)

            
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()


if __name__ == '__main__':
    app.run(debug=True)