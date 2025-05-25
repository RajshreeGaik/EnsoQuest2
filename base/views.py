from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from account.models import Profile
from quiz.models import UserRank, Quiz, QuizSubmission, Question
from django.contrib.auth.decorators import login_required,user_passes_test
import datetime
from .models import Message, Blog
from django.db.models import Count, Q
import math
from django.db.models.functions import ExtractYear
from .models import Feedback
from .models import Notice
from .form import NoticeForm


# Create your views here.
def home(request):

    leaderboard_users = UserRank.objects.order_by('rank')[:4]

    context={"leaderboard_users":leaderboard_users}

    return render(request, 'welcome.html', context)

@login_required(login_url="login")
def leaderboard_view(request):

    user_object = request.user
    user_profile = request.user.profile
    
    leaderboard_users = UserRank.objects.order_by('rank')
    

    context = {"leaderboard_users":leaderboard_users}
    return render(request, "Leaderboard.html", context)

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
@login_required
def dashboard_view(request):

    # Total Number
    total_users = User.objects.all().count()
    total_quizzes = Quiz.objects.all().count()
    total_quiz_submit = QuizSubmission.objects.all().count()
    total_questions = Question.objects.all().count()

    # today_numbers
    today_users = User.objects.filter(date_joined__date=datetime.date.today()).count()
    today_quizzes_objs = Quiz.objects.filter(created_at__date=datetime.date.today())
    today_quizzes = Quiz.objects.filter(created_at__date=datetime.date.today()).count()
    today_quiz_submit = QuizSubmission.objects.filter(submitted_at__date=datetime.date.today()).count()
    today_questions = 0
    for quiz in today_quizzes_objs:
        today_questions += quiz.question_set.count()

    # Gain %
    gain_users = gain_percentage(total_users, today_users)
    gain_quizzes = gain_percentage(total_quizzes, today_quizzes)
    gain_quiz_submit = gain_percentage(total_quiz_submit, today_quiz_submit)
    gain_questions = gain_percentage(total_questions, today_questions)

    # Inbox Messages
    messages = Message.objects.filter(created_at__date=datetime.date.today()).order_by('-created_at')

    context = {
               "total_users": total_users,
               "total_quizzes": total_quizzes,
               "total_quiz_submit": total_quiz_submit,
               "total_questions": total_questions,
               "today_users":today_users,
               "today_quizzes":today_quizzes,
               "today_quiz_submit":today_quiz_submit,
               "today_questions":today_questions,
               "gain_users": gain_users,
               "gain_quizzes": gain_quizzes,
               "gain_quiz_submit": gain_quiz_submit,
               "gain_questions": gain_questions,
               "messages": messages,
                 }
    return render(request, "dashboard.html", context)

def gain_percentage(total, today):
    if total > 0 and today > 0:
        gain = math.floor((today *100)/total)
        return gain
    
def about_view(request):
    return render(request, "about.html")

def blogs_view(request):

    year_blog_count = Blog.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id')).order_by('-year').filter(status='public')

    blogs = Blog.objects.filter(status='public').order_by('-created_at')

    context={"year_blog_count":year_blog_count, "blogs": blogs}
    return render(request, "blogs.html", context)

@login_required
def blog_view(request,blog_id):

        blog = get_object_or_404(Blog, pk=blog_id)
        
        context={"blog": blog}
        return render(request, "blog.html", context)
    
@login_required
def contact_view(request):

        if request.method == "POST":
           subject = request.POST.get('subject')
           message = request.POST.get('message') 

           if subject is not None and Message is not None:
               form = Message.objects.create(user=request.user, subject=subject, message=message)
               form.save()
               messages.success(request, "we got your message. we will resolve your query soon.")
               return redirect('profile', request.user.username)
           
           else:
               return redirect('contact')
           
        return render(request, "contact.html")

@user_passes_test(is_superuser)
@login_required
def message_view(request, id):

    message = get_object_or_404(Message,pk=id)
    if not message.is_read:
        message.is_read = True
        message.save()
    
    context = {"message":message}
    return render(request, "message.html", context)

    
def terms_conditions_view(request):
    return render(request, "terms-conditions.html")

@login_required
def resources_view(request):

        return render(request, "resources.html")

def search_users_view(request):

    query = request.GET.get('q')

    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).order_by('date_joined')

    else: 
        users = []

 
    context={"query": query, "users":users}
    return render (request, "search-users.html", context)



@login_required
def feedback_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        rating = int(request.POST.get('rating'))
        expectations_met = request.POST.get('expectation')  # from form field
        improvement_suggestions = request.POST.get('improvement')  # from form field

        Feedback.objects.create(
            name=name,
            email=email,
            rating=rating,
            expectations_met=expectations_met,
            improvement_suggestions=improvement_suggestions,
        )
        # Add a success message
        messages.success(request, "Thank you for your feedback 😊🎉🙏!")
        # Redirect to feedback page to avoid form resubmission
        return redirect('feedback')  # Make sure 'feedback' is the name of your url pattern
    return render(request, "feedback.html")


def custom_404(request, exception):
    return render(request, '404.html', status=404)

from quiz.models import Quiz

def search_view(request):
    query = request.GET.get('q', '')
    if query:
        quizzes = Quiz.objects.filter(title__icontains=query)
    else:
        quizzes = Quiz.objects.none()  # or all() if you want everything to show by default

    context = {
        'quizzes': quizzes,
        'search_query': query,
    }

    return render(request, 'search_results.html', context)




# Check if user is admin
def is_admin(user):
    return user.is_superuser

# View all notices
@login_required
def notice_list(request):
    notices = Notice.objects.order_by('-created_at')
    return render(request, 'notice_list.html', {'notices': notices})

# Add a notice (admin only)
@login_required
@user_passes_test(is_admin)
def add_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notice_list')
    else:
        form = NoticeForm()
    return render(request, 'notice_form.html', {'form': form, 'action': 'Add'})

# Edit a notice (admin only)
@login_required
@user_passes_test(is_admin)
def edit_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('notice_list')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'notice_form.html', {'form': form, 'action': 'Edit'})




