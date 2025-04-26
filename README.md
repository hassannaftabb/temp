# Face Recognition Attendance System

A Python-based attendance system that uses facial recognition to track attendance.

## Setup Instructions

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Prepare the dataset:
   - Create a folder named `dataset` (already created)
   - Add photos of people to track in the dataset folder
   - Name each photo as the person's name (e.g., "john_doe.jpg")
   - Make sure each photo has exactly one face
   - Photos should be clear and well-lit

3. Run the system:
```bash
python attendance_system.py
```

## Usage

1. The system will start your webcam and begin detecting faces
2. When a recognized face is detected:
   - A green box will appear around the face
   - The person's name will be displayed
   - Attendance will be marked in `Attendance.csv`
3. Press 'q' to quit the application

## File Structure

- `attendance_system.py`: Main program file
- `requirements.txt`: Python dependencies
- `dataset/`: Folder containing face images
- `Attendance.csv`: CSV file storing attendance records

## Attendance Records

The system creates an `Attendance.csv` file with the following columns:
- Name
- Date
- Time

Each person is recorded only once per session. 