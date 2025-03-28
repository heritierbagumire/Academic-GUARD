from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from admin_app.models import Teacher, Transcript
from .models import MarkCorrection

def is_teacher(user):
    return user.is_authenticated and user.role == 'teacher'

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    teacher = Teacher.objects.get(email=request.user.email)
    transcripts = Transcript.objects.all()

    if request.method == 'POST':
        transcript_id = request.POST.get('transcript_id')
        subject = request.POST.get('subject')
        new_mark = request.POST.get('new_mark')
        transcript = Transcript.objects.get(id=transcript_id)
        old_mark = transcript.extracted_marks.get(subject, 0)
        transcript.extracted_marks[subject] = int(new_mark)
        transcript.save()
        MarkCorrection.objects.create(
            teacher=teacher,
            student=transcript.student,
            subject=subject,
            old_mark=old_mark,
            new_mark=new_mark
        )

    corrections = MarkCorrection.objects.filter(teacher=teacher)
    context = {
        'teacher': teacher,
        'transcripts': transcripts,
        'corrections': corrections,
    }
    return render(request, 'teacher/dashboard.html', context)