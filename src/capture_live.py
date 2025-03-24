import cv2
import os
from deepface import DeepFace
from datetime import datetime
from . send import send_email

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
current_datetime = now.strftime("%Y-%m-%d %H:%M:%S")


def read_status():
    file_path = "entry_status.txt"
    if not os.path.exists(file_path):
        # return "Not Available"  # Default value when file doesn't exist
        update_status(1)
        return "1"

    with open(file_path, "r", encoding="utf-8") as file:
        status = file.read().strip()  # Strip to avoid unwanted newlines
    return status or "Not Available"  # Handle empty file case

# def read_status():
#     with open("assets/entry_status.txt","r") as file:
#         status = file.read()
#     return status

# def update_status(status):
#     with open("assets/entry_status.txt","w") as file:
#         file.write(str(status))

def update_status(status):
    with open("entry_status.txt", "w", encoding="utf-8") as file:
        file.write(str(status))



def capture_and_verify(stored_image_folder):
    # Load pre-trained face detection model (Haar cascade)
    save_path = "F:/School_Bus_Safety_System/captured_student_faces"
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Initialize webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(50, 50))

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.putText(frame, "Face Captured!", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        cv2.imshow("Live Face Capture", frame)

        # Press 's' to capture and compare
        if cv2.waitKey(1) & 0xFF == ord('s') and len(faces) > 0:
            x, y, w, h = faces[0]  # Take first detected face
            face_crop = frame[y:y+h, x:x+w]  # Crop face
            # captured_path = f"captured_face.jpg"
            captured_path =  f"{save_path}/captured_face.jpg"
            cv2.imwrite(captured_path, face_crop)  # Save the cropped face
            
            match_found = False
            # Compare with stored images
            for filename in os.listdir(stored_image_folder):
                stored_image_path = os.path.join(stored_image_folder, filename)

                try:
                    result = DeepFace.verify(img1_path=captured_path, img2_path=stored_image_path)
                    if result["verified"]:
                        # global entry_status
                        # entry_status = 1 # Student is  inside the bus now
                        print(f"Match Found: {filename}")
                        print("Varified!!")
                        varified = True
                        print("Student Entry Time: ", current_datetime)

                        status = read_status()
                        print("Current Status: ", status)
                        # print(type(status))
                        if status == '1':
                            update_status(0)
                            print("Student Status: Inside")
                            student_status = "Inside"
                            send_email(message=f"Your child  is {student_status}  the bus at {current_datetime}")
                        else:
                            print("Student Status: Outside")
                            update_status(1)
                            student_status = "Outside"
                            send_email(message=f"Your child  is {student_status}  the bus at {current_datetime}")
                        
                        match_found = True
                        cap.release()
                        cv2.destroyAllWindows()
                        return status, current_datetime, student_status, varified  # Stop when a match is found
                except:
                    continue
            
            if not match_found:
                print("No Match Found")
                break

    cap.release()
    cv2.destroyAllWindows()

    return status, current_datetime, student_status, varified

# Folder where stored images exist
# stored_folder = "F:/School_Bus_Safety_System/student_faces/"
# capture_and_verify(stored_folder)

def start_capturing():
    stored_folder = "F:/School_Bus_Safety_System/student_faces/"
    status, current_datetime, student_status, varified=capture_and_verify(stored_folder)
    
    return status, current_datetime, student_status, varified
