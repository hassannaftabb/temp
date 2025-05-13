import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

# Initialize paths and lists
path = 'dataset'
images = []
names = []
myList = os.listdir(path)

# Load images and create name list
for cl in myList:
    img = cv2.imread(f'{path}/{cl}')
    images.append(img)
    names.append(os.path.splitext(cl)[0])

def find_encodings(images):
    """Create encodings for all known faces"""
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list

def mark_attendance(name):
    """Mark attendance in CSV file"""
    with open('Attendance.csv', 'a+') as f:
        f.seek(0)
        data = f.readlines()
        name_list = []
        for line in data:
            entry = line.split(',')
            name_list.append(entry[0])

        if name not in name_list:
            now = datetime.now()
            time_string = now.strftime('%H:%M:%S')
            date_string = now.strftime('%Y-%m-%d')
            f.writelines(f'\n{name},{date_string},{time_string}')

# Create attendance file if it doesn't exist
if not os.path.exists('Attendance.csv'):
    with open('Attendance.csv', 'w') as f:
        f.write('Name,Date,Time')

# Generate encodings for known faces
print("Generating encodings for known faces...")
known_encodings = find_encodings(images)
print("Encoding Complete ✅")

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        print("Failed to grab frame")
        break

    # Resize image for faster face recognition
    img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)

    # Detect faces in current frame
    faces_current_frame = face_recognition.face_locations(img_small)
    encodes_current_frame = face_recognition.face_encodings(img_small, faces_current_frame)

    # Check each face in the frame
    for encodeFace, faceLoc in zip(encodes_current_frame, faces_current_frame):
        matches = face_recognition.compare_faces(known_encodings, encodeFace)
        face_dis = face_recognition.face_distance(known_encodings, encodeFace)
        
        if len(face_dis) > 0:  # Check if any known faces were found
            matchIndex = np.argmin(face_dis)
            
            if matches[matchIndex]:
                name = names[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                # Scale back up face locations
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                
                # Draw rectangle around face
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                
                # Mark attendance
                mark_attendance(name)

    # Display the image
    cv2.imshow('Webcam', img)

    # Break loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows() 