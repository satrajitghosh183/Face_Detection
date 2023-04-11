import cv2
from tkinter import *
from PIL import Image, ImageTk
from face_detection import FaceDetector

class FaceDetectionGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Face Detection")
        self.frame = Frame(self.root)
        self.frame.pack()

        self.canvas = Canvas(self.frame, width=640, height=480)
        self.canvas.pack()

        self.face_detector = FaceDetector()

        self.video = cv2.VideoCapture(0)
        self.delay = 15
        self.update()

        self.root.mainloop()

    def update(self):
        ret, frame = self.video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.face_detector.process(frame)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.canvas.imgtk = imgtk
        self.canvas.create_image(0, 0, anchor=NW, image=imgtk)
        self.root.after(self.delay, self.update)

if __name__ == "__main__":
    gui = FaceDetectionGUI()
