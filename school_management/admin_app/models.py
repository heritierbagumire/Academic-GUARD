from django.db import models

class EnrollmentData(models.Model):
    year = models.IntegerField(unique=True)
    total_students = models.IntegerField()
    new_students = models.IntegerField()
    graduating_students = models.IntegerField()
    retention_rate = models.FloatField()  # Percentage (e.g., 86.0 for 86%)

    def __str__(self):
        return f"Enrollment Data for {self.year}"