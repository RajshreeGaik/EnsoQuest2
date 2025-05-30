# forum/admin.py

from django.contrib import admin
from .models import Question, Comment, Like

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'created_at')
    search_fields = ('content',)
    list_filter = ('created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'comment')
    list_filter = ('question', 'comment')


# Register your models here.
