
import cv2
import os
from deepface import DeepFace
from datetime import datetime

# Folder where stored face images are kept
stored_image_folder = "path/to/stored_faces"  # Change this to the folder where stored images are saved
save_path = "path/to/save"  # Folder to save captured face images

# Function to read student status
def read_status():
    try:
        with open("status.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0"  # Default status

# Function to update student status
def update_status(status):
    with open("status.txt", "w") as f:
        f.write(str(status))

# Function to send email notifications (Stub)
def send_email(message):
    print(f"Email Sent: {message}")

# Start Video Capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Face Recognition", frame)

    # Press 's' to capture and compare
    if cv2.waitKey(1) & 0xFF == ord('s') and len(faces) > 0:
        x, y, w, h = faces[0]  # Take first detected face
        face_crop = frame[y:y+h, x:x+w]  # Crop face
        captured_path = f"{save_path}/captured_face.jpg"
        cv2.imwrite(captured_path, face_crop)  # Save the cropped face

        match_found = False
        varified = False
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Compare with stored images
        for filename in os.listdir(stored_image_folder):
            stored_image_path = os.path.join(stored_image_folder, filename)
            
            try:
                result = DeepFace.verify(img1_path=captured_path, img2_path=stored_image_path)
                if result["verified"]:
                    print(f"Match Found: {filename}")
                    print("Verified!!")
                    varified = True
                    print("Student Entry Time:", current_datetime)

                    status = read_status()
                    print("Current Status:", status)

                    if status == '1':
                        update_status(0)
                        student_status = "Inside"
                    else:
                        update_status(1)
                        student_status = "Outside"

                    print(f"Student Status: {student_status}")
                    send_email(message=f"Your child is {student_status} the bus at {current_datetime}")

                    match_found = True
                    break  # Stop when a match is found
            except Exception as e:
                print(f"Error comparing face: {e}")
                continue

        if not match_found:
            print("No Match Found")

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
    