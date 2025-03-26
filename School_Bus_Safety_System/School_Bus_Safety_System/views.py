import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from backend.models import Student
from src.sms import send_sms
from dotenv import load_dotenv
load_dotenv()

# sys.path.append("F:/School_Bus_Safety_System")


from src.capture_live import start_capturing
from src.capture_image import capture_image
admin_phno = os.getenv("ADMIN_PHNO")

STD_ID = None

def take_input(flag):
    # flag = input("R to register new student, C to capture and compare and login:").lower()
    if flag == "r":
        result=capture_image()
        return result, None, None, None
    elif flag == "c":
        status, current_datetime, student_status, varified=start_capturing()
        return status, current_datetime, student_status, varified
    else:
        print("Invalid input")
        return "Invalid input", None, None, None


def take_attendence(request):
    status, current_datetime, student_status, varified=start_capturing()
    student_id = request.session.get('student_id')  # Assuming student_id is stored in the session during login
    try:
        student = Student.objects.get(rollno=student_id)
        parents_no = f"+91{student.parent_contact}"
        print("parents contact ::", student.parent_contact)
        print(parents_no)
        print(type(parents_no))

        if varified:
            send_sms(phone_number=parents_no,message=f"Your child is {student_status} the bus at {current_datetime}")
        else:
            send_sms(phone_number=admin_phno,message=f"Unknown Person Detected in the bus at {current_datetime}")
        # Fetch the student object using the roll number

        # # Create a new TravelStatus record
        # travel_status = TravelStatus.objects.create(
        #     student=student,
        #   # Reference the rollno field
        #     datetime=current_datetime,
        #     status=status,
        #     varified=varified
        # )

      

    except Student.DoesNotExist:
        # Handle the case where the student does not exist
        print("Student does not exist.")
        return "Student not found", None, None, None

    # Return the attendance details
    return status, current_datetime, student_status, varified
    


def mylocation_view(request):
    return render(request, 'templates/mylocation.html')

def register_student(request):
    if request.method == 'POST':
        rollno = request.POST.get('rollno_pic')
        result=capture_image(rollno)
        messages.success(request, result)
        status = "Student Registration Success"
        messages.success(request, "Student  registered successfully!")
        return render(request,'admin.html', {'status':status})
    return HttpResponse("Invalid request")

def show_admin_previlages(request,status=None):
    return render(request, 'admin_authentication.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username_admin_login')
        password = request.POST.get('password_login_admin')

        # Check if the admin credentials are correct
        if username == os.getenv("ADMIN_USERNAME") and password == os.getenv("ADMIN_PASSWORD"):  # Replace with your admin credentials
            # Set the session variable to indicate the admin is logged in
            messages.success(request, "Admin login successful!")
            return render(request,'admin.html')  # Replace with the name of your admin privileges URL
        else:
            return HttpResponse("Invalid admin credentials.")

    return render(request, 'admin_authentication.html')


STATUS = None
CURRENT_DATETIME = None
STUDENT_STATUS = None
VARIFIED = None

def index(request):
    if request.method == 'POST':
        status, current_datetime, student_status, varified = take_attendence(request)
        global CURRENT_DATETIME,STATUS,STUDENT_STATUS,VARIFIED
        STATUS = status
        CURRENT_DATETIME = current_datetime
        STUDENT_STATUS = student_status
        VARIFIED = varified
        return render(request, 'index.html',
                      {'status':status, 'current_datetime':current_datetime, 
                       'student_status':student_status, 
                       'varified':varified})
    return render(request, 'index.html')


def home(request):
    return render(request, 'test.html')


def show_parents_view(request):
    if request.method == 'Post':
        pass 
       # Retrieve the currently logged-in student's details
    student_id = request.session.get('student_id')  # Assuming student_id is stored in the session during login
    try:
        student = Student.objects.get(rollno=int(student_id))
      
          # Fetch the student details from the database
        print("Student name:", student.name)
        print("Student name:", student.rollno)
    except Student.DoesNotExist:
        student = None  # Handle the case where the student does not exist

    # Pass the student details to the template
    display_status = {'status':STATUS, 'current_datetime':CURRENT_DATETIME, 'student_status':STUDENT_STATUS, 'varified':VARIFIED}
    return render(request, 'parents_view.html', {'student': student, 'display_status':display_status})
    # return render(request, 'parents_view.html', {'student': student})

def logout(request):
    logout(request)
    messages.success(request, "Logout successful!")
    return redirect('login')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username_login')
        password = request.POST.get('password_login')

        try:
            # Check if the user exists in the custom model
            student = Student.objects.get(username=username)

            # Verify the password
            if student.password == password:  # Replace with hashed password check if applicable
                # Store the student in the session
                request.session['student_id'] = student.rollno
                global STD_ID
                STD_ID = student.rollno
                print(student.rollno)
                messages.success(request, "Login successful!")
                return redirect("parents_view")
            else:
                messages.error(request, "Invalid username or password.")
        except Student.DoesNotExist:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

    # name rollno class student phno parents phno busroute 
from django.shortcuts import render

def signup(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        rollno = request.POST.get('rollno')
        student_class = request.POST.get('std_class')  
        student_phno = request.POST.get('student_phno')
        parents_phno = request.POST.get('parents_phno')
        busroute = request.POST.get('busroute')
        username = request.POST.get('sign_username')
        password = request.POST.get('sign_password')
        confirm_password = request.POST.get('confirm_password')


        if password != confirm_password:
            return HttpResponse( 'Passwords do not match!')

        if User.objects.filter(username=username).exists():
            return HttpResponse({ "Username already exists. Choose a different one."}, status=400)

        myuser = User.objects.create_user(username, password)
        myuser.fullname = fullname
        myuser.rollno = rollno
        myuser.student_class = student_class
        myuser.student_phno = student_phno
        myuser.parents_phno = parents_phno
        myuser.busroute = busroute


        myuser.save()
        messages.success(request, 'Signup successful!')

        return redirect('login')
    


    return render(request, 'signup.html')