from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from account.models import Profile
from quiz.models import UserRank, Quiz, QuizSubmission, Question
from django.contrib.auth.decorators import login_required,user_passes_test
import datetime
from .models import *
from .form import *
from django.db.models import Count, Q
import math
from django.db.models.functions import ExtractYear
from django.forms import modelform_factory
from django.http import Http404
from django.db import transaction
from base.models import Notification
from .form import BlogForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from .models import Blog, Like, Comment
from .form import CommentForm


# Create your views here.
def home(request):
    leaderboard_users = UserRank.objects.order_by('rank')[:4]
    
    unread_count = 0
    if request.user.is_authenticated:
        unread_count = request.user.notification_set.filter(is_read=False).count()

    context = {
        "leaderboard_users": leaderboard_users,
        "unread_count": unread_count,
    }

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
#@user_passes_test(lambda u: u.is_staff)
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blogs')
    else:
        form = BlogForm()
    return render(request, 'create_blog.html', {'form': form})

# views.py
@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)

    # Optional: Only allow the author or admin to edit
    if request.user != blog.author and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to edit this blog.")

    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog', blog_id=blog.id)
    else:
        form = BlogForm(instance=blog)

    return render(request, 'edit_blog.html', {'form': form, 'blog': blog})

@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    liked = False

    # Toggle like
    like_obj, created = Like.objects.get_or_create(user=request.user, blog=blog)
    if not created:
        like_obj.delete()
    else:
        liked = True

    # Return JSON response for AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'like_count': blog.likes.count()
        })

    return redirect('blog', blog_id=blog_id)

@login_required
@login_required
def comment_blog(request, blog_id):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, id=blog_id)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(blog=blog, user=request.user, content=content)
        return redirect('blog', blog_id=blog.id)



    
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
    resources = Resource.objects.all()
    return render(request, "resource_list.html", {'resources': resources})

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



@login_required
def upload_resource(request):
    if not request.user.is_staff:
        return render(request, '403.html')  # Optional
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user
            resource.save()
            return redirect('resource_list')
    else:
        form = ResourceForm()
    return render(request, 'upload_resource.html', {'form': form})


@login_required
def feedback_dashboard(request):
    # Check if user is in TAD group
    is_tad = request.user.groups.filter(name='TAD').exists()

    if is_tad:
        forms = FeedbackForm.objects.filter(created_by=request.user)
        context = {'forms': forms, 'is_tad': True}
    else:
        assigned_forms = FeedbackForm.objects.filter(assigned_users=request.user)
        context = {'assigned_forms': assigned_forms, 'is_tad': False}

    return render(request, 'feedback_dashboard.html', context)


@login_required
@transaction.atomic
def create_feedback_form(request):
    # Only TAD group users allowed
    if not request.user.groups.filter(name='TAD').exists():
        messages.error(request, "You are not authorized to create feedback forms.")
        return redirect('feedback_dashboard')

    users = User.objects.exclude(id=request.user.id)  # Exclude self from assignment list

    if request.method == 'POST':
        title = request.POST.get('title')
        assigned_users_ids = request.POST.getlist('assigned_users')

        question_texts = request.POST.getlist('question_text')
        question_types = request.POST.getlist('question_type')
        question_options_list = request.POST.getlist('question_options')

        if not title or not assigned_users_ids or not question_texts:
            messages.error(request, "Please fill all required fields.")
            return render(request, 'feedback_create_form.html', {'users': users})

        # Create form
        form = FeedbackForm.objects.create(title=title, created_by=request.user)
        form.assigned_users.set(User.objects.filter(id__in=assigned_users_ids))
        form.save()

        # Create questions
        for text, qtype, options in zip(question_texts, question_types, question_options_list):
            if text.strip():
                FeedbackQuestion.objects.create(
                    form=form,
                    text=text.strip(),
                    question_type=qtype,
                    options=options.strip() if options else ''
                )

        messages.success(request, "Feedback form created successfully!")
        return redirect('feedback_dashboard')

    return render(request, 'feedback_create_form.html', {'users': users})

@login_required
def feedback_fill_form(request, form_id):
    form = get_object_or_404(FeedbackForm, id=form_id)

    # Prepare questions with option_list in view
    questions_with_options = []
    for question in form.questions.all():
        option_list = [opt.strip() for opt in question.options.split(',')] if question.options else []
        questions_with_options.append({
            'id': question.id,
            'text': question.text,
            'question_type': question.question_type,
            'option_list': option_list,
        })

    # Check user assignment
    if request.user not in form.assigned_users.all():
        messages.error(request, "You are not assigned to this feedback form.")
        return redirect('feedback_dashboard')

    existing_response = FeedbackResponse.objects.filter(form=form, user=request.user).first()

    if existing_response:
        return render(request, 'feedback_fill_form.html', {
            'form': form,
            'already_submitted': True,
        })

    if request.method == 'POST':
        response = FeedbackResponse.objects.create(form=form, user=request.user)

        for question in form.questions.all():
            field_name = f"question_{question.id}"

            if question.question_type == 'CHECKBOX':
                answers = request.POST.getlist(field_name)
                answer_text = ", ".join(answers) if answers else ''
            else:
                answer_text = request.POST.get(field_name, '').strip()

            FeedbackAnswer.objects.create(
                response=response,
                question=question,
                answer_text=answer_text
            )

        messages.success(request, "Feedback submitted successfully!")
        return redirect('feedback_dashboard')

    return render(request, 'feedback_fill_form.html', {
        'form': form,
        'questions': questions_with_options,
        'already_submitted': False,
    })


@login_required
def view_feedback_responses(request, form_id):
    form = get_object_or_404(FeedbackForm, id=form_id)

    # Only creator (TAD user) can view responses
    if request.user != form.created_by:
        messages.error(request, "You are not authorized to view responses for this form.")
        return redirect('feedback_dashboard')

    responses = FeedbackResponse.objects.filter(form=form).order_by('-submitted_at').prefetch_related('answers', 'user')

    return render(request, 'feedback_view_responses.html', {
        'form': form,
        'responses': responses
    })

# base/views.py
@login_required
def notification_list(request):
    # Fetch all notifications for the logged-in user
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    # ✅ Mark all unread notifications as read
    notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'notifications.html', {'notifications': notifications})

