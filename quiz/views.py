from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Quiz, Category
from django.db.models import Q
from quiz.models import QuizSubmission
from django.contrib import messages
from quiz.models import Quiz, Category, QuizSubmission, Choice, QuizAnswer


# Create your views here.
@login_required
def all_quiz_view(request, category=None):

    quizzes = Quiz.objects.order_by('-created_at')
    categories = Category.objects.all()

    context = {"quizzes": quizzes, "categories": categories}
    return render(request, 'all-test.html', context)


@login_required
def search_view(request, category):

    #search by searchbar
    if request.GET.get('q') != None:
       q = request.GET.get('q')
       query = Q(title__icontains=q) | Q(description__icontains=q)
       quizzes = Quiz.objects.filter(query)

    #search by category
    elif category !=" ":
      quizzes = Quiz.objects.filter(category__name__iexact=category)
    

    else:
       quizzes = Quiz.objects.order_by('-created_at')


    categories = Category.objects.all()

    context = {"quizzes": quizzes, "categories": categories}
    return render(request, 'all-test.html', context)

@login_required
def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == "POST":
        score = 0
        submission = QuizSubmission.objects.create(user=request.user, quiz=quiz, score=0)

        for question in quiz.question_set.all():
            selected_id = request.POST.get(str(question.id))
            if selected_id:
                try:
                    selected_choice = Choice.objects.get(id=int(selected_id), question=question)
                except Choice.DoesNotExist:
                    selected_choice = None

                if selected_choice:
                    if selected_choice.is_correct:
                        score += 1
                    QuizAnswer.objects.create(
                        submission=submission,
                        question=question,
                        selected_choice=selected_choice
                    )
                else:
                    # No valid selected choice found — you can handle this if you want
                    pass

        submission.score = score
        submission.save()
        return redirect('quiz_result', submission_id=submission.id)

    return render(request, 'test.html', {'quiz': quiz})

def quiz_result_view(request, submission_id):
    submission = get_object_or_404(QuizSubmission, id=submission_id)

    total_questions = submission.quiz.question_set.count()
    correct_answers = QuizAnswer.objects.filter(
        submission=submission,
        selected_choice__is_correct=True
    ).count()

    all_answers = QuizAnswer.objects.filter(submission=submission)

    context = {
        'submission': submission,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'answers': all_answers,
    }

    return render(request, 'test-result.html', context)
