import cv2
import mediapipe as mp
import time
import csv
from flask import Flask, Response, render_template_string
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Initialize MediaPipe face detection
mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection(min_detection_confidence=0.5)

# List to keep track of unique faces
unique_faces = []

@app.route('/')
def index():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Face Detection App</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; }
            #video-feed { max-width: 100%; height: auto; }
        </style>
    </head>
    <body>
        <h1>Face Detection App</h1>
        <img id="video-feed" src="{{ url_for('video_feed') }}" alt="Video Feed">
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/Face')
def face_info():
    return json.dumps({'url': '/video_feed'})

@app.route('/video_feed')
def video_feed():
    return Response(process_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

def process_video():
    # Try to open the external webcam first, then fall back to the built-in webcam
    for camera_index in [1, 0]:  # Try 1 (external) then 0 (built-in)
        cap = cv2.VideoCapture(camera_index)
        if cap.isOpened():
            print(f"Successfully opened camera index {camera_index}")
            break
    else:
        print("Error: Could not open any video device. Exiting.")
        return

    pTime = 0
    print("Video feed function is running")

    # Create a CSV file to store detection data
    csv_path = 'detections.csv'
    csv_file_exists = os.path.isfile(csv_path)
    
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not csv_file_exists:
            writer.writerow(['id', 'score', 'bounding_box'])

    while True:
        success, img = cap.read()

        if not success:
            print("Failed to capture image. Retrying...")
            continue

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = faceDetection.process(imgRGB)

        if results.detections:
            for id, detection in enumerate(results.detections):
                mpDraw.draw_detection(img, detection)
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = img.shape
                bbox = (int(bboxC.xmin * iw), int(bboxC.ymin * ih), 
                        int(bboxC.width * iw), int(bboxC.height * ih))
                cv2.rectangle(img, bbox, (255, 0, 255), 2)
                cv2.putText(img, f'{int(detection.score[0] * 100)}%', 
                            (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

                # Check for unique face based on bounding box proximity
                found_match = False
                for i, face_data in enumerate(unique_faces):
                    distance = abs(bbox[0] - face_data[0][0]) + abs(bbox[1] - face_data[0][1]) + \
                               abs(bbox[2] - face_data[0][2]) + abs(bbox[3] - face_data[0][3])
                    if distance < 100:
                        unique_faces[i][0] = bbox  # Update bounding box
                        unique_faces[i][1] += 1    # Increment visit count
                        found_match = True
                        visitor_text = f"Welcome back, visitor {i + 1}! Visit count: {unique_faces[i][1]}"
                        print(visitor_text)
                        cv2.putText(img, visitor_text, (bbox[0], bbox[1] - 50), 
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 1)
                        break

                if not found_match:
                    # New face detected
                    unique_faces.append([bbox, 1])
                    new_visitor_text = f"Welcome, new visitor {len(unique_faces)}!"
                    print(new_visitor_text)
                    cv2.putText(img, new_visitor_text, (bbox[0], bbox[1] - 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Write detection data to CSV
                with open(csv_path, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([id, detection.score[0], bboxC])

        # Calculate and display FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)