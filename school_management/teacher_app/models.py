# Create your models here.
from django.db import models
from admin_app.models import Student, Teacher

class MarkCorrection(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    old_mark = models.IntegerField()
    new_mark = models.IntegerField()
    corrected_at = models.DateTimeField(auto_now_add=True)