from flask import Flask, render_template, Response
import cv2
from detector import CrowdDetector

app = Flask(__name__)
detector = CrowdDetector()

def gen_frames():
    cap = cv2.VideoCapture(1)  # Use external camera
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            faces, frame = detector.detect_faces(frame)
            detector.update_crowd_count(faces)
            detector.update_csv()

            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield frame in byte format for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
