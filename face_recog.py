import os
# preload camera for faster loading times
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import sys
import imutils
import math

base_options = python.BaseOptions(model_asset_path='face_landmarker.task')
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=False,
    output_facial_transformation_matrixes=False,
    num_faces=1)
detector = vision.FaceLandmarker.create_from_options(options)
video_capture = cv.VideoCapture(0)

KNOWN_DISTANCE = 38.4 # cm
KNOWN_WIDTH = 27.7 # cm
KNOWN_PIXEL_WIDTH = 155 # cm
FOCAL_LENGTH = (KNOWN_PIXEL_WIDTH * KNOWN_DISTANCE) / KNOWN_WIDTH

face_width = 0

if not video_capture.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = video_capture.read()
    if not ret: break
    frame = imutils.resize(frame, width=450)
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    results = detector.detect(mp_image)
    ih, iw, ic = frame.shape

    if results.face_landmarks:
        face_landmarks = results.face_landmarks[0]
        forehead = face_landmarks[10]
        center_x = int(forehead.x * iw)
        center_y = int(forehead.y * ih)

        frame_center_x = iw / 2
        frame_center_y = ih / 2

        offset_x = center_x - frame_center_x
        offset_y = center_y - frame_center_y

        angle_x = math.degrees(math.atan2(offset_x, FOCAL_LENGTH))
        angle_y = math.degrees(math.atan2(offset_y, FOCAL_LENGTH))

        cv.circle(frame, (int(center_x), int(center_y)), 1, (0,0,255), 2)

    cv.imshow('Face Detection', frame)

    print("Angle x: ", angle_x, " deg. Angle y: ", angle_y, " deg.")

    # quit key = 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv.destroyAllWindows()