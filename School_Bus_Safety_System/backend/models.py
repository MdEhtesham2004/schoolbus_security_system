from django.db import models

# Create your models here.
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    stuclass  = models.CharField(max_length=20)
    rollno =  models.IntegerField()
    grade = models.CharField(max_length=10)
    student_contact = models.CharField(max_length = 10 ,null=True)
    parent_contact = models.CharField(max_length=10)
    busroute = models.CharField(max_length=10)

    def __str__(self):
        return self.username





# name rollno class student phno parents phno busroute 
