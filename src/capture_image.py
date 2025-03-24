import cv2
import os

def capture_image(id):
    # Create folder to store images if not exists
    dataset_path = "F:/School_Bus_Safety_System/student_faces"
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path,exist_ok=True)

    # student_id = input("Enter Student ID: ")
    student_id = id

    cap = cv2.VideoCapture(0)  # Open webcam
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_img = gray[y:y + h, x:x + w]
            filename = f"{dataset_path}/{student_id}.jpg"
            cv2.imwrite(filename, face_img)  # Save the captured face image
            
            # Draw rectangle around the detected face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, "Face Captured!", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        cv2.imshow("Face Capture", frame)

        if cv2.waitKey(1) & 0xFF == ord("q") or len(faces) > 0:  # Press 'q' or capture 1 image to exit
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Face image saved as {filename}")
    return "Success"
