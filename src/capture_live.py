import cv2
import os
from deepface import DeepFace
from datetime import datetime
from   . send import send_email

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
    save_path = "F:/School_Bus_Safety_System/captured_student_faces"
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use CAP_DSHOW for better stability on Windows

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None, None, None, False  # Exit gracefully

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame")
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(50, 50))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Live Face Capture", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s') and len(faces) > 0:
            x, y, w, h = faces[0]  
            face_crop = frame[y:y+h, x:x+w]
            captured_path = f"{save_path}/captured_face.jpg"
            cv2.imwrite(captured_path, face_crop)  

            match_found = False
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for filename in os.listdir(stored_image_folder):
                stored_image_path = os.path.join(stored_image_folder, filename)

                try:
                    result = DeepFace.verify(img1_path=captured_path, img2_path=stored_image_path)
                    if result["verified"]:
                        match_found = True
                        varified = True
                        student_status = "Inside" if read_status() == '1' else "Outside"
                        
                        # Toggle student status
                        update_status(0 if student_status == "Inside" else 1)

                        # Send email notification
                        send_email(message=f"Your child is {student_status} the bus at {current_datetime}")

                        print(f"Match Found: {filename}")
                        print("Verified!")
                        print("Student Entry Time: ", current_datetime)
                        print("Student Status: ", student_status)

                        cap.release()
                        cv2.destroyAllWindows()
                        return "Match Found", current_datetime, student_status, varified  
                except:
                    continue

            if not match_found:
                print("No Match Found!")
                cap.release()
                cv2.destroyAllWindows()
                return "No Match!", "No Match Found", "Unknown Person", False  

        elif key == ord('q'):  # Press 'q' to exit the loop
            print("Exiting...")
            break

    cap.release()
    cv2.destroyAllWindows()
    return None, None, None, False  
# Folder where stored images exist
# stored_folder = "F:/School_Bus_Safety_System/student_faces/"
# capture_and_verify(stored_folder)

def start_capturing():
    stored_folder = "F:/School_Bus_Safety_System/student_faces/"
    status, current_datetime, student_status, varified=capture_and_verify(stored_folder)
    
    return status, current_datetime, student_status, varified


# status, current_datetime, student_status, varified = start_capturing()

# print(status, current_datetime, student_status, varified )  