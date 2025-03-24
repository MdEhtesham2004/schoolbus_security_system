from deepface import DeepFace
import os 
def compare_images_deepfake(image_path1, image_path2):
    try:
        result = DeepFace.verify(image_path1, image_path2, model_name="Facenet")
        verified = result["verified"]
        # print(verified)
        # print(result)
    except Exception as e:
        print("Error:", e)
        verified = False
        result = {}
    return (verified, result)

varified_list = []
for i in range(34):
    image_path = f"F:\School_Bus_Safety_System\student_faces\{i}.jpg"
    if not os.path.exists(image_path):
        continue 
    else : 
        varified,result = compare_images_deepfake("F:/School_Bus_Safety_System/captured_student_faces/32.jpg",image_path)
        if varified:
            print("varified!!")
            break
if not varified:
    print("No user found!!")



            




# varified,result = compare_images_deepfake("F:\School_Bus_Safety_System\captured_student_faces\31.jpg", "F:\School_Bus_Safety_System\student_faces\31.jpg")

# print(varified,result)
