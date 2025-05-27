from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Category, Quiz, Question, Choice, QuizSubmission, UserRank

# QuizSubmission Form
class QuizSubmissionForm(ModelForm):
    class Meta:
        model = QuizSubmission
        fields = "__all__"

class QuizSubmissionAdmin(admin.ModelAdmin):
    form = QuizSubmissionForm

# UserRank Form
class UserRankForm(ModelForm):
    class Meta:
        model = UserRank
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        self.instance.rank = cleaned_data.get("rank")
        self.instance.total_score = cleaned_data.get("total_score")
        self.instance.clean()
        return cleaned_data

class UserRankAdmin(admin.ModelAdmin):
    form = UserRankForm
    readonly_fields = ['rank', 'total_score']

# Registering everything
admin.site.register(Category)
admin.site.register(Quiz)
admin.site.register(Question)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
admin.site.register(Choice, ChoiceAdmin)

admin.site.register(QuizSubmission, QuizSubmissionAdmin)
admin.site.register(UserRank, UserRankAdmin)
