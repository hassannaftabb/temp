import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from PIL import Image, ImageTk
import threading
import pandas as pd

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance System")
        self.root.geometry("1200x800")
        
        # Initialize variables
        self.path = 'dataset'
        self.images = []
        self.names = []
        self.known_encodings = []
        self.is_running = False
        
        # Create dataset directory if it doesn't exist
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            
        # Create main notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Create tabs
        self.dataset_tab = ttk.Frame(self.notebook)
        self.monitor_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dataset_tab, text='Dataset Management')
        self.notebook.add(self.monitor_tab, text='Attendance Monitor')
        
        # Initialize GUI elements
        self.create_dataset_widgets()
        self.create_monitor_widgets()
        
        # Load existing images
        self.load_existing_images()
        
    def create_dataset_widgets(self):
        # Left frame for image upload
        left_frame = ttk.Frame(self.dataset_tab)
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=5)
        
        # Name entry
        ttk.Label(left_frame, text="Enter Name:").pack(pady=5)
        self.name_entry = ttk.Entry(left_frame)
        self.name_entry.pack(pady=5)
        
        # Upload button
        self.upload_btn = ttk.Button(left_frame, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack(pady=10)
        
        # Status label
        self.status_label = ttk.Label(left_frame, text="Status: Ready")
        self.status_label.pack(pady=10)
        
        # Image preview
        self.preview_label = ttk.Label(left_frame)
        self.preview_label.pack(pady=10)
        
        # Right frame for dataset list
        right_frame = ttk.Frame(self.dataset_tab)
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=5)
        
        # Dataset list
        ttk.Label(right_frame, text="Current Dataset:").pack(pady=5)
        self.dataset_list = ttk.Treeview(right_frame, columns=('Name',), show='headings')
        self.dataset_list.heading('Name', text='Name')
        self.dataset_list.pack(fill='both', expand=True)
        
        # Delete button
        self.delete_btn = ttk.Button(right_frame, text="Delete Selected", command=self.delete_selected)
        self.delete_btn.pack(pady=10)
        
    def create_monitor_widgets(self):
        # Left frame for camera
        left_frame = ttk.Frame(self.monitor_tab)
        left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=5)
        
        # Camera preview
        self.camera_label = ttk.Label(left_frame)
        self.camera_label.pack(pady=10)
        
        # Start/Stop button
        self.start_btn = ttk.Button(left_frame, text="Start Camera", command=self.toggle_camera)
        self.start_btn.pack(pady=10)
        
        # Right frame for attendance table
        right_frame = ttk.Frame(self.monitor_tab)
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=5)
        
        # Attendance table
        ttk.Label(right_frame, text="Attendance Records:").pack(pady=5)
        self.attendance_table = ttk.Treeview(right_frame, 
                                           columns=('Name', 'Date', 'Time'),
                                           show='headings')
        self.attendance_table.heading('Name', text='Name')
        self.attendance_table.heading('Date', text='Date')
        self.attendance_table.heading('Time', text='Time')
        self.attendance_table.pack(fill='both', expand=True)
        
        # Load existing attendance records
        self.load_attendance_records()
        
    def load_attendance_records(self):
        """Load existing attendance records into the table"""
        if os.path.exists('Attendance.csv'):
            df = pd.read_csv('Attendance.csv')
            for _, row in df.iterrows():
                self.attendance_table.insert('', 'end', values=(row['Name'], row['Date'], row['Time']))
                
    def delete_selected(self):
        """Delete selected image from dataset"""
        selected = self.dataset_list.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an entry to delete")
            return
            
        name = self.dataset_list.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", f"Delete {name} from dataset?"):
            # Remove from dataset
            index = self.names.index(name)
            self.names.pop(index)
            self.images.pop(index)
            
            # Delete file
            os.remove(f'{self.path}/{name}.jpg')
            
            # Update list
            self.dataset_list.delete(selected[0])
            
            # Regenerate encodings
            self.generate_encodings()
            
    def load_existing_images(self):
        """Load existing images from dataset folder"""
        if os.path.exists(self.path):
            myList = os.listdir(self.path)
            for cl in myList:
                try:
                    img_path = f'{self.path}/{cl}'
                    img = cv2.imread(img_path)
                    if img is not None and not img.size == 0:
                        self.images.append(img)
                        name = os.path.splitext(cl)[0]
                        self.names.append(name)
                        self.dataset_list.insert('', 'end', values=(name,))
                except Exception as e:
                    print(f"Error loading image {cl}: {str(e)}")
            
            if self.images:
                self.generate_encodings()
            else:
                self.status_label.config(text="Status: No valid images found in dataset")
            
    def generate_encodings(self):
        """Generate encodings for all known faces"""
        self.known_encodings = []
        for i, img in enumerate(self.images):
            try:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encodings = face_recognition.face_encodings(img_rgb)
                if encodings:
                    self.known_encodings.append(encodings[0])
                else:
                    print(f"Warning: No face found in image for {self.names[i]}")
            except Exception as e:
                print(f"Error processing image for {self.names[i]}: {str(e)}")
            
    def upload_image(self):
        """Handle image upload"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a name")
            return
            
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        if file_path:
            try:
                # Read and validate image
                img = cv2.imread(file_path)
                if img is None or img.size == 0:
                    messagebox.showerror("Error", "Failed to load image")
                    return
                
                # Check if image contains a face
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(img_rgb)
                
                if not face_locations:
                    messagebox.showerror("Error", "No face detected in the image")
                    return
                
                # Save image and update system
                cv2.imwrite(f'{self.path}/{name}.jpg', img)
                self.images.append(img)
                self.names.append(name)
                self.dataset_list.insert('', 'end', values=(name,))
                self.generate_encodings()
                
                # Clear name entry
                self.name_entry.delete(0, 'end')
                
                messagebox.showinfo("Success", f"Image uploaded successfully for {name}")
                self.status_label.config(text=f"Status: {len(self.images)} images loaded")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process image: {str(e)}")
                
    def toggle_camera(self):
        """Toggle camera on/off"""
        if not self.is_running:
            if not self.known_encodings:
                messagebox.showwarning("Warning", "No face encodings available. Please upload some images first.")
                return
                
            self.is_running = True
            self.start_btn.config(text="Stop Camera")
            threading.Thread(target=self.run_camera, daemon=True).start()
        else:
            self.is_running = False
            self.start_btn.config(text="Start Camera")
            
    def run_camera(self):
        """Run face recognition camera"""
        cap = cv2.VideoCapture(0)
        
        while self.is_running:
            success, img = cap.read()
            if not success:
                break
                
            try:
                # Resize image for faster face recognition
                img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
                
                # Detect faces in current frame
                faces_current_frame = face_recognition.face_locations(img_small)
                encodes_current_frame = face_recognition.face_encodings(img_small, faces_current_frame)
                
                # Check each face in the frame
                for encodeFace, faceLoc in zip(encodes_current_frame, faces_current_frame):
                    matches = face_recognition.compare_faces(self.known_encodings, encodeFace)
                    face_dis = face_recognition.face_distance(self.known_encodings, encodeFace)
                    
                    if len(face_dis) > 0:
                        matchIndex = np.argmin(face_dis)
                        
                        if matches[matchIndex]:
                            name = self.names[matchIndex].upper()
                            y1, x2, y2, x1 = faceLoc
                            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                            
                            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                            
                            self.mark_attendance(name)
                
                # Convert image for tkinter
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(img_rgb)
                img_tk = ImageTk.PhotoImage(image=img_pil)
                
                # Update preview
                self.camera_label.config(image=img_tk)
                self.camera_label.image = img_tk
                
            except Exception as e:
                print(f"Error in camera processing: {str(e)}")
                continue
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        
    def mark_attendance(self, name):
        """Mark attendance in CSV file and update table"""
        if not os.path.exists('Attendance.csv'):
            with open('Attendance.csv', 'w') as f:
                f.write('Name,Date,Time')
                
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
                
                # Update attendance table
                self.attendance_table.insert('', 0, values=(name, date_string, time_string))

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.mainloop() 