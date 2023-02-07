# Computer-Vision
Short python training projects, work in progress.
Python **3.7.9**

Libraries:

OpenCV : Computer Vision library | pip install cv2 \
mediapipe : Trained recognition tool | pip install mediapipe \
pyzbar : Trained QR and BAR code reader | pip install pyzbar \
numpy : Mathmatecal computing | pip install numpy \
pycaw : | Core Audio Windows | pip install pycaw

**Note: mediapipe not yet compatible with Python 3.7+**


Descriptions:

Hand Gesture volume control.py:
Captures video with openCV, converts it to BGR. Recognises the hands with mediapipe, assigns 21 landmarks to each hand. Calculates the distance between the tip of the index and the tip of the thumb using math, and interprets it as the volume range using numpy then draws volume bar using openCV.

QR reader:
Captures video with openCV. Decodes capture with pyzbar, extracting QR contents, then prints ID on the screen.
