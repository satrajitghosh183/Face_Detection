import cv2
import mediapipe as mp 
import time 

class FaceDetectorOpenCV2():
	def __init__(self, minDetectionCon = 0.65):
		self.minDetectionCon = minDetectionCon

		self.mpFaceDetection = mp.solutions.face_detection
		self.mpDraw = mp.solutions.drawing_utils
		self.faceDetection = self.mpFaceDetection.FaceDetection()

	def findFaces(self, img, draw=True):

		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.results = self.faceDetection.process(imgRGB)
		# print(self.results)
		bboxs = [] 
		if self.results.detections:
			for id, detection in enumerate(self.results.detections):
				bboxC = detection.location_data.relative_bounding_box
				ih, iw, ic = img.shape
				bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
				bboxs.append([id, bbox, detection.score])

				cv2.rectangle(img, bbox, (255, 0, 255), 3)
				cv2.putText(img, f'{int(detection.score[0]*100)}%', (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

		return img, bboxs


def main():
	
	cap = cv2.VideoCapture(0)
	pTime = 0
	print("Press q to stop the algorithm")
	my_face_detector = FaceDetectorOpenCV2(0.45)
	while True:

		success, img = cap.read()
		img, bounding_boxes = my_face_detector.findFaces(img)
		cTime = time.time()
		fps = 1 / (cTime - pTime)
		pTime = cTime 
		cv2.putText(img, f'FPS : {int(fps)}', (20, 75), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)

		cv2.imshow("Image", img)
		if cv2.waitKey(10) & 0xFF == ord('q'):
			print("Successfully breaking the loop")
			break


if __name__ == '__main__':
	main()
