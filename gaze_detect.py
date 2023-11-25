import cv2
import numpy as np
import dlib
from math import hypot  # X-Y Plant Distence
#import pyglet   # wav
import time
import os
import threading

from Ques_Window import windows

Question_path = os.path.abspath("Ques_Window.py")
cap = cv2.VideoCapture(0)
frames = 0
frames_to_blink = 3


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    #hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    #ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = hor_line_lenght / ver_line_lenght
    return ratio

def eyes_contour_points(facial_landmarks):
    left_eye = []
    right_eye = []
    for n in range(36, 42):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        left_eye.append([x, y])
    for n in range(42, 48):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        right_eye.append([x, y])
    left_eye = np.array(left_eye, np.int32)
    right_eye = np.array(right_eye, np.int32)
    return left_eye, right_eye

if __name__ == "__main__":

    Questions = windows()

    Que_t = threading.Thread(target=Questions.Control, args=["start"])
    Que_t.start()

    print("start detecting")
    while True:

        ret, frame = cap.read()
        rows, cols, _ = frame.shape
        frames += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Draw a white space for loading bar
        frame[rows - 50: rows, 0: cols] = (255, 255, 255)

        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)

            left_eye, right_eye = eyes_contour_points(landmarks)

            # Detect blinking
            left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
            right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
            blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

            # Eyes color
            cv2.polylines(frame, [left_eye], True, (0, 0, 255), 2)
            cv2.polylines(frame, [right_eye], True, (0, 0, 255), 2)

            if blinking_ratio > 5:
                # cv2.putText(frame, "BLINKING", (50, 150), font, 4, (255, 0, 0), thickness=3)
                blinking_frames += 1
                frames -= 1

                # Show green eyes when closed
                cv2.polylines(frame, [left_eye], True, (0, 255, 0), 2)
                cv2.polylines(frame, [right_eye], True, (0, 255, 0), 2)

                # Typing letter
                if blinking_frames == frames_to_blink:
                    
                    print("Blinked!!!!!!!!!!!!!!!!!!!!!")

                    #Questions.blinked = True
                    #result = Questions.result
                    signal_stop = threading.Thread(target=Questions.from_threading)
                    signal_stop.start()

                    #print(result)
                    #sound.play()
                    select_keyboard_menu = True
                    # time.sleep(1)

            else:
                blinking_frames = 0

            key = cv2.waitKey(1)
            if key == 27:
                break
        
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break


    Que_t.join()
    
    cap.release()
    cv2.destroyAllWindows()