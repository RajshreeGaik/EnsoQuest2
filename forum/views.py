# forum/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Comment, Like
from .forms import QuestionForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

def question_list(request):
    questions = Question.objects.all().order_by('-created_at')
    
    return render(request, 'question_list.html', {'questions': questions})

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    comments = question.comments.all()
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.question = question
            new_comment.save()
            return redirect('forum:question_detail', pk=pk)
    else:
        comment_form = CommentForm()

    return render(request, 'question_detail.html', {
        'question': question,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('forum:question_list')
    else:
        form = QuestionForm()
    return render(request, 'question_form.html', {'form': form})

@login_required
def like_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    Like.objects.get_or_create(user=request.user, question=question)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    Like.objects.get_or_create(user=request.user, comment=comment)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk, user=request.user)
    if request.method == "POST":
        question.delete()
        return redirect('forum:question_list')
    return render(request, 'forum/confirm_delete.html', {
        'object': question,
        'type': 'question'
    })

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    question_pk = comment.question.pk
    if request.method == "POST":
        comment.delete()
        return redirect('forum:question_detail', pk=question_pk)
    return render(request, 'forum/confirm_delete.html', {
        'object': comment,
        'type': 'comment'
    })

@login_required
def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk, user=request.user)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('forum:question_detail', pk=question.pk)
    else:
        form = QuestionForm(instance=question)
    
    context = {
        'form': form,
        'title': 'Edit Question',
        'heading': 'Edit Your Question',
        'back_url': reverse('forum:question_list'),
    }
    return render(request, 'edit_form.html', context)

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('forum:question_detail', pk=comment.question.pk)
    else:
        form = CommentForm(instance=comment)
    
    context = {
        'form': form,
        'title': 'Edit Comment',
        'heading': 'Edit Your Comment',
        'back_url': reverse('forum:question_detail', kwargs={'pk': comment.question.pk}),
    }
    return render(request, 'edit_form.html', context)




# Create your views here.
