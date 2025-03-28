from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    profile_picture = models.ImageField(upload_to='students/', null=True, blank=True)
    year_of_intake = models.IntegerField()
    combination = models.CharField(max_length=100, default="Software Development & Embedded Systems")
    father_first_name = models.CharField(max_length=100)
    father_last_name = models.CharField(max_length=100)
    mother_first_name = models.CharField(max_length=100)
    mother_last_name = models.CharField(max_length=100)
    residence = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    parent_email = models.EmailField()
    nationality = models.CharField(max_length=100)

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    classes_taught = models.CharField(max_length=200)  # e.g., "Senior 6"
    courses_taught = models.CharField(max_length=200)  # e.g., "Maths, Physics"

class Transcript(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    level = models.CharField(max_length=50)  # e.g., "O-Level", "Senior 1"
    pdf_file = models.FileField(
        upload_to='transcripts/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        null=True,
        blank=True
    )
    extracted_marks = models.JSONField(null=True, blank=True)  # e.g., {"Maths": 85, "Physics": 78}
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def extract_marks(self):
        """Extract marks from PDF using pdfplumber."""
        import pdfplumber
        if self.pdf_file:
            with pdfplumber.open(self.pdf_file.path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                marks = {}
                for line in text.split('\n'):
                    if "Maths" in line:
                        marks["Maths"] = int(line.split()[-1])
                    elif "Physics" in line:
                        marks["Physics"] = int(line.split()[-1])
                    elif "ML" in line:
                        marks["ML"] = int(line.split()[-1])
                    elif "Cybersecurity" in line:
                        marks["Cybersecurity"] = int(line.split()[-1])
                    elif "English" in line:
                        marks["English"] = int(line.split()[-1])
                self.extracted_marks = marks
                self.save()