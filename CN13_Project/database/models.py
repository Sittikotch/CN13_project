from django.forms import ModelForm
from django.db import models

# Create your models here.

class Student(models.Model):
    DEPT_CHOICES = (
        ("Electrical Engineering", "EE"),
        ("Industrial Engineering", "IE"),
        ("Civil Engineering", "CE"),
        ("Chemical Engineering", "ChE"),
        ("Mechanical Engineering", "ME"),
        ("Computer Engineering", "CN")
    )

    userId = models.CharField(max_length=50, unique=True)
    sid = models.CharField(max_length=10)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    tel = models.CharField(max_length=10)
    dept = models.CharField(max_length=50,
                            choices=DEPT_CHOICES)

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['sid','fname','lname','tel','dept']
        labels = {
            'sid': 'student id',
            'fname': 'first name',
            'lname': 'last name',
            'tel': 'telephone number',
            'dept': 'department',
        }