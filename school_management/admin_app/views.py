from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Student, Teacher, Transcript
from sklearn.linear_model import LinearRegression
import pandas as pd
from django.contrib import messages

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    transcripts = Transcript.objects.all()

    # Handle PDF upload
    if request.method == 'POST' and 'pdf_file' in request.FILES:
        student_id = request.POST.get('student_id')
        level = request.POST.get('level')
        pdf_file = request.FILES['pdf_file']
        student = Student.objects.get(id=student_id)
        transcript = Transcript.objects.create(student=student, level=level, pdf_file=pdf_file)
        transcript.extract_marks()
        messages.success(request, "Transcript uploaded and marks extracted.")

    # AI Prediction
    df = pd.DataFrame(list(transcripts.values('student__id', 'extracted_marks')))
    predictions = []
    if not df.empty:
        X = df['extracted_marks'].apply(lambda x: sum(x.values()) / len(x) if x else 0).values.reshape(-1, 1)
        y = df['student__id']
        model = LinearRegression().fit(X, y)
        predictions = model.predict(X)

    context = {
        'students': students,
        'teachers': teachers,
        'transcripts': transcripts,
        'total_students': students.count(),
        'predictions': predictions.tolist(),
    }
    return render(request, 'admin/dashboard.html', context)