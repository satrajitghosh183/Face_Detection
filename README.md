
# Project Title
Title: Facial Recognition using OpenCV, MediaPipe and Flask

Introduction:

Facial recognition has become increasingly popular in recent years, and there are many applications for this technology, including security, marketing, and social media. In this project, we will use OpenCV, MediaPipe, and Flask to build a facial recognition system that detects faces and stores them in a CSV file offline.

OpenCV is an open-source computer vision library that provides a wide range of image and video processing algorithms. MediaPipe is a framework for building pipelines to process multimedia data, including video and audio. Flask is a lightweight web framework for Python, which makes it easy to create web applications.

Our facial recognition system will use OpenCV to detect faces in real-time video streams. We will then use MediaPipe to extract facial landmarks, such as the position of the eyes, nose, and mouth. Finally, we will use Flask to store the facial landmarks in a CSV file offline. This will allow us to build a database of faces that can be used for future facial recognition applications.

In this project, we will focus on building a facial recognition system that is accurate, efficient, and easy to use


## What we used 
Sure! Here's a detailed explanation of the components used in the facial recognition system built using OpenCV, MediaPipe, and Flask:

OpenCV: OpenCV is an open-source computer vision library that provides a wide range of image and video processing algorithms. In this project, we will use OpenCV to capture real-time video streams and detect faces within those streams. OpenCV provides various algorithms for face detection, such as Haar Cascades, which can detect the presence of a face in an image by analyzing features such as edges, lines, and corners.

MediaPipe: MediaPipe is a framework for building pipelines to process multimedia data, including video and audio. In this project, we will use MediaPipe to extract facial landmarks from the detected faces. Facial landmarks are key points on the face, such as the corners of the eyes, nose, and mouth. These landmarks can be used to identify a person's unique facial features and build a database of faces.

Flask: Flask is a lightweight web framework for Python, which makes it easy to create web applications. In this project, we will use Flask to store the facial landmarks in a CSV file offline. Flask provides a simple and intuitive way to build web applications, allowing us to quickly and easily store and retrieve data from our database.

CSV File: A CSV (Comma Separated Values) file is a simple and widely used file format for storing tabular data. In this project, we will store the facial landmarks in a CSV file offline. This will allow us to build a database of faces that can be used for future facial recognition applications.

In summary, OpenCV is used to detect faces in real-time video streams, MediaPipe is used to extract facial landmarks from the detected faces, Flask is used to store the facial landmarks in a CSV file offline, and the CSV file is used to build a database of faces that can be used for future facial recognition applications. By combining these components, we can create a powerful and accurate facial recognition system that is efficient and easy to use.
## How to use 
To use this facial recognition system, follow the instructions below:

Clone the repository and navigate to the project directory in the terminal.
 
To clone 
git clone https://github.com/satrajitghosh183/Face_Detection.git

Install the required packages using the following command:

pip install -r requirements.txt

Run the Flask application using the following command:


python .\FlaskImplementation5.py
This will start the Flask server and you should see a message similar to the following:


Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
![Screenshot 2023-04-12 095412](https://user-images.githubusercontent.com/83156880/231350046-87f4a987-0d62-44d2-a2cc-e62f9b7b7c02.png)


Open your web browser and navigate to the local host address shown in the terminal message ( http://127.0.0.1:5000/.)

Click the "Start" button to begin capturing video from your device's camera and detecting faces in real-time.

If a face is detected, the facial landmarks will be extracted using MediaPipe and stored in a CSV file offline using Flask.

To stop the facial recognition system, click the "Stop" button.

That's it! With these simple steps, you can use the facial recognition system to detect faces in real-time video streams, extract facial landmarks, and store them in a CSV file for future use. Note that you may need to modify the code to suit your specific needs, such as changing the parameters for face detection or facial landmark extraction
![image](https://user-images.githubusercontent.com/83156880/231350664-9cc62ad3-12c4-4963-ade5-45cde934568f.png)
![image](https://user-images.githubusercontent.com/83156880/231350728-78cc7b73-a2ff-4974-8210-08203a41838d.png)
![image](https://user-images.githubusercontent.com/83156880/231350710-788f5695-4512-496a-8fb6-3d386b7a2c3a.png)
![image](https://user-images.githubusercontent.com/83156880/231350776-bcfc060e-e824-4b02-9d15-fff399c50682.png)


Project Members 
Satrajit Ghosh(satrajitghosh183)--Backend(Python,Flask)


Subhramoy Biswas(Subhramoy9)--Frontend(React JS,CSS,HTML,Flask)


Anubhab Paul(cypher-2000)-----Deployment(Flask)


