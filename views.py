from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Question, Choice, Submission


def get_enrollment(user, course):
    try:
        return Enrollment.objects.get(user=user, course=course)
    except Enrollment.DoesNotExist:
        return None


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    enrollment = get_enrollment(user, course)

    if not enrollment:
        return redirect('onlinecourse:course_details', pk=course_id)

    if request.method == 'POST':
        submission = Submission.objects.create(enrollment=enrollment)
        selected_ids = []
        for key, values in request.POST.items():
            if key.startswith('choice'):
                for value in request.POST.getlist(key):
                    selected_ids.append(int(value))

        selected_choices = Choice.objects.filter(id__in=selected_ids)
        submission.choices.set(selected_choices)
        submission.save()

        return redirect('onlinecourse:show_exam_result', course_id=course_id, submission_id=submission.id)

    return redirect('onlinecourse:course_details', pk=course_id)


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, id=course_id)
    submission = get_object_or_404(Submission, id=submission_id)
    selected_ids = submission.choices.values_list('id', flat=True)

    total_score = 0
    questions = Question.objects.filter(course=course)
    for question in questions:
        if question.is_get_score(selected_ids):
            total_score += question.grade

    context = {
        'course': course,
        'submission': submission,
        'selected_ids': selected_ids,
        'total_score': total_score,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
