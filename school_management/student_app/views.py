from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from admin_app.models import Student, Transcript
from .models import Claim

def is_student(user):
    return user.is_authenticated and user.role == 'student'

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    student = Student.objects.get(email=request.user.email)
    transcripts = student.transcript_set.all()
    claims = Claim.objects.filter(student=student)

    if request.method == 'POST':
        subject = request.POST.get('subject')
        issue = request.POST.get('issue')
        Claim.objects.create(student=student, subject=subject, issue=issue)

    context = {
        'student': student,
        'transcripts': transcripts,
        'claims': claims,
    }
    return render(request, 'student/dashboard.html', context)