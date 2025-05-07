from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from account.models import Profile
from .models import Quiz, Category
from django.db.models import Q
from quiz.models import QuizSubmission
from django.contrib import messages

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
      
      # get the score
      score = int(request.POST.get('score', 0))

      # save the new quiz submission 
      submission = QuizSubmission(user=request.user, quiz=quiz, score=score)
      submission.save()
      return redirect('quiz_result', submission_id = submission.id)

  
   return render(request,'test.html',{'quiz':quiz})

@login_required
def quiz_result_view(request,submission_id):

   submission = get_object_or_404(QuizSubmission, pk=submission_id)

   context ={'submission': submission}
   return render(request, 'test-result.html', context)

