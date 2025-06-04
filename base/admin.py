from django.contrib import admin
from .models import Message, Blog, Notice, Resource
from .models import FeedbackForm, FeedbackQuestion, FeedbackResponse, FeedbackAnswer
from .models import Blog, Like, Comment
# Mixin to restrict admin access to superusers in 'TAD' group only
class TadGroupAdminMixin:
    def has_module_permission(self, request):
        return request.user.is_superuser and request.user.groups.filter(name='TAD').exists()

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser and request.user.groups.filter(name='TAD').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.user.groups.filter(name='TAD').exists()

    def has_add_permission(self, request):
        return request.user.is_superuser and request.user.groups.filter(name='TAD').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser and request.user.groups.filter(name='TAD').exists()

# Register models without restriction
admin.site.register(Message)
admin.site.register(Blog)
admin.site.register(Notice)

admin.site.register(Like)
admin.site.register(Comment)

# Register feedback models with restricted access
@admin.register(FeedbackForm)
class FeedbackFormAdmin(TadGroupAdminMixin, admin.ModelAdmin):
    pass

@admin.register(FeedbackQuestion)
class FeedbackQuestionAdmin(TadGroupAdminMixin, admin.ModelAdmin):
    pass

@admin.register(FeedbackResponse)
class FeedbackResponseAdmin(TadGroupAdminMixin, admin.ModelAdmin):
    pass

@admin.register(FeedbackAnswer)
class FeedbackAnswerAdmin(TadGroupAdminMixin, admin.ModelAdmin):
    pass

# admin.py

from django.contrib import admin
from .models import Resource

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'uploaded_by', 'uploaded_at')





