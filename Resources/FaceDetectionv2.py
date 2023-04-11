import cv2
import mediapipe as mp
import time
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["face_detection_db"]
face_collection = db["face_data"]

# Define schema for face data
face_data_schema = {
    "face_id": "",
    "timestamp": "",
    "score": "",
    "bbox": {"x": "", "y": "", "w": "", "h": ""},
    "landmarks": [{"x": "", "y": ""} for i in range(6)],
    "image_path": "",
    "visit_count": 0
}

# Initialize face detection module
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
face_detection = mp_face_detection.FaceDetection()

# Initialize video capture
cap = cv2.VideoCapture(0)
p_time = 0

while True:
    # Read a frame from video capture
    success, img = cap.read()

    # Process the frame with face detection module
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_detection.process(img_rgb)

    if results.detections:
        for id, detection in enumerate(results.detections):
            bbox = detection.location_data.relative_bounding_box
            score = detection.score[0]

            # Store face data in dictionary
            face_data = face_data_schema.copy()
            face_data["face_id"] = id
            face_data["timestamp"] = time.time()
            face_data["score"] = score
            face_data["bbox"]["x"] = bbox.xmin
            face_data["bbox"]["y"] = bbox.ymin
            face_data["bbox"]["w"] = bbox.width
            face_data["bbox"]["h"] = bbox.height
            face_data["landmarks"] = [{"x": lm.x, "y": lm.y} for lm in detection.location_data.relative_keypoints]
            face_data["image_path"] = f"face_{id}_{int(time.time())}.jpg"

            # Draw bounding box and text on the image
            ih, iw, ic = img.shape
            x, y, w, h = int(bbox.xmin * iw), int(bbox.ymin * ih), int(bbox.width * iw), int(bbox.height * ih)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 3)
            cv2.putText(img, f'{int(score*100)}%', (x, y - 20), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

            # Save the image
            cv2.imwrite(face_data["image_path"], img)

            # Check if the face has visited before
            found_face = face_collection.find_one({"face_id": id})
            if found_face:
                # If the face has visited before, check if it's a match
                prev_score = found_face["score"]
                prev_landmarks = found_face["landmarks"]
                is_match = True
                for i in range(6):
                    x_diff = abs(face_data["landmarks"][i]["x"] - prev_landmarks[i]["x"])
                    y_diff = abs(face_data["landmarks"][i]["y"] - prev_landmarks[i]["y"])
                    if x_diff > 0.1 or y_diff > 0.1:
                        is_match = False
                        break

                if is_match:
                    # If it's a match, increment the visit count and update the record
                    face_collection.update_one({"face_id": id}, {"$inc": {"visit_count": 1}})
                    print("Welcome back! This is your {} visit.".format(found_face["visit_count"] + 1))
                else:
                    # If it's not a match, insert the new record
                    face_data["visit_count"] = 1
                    face_collection.insert_one(face_data)
                    print("New face detected and added to the database.")
            # Display the image with bounding boxes and text
                cv2.imshow("Image", img)

                # Calculate and display the frame rate
                c_time = time.time()
                fps = 1 / (c_time - p_time)
                p_time = c_time
                cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

                # Press 'q' to quit the program
                if cv2.waitKey(1) & 0xFF == ord('q'):
                 break
                cap.release()
                cv2.destroyAllWindows()