import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import filedialog
import dlib
from math import hypot
import matplotlib.pyplot as plt
import imutils
from imutils import face_utils

class Video:
    def __init__(self):
        file_path = filedialog.askopenfilename()
      
        # Create a VideoCapture object and read from input file
        # If the input is the camera, pass 0 instead of the video file name
        self.cap = cv.VideoCapture(r'{0}'.format(file_path))
        #self.cap = cv.VideoCapture(r"C:\Users\Lenovo\Documents\morse\hello.mp4")
        self.cap.set(3, 1920)
        self.cap.set(4, 1080)
        # Check if camera opened successfully

        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(r"C:\Users\Lenovo\Documents\Morse\shape_predictor_68_face_landmarks.dat")

        font = cv.FONT_HERSHEY_PLAIN

        def midpoint(p1 ,p2):
            return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

        def euclidean_distance(leftx,lefty, rightx, righty):
            return np.sqrt((leftx-rightx)**2 +(lefty-righty)**2)

        # Defining the eye aspect ratio
        def get_EAR(eye_points, facial_landmarks):
        # Defining the left point of the eye   
            left_point = [facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y]
        # Defining the right point of the eye   
            right_point = [facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y]
        # Defining the top mid-point of the eye    
            center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
        # Defining the bottom mid-point of the eye   
            center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))
        # Drawing horizontal and vertical line       
            hor_line = cv.line(frame, (left_point[0], left_point[1]), (right_point[0], right_point[1]), (255, 0, 0), 3)
            ver_line = cv.line(frame, (center_top[0], center_top[1]),(center_bottom[0], center_bottom[1]), (255, 0, 0), 3)
         # Calculating length of the horizontal and vertical line    
            hor_line_lenght = euclidean_distance(left_point[0], left_point[1], right_point[0], right_point[1])
            ver_line_lenght = euclidean_distance(center_top[0], center_top[1], center_bottom[0], center_bottom[1])
         # Calculating eye aspect ratio     
            EAR = ver_line_lenght / hor_line_lenght
            return EAR

        if (self.cap.isOpened()== False):
          print("Error opening video stream or file")
        # Read until video is completed
    
        self.eye_blink_signal=[]
        # Creating an object blink_ counter
        blink_counter = 0
        previous_ratio = 100
        blinking_ratio_rounded = 0

        while True:
            ret, frame = self.cap.read()
            if ret == False:
                break
            
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = detector(gray)

            for face in faces:
                x, y = face.left(), face.top()
                x1, y1 = face.right(), face.bottom()

                landmarks = predictor(gray, face)
                 
            # Calculating left eye aspect ratio    
                left_eye_ratio = get_EAR([36, 37, 38, 39, 40, 41], landmarks)
            # Calculating right eye aspect ratio  
                right_eye_ratio = get_EAR([42, 43, 44, 45, 46, 47], landmarks)
            # Calculating aspect ratio for both eyes  
                blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2
            # Rounding blinking_ratio on two decimal places   
                blinking_ratio_1 = blinking_ratio * 100
                blinking_ratio_2 = np.round(blinking_ratio_1)
                blinking_ratio_rounded = blinking_ratio_2 / 100
            # Appending blinking ratio to a list eye_blink_signal
                self.eye_blink_signal.append(blinking_ratio)
                if blinking_ratio < 0.20:
                  if previous_ratio > 0.20:
                    blink_counter = blink_counter + 1
             # Displaying blink counter and blinking ratio in our output video      
    
                previous_ratio = blinking_ratio
  
            cv.putText(frame, "Blink count: " +str(blink_counter), (30, 50), font, 1, (0, 0, 255),2)
            cv.putText(frame, "EAR: " +str(blinking_ratio_rounded), (30, 70), font, 1, (0, 0, 255),2)
                
                
            cv.imshow("Frame", frame)
            key = cv.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        self.cap.release()
        cv.destroyAllWindows() 
        input('press any key to exit')
        plt.plot(self.eye_blink_signal)
        plt.xlabel("Frames")
        plt.ylabel('EAR')
        plt.title('')
        plt.axhline(y = 0.20, color = 'r', linestyle = '-')
        plt.show()
        count = []
        cnt = 0
        cn = []
        c = 0

        for ratio in self.eye_blink_signal:
           if ratio<0.20:
               cnt+= 1
           if ratio>=0.20:
               count.append(cnt)
               cnt = 0
        for i in count:
            if i == 0:
                c += 1
            else:
                cn.append(c)
                c = 0
        print(cn)

if __name__ == "__main__":
    Video()