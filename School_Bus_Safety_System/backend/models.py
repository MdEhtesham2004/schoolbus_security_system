from django.db import models

# Create your models here.
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    stuclass  = models.CharField(max_length=20)
    rollno =  models.IntegerField(unique=True)
    grade = models.CharField(max_length=10)
    student_contact = models.CharField(max_length = 10 ,null=True)
    parent_contact = models.CharField(max_length=10)
    busroute = models.CharField(max_length=10)

    def __str__(self):
        return self.username
    

class TravelStatus(models.Model):
    # student = models.ForeignKey(Student, on_delete=models.CASCADE,unique=True, related_name="travel_status")
    # rollno = models.ForeignKey(Student, to_field="rollno",unique=True, on_delete=models.CASCADE, related_name="travel_status_by_rollno")
    # student = models.ForeignKey('Student', on_delete=models.CASCADE)

    student = models.OneToOneField(Student, to_field="rollno", on_delete=models.CASCADE, related_name="travel_status_by_rollno")
    datetime = models.DateTimeField(auto_now_add=True)  # Automatically set the current date and time
    status = models.CharField(max_length=50)  # Example: "Present", "Absent", etc.
    varified = models.BooleanField(default=False)  # Boolean field to indicate verification status

    def __str__(self):
        return f"Travel Status for {self.student.name} on {self.datetime.strftime('%Y-%m-%d %H:%M:%S')}"
# name rollno class student phno parents phno busroute 
