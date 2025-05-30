from django.db import models
import pandas as pd
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.models import Sum

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quiz_file = models.FileField(upload_to='quiz/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Tests'

    def __str__(self):
        return self.title
    
    # call the function on quize save
    def save(self, *args, **kwargs):
        super().save( *args, **kwargs)
        if self.quiz_file:
            self.import_quiz_from_excel()

    #function to extract excel file
    def import_quiz_from_excel(self):
        #read the excel file
        df = pd.read_excel(self.quiz_file.path)

        

        df.columns = df.columns.str.strip().str.lower()
        # print("Excel columns found:", df.columns.tolist())
        # required_columns = ['question', 'a', 'b', 'c', 'd', 'answer']
        # for col in required_columns:
        #     if col not in df.columns:
        #         raise ValueError(f"Missing column: '{col}' in uploaded Excel file.")




        #iterate over each row
        for index, row in df.iterrows():
            # extract question text, choices and correct answer from row
            question_text = row['question']
            choice1 = row['a']
            choice2 = row['b']
            choice3 = row['c']
            choice4 = row['d']
            correct_answer = row['answer'].strip().upper()

            # create the question object
            question = Question.objects.get_or_create(quiz=self, text=question_text)

            # create choices objects
            choice_1 = Choice.objects.get_or_create(question=question[0], text=choice1, is_correct=correct_answer == 'A')
            choice_2 = Choice.objects.get_or_create(question=question[0], text=choice2, is_correct=correct_answer == 'B')
            choice_3 = Choice.objects.get_or_create(question=question[0], text=choice3, is_correct=correct_answer == 'C')
            choice_4 = Choice.objects.get_or_create(question=question[0], text=choice4, is_correct=correct_answer == 'D')

      
      
    
class Question(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text[:50]
    
class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __self__(self):
        return f"{self.question.text[:50]}, {self.text[:20]}"
    
class QuizSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}, {self.quiz.title}"

    def clean(self):
        if self.quiz:
            total_questions = self.quiz.question_set.count()
            if self.score > total_questions:
                raise ValidationError(f"Score cannot exceed total marks ({total_questions}).")

class UserRank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.IntegerField(null=True, blank=True)
    total_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.rank}, {self.user.username}"

    def clean(self):
        # This ensures admin cannot manually change the rank/score
        if self.pk:  # If this is an update, not a new instance
            original = UserRank.objects.get(pk=self.pk)
            if original.rank != self.rank or original.total_score != self.total_score:
                raise ValidationError("Rank and total score cannot be changed manually.")

@receiver(post_save, sender=QuizSubmission)
def quizsubmission_post_save_handler(sender, instance, created, **kwargs):
    print("Leaderboard update triggered")
    update_leaderboard()
    
def update_leaderboard():
    user_scores = (
        QuizSubmission.objects
        .values('user')
        .annotate(total_score=Sum('score'))
        .order_by('-total_score', 'user__username')
    )

    rank = 0
    prev_score = None

    for i, entry in enumerate(user_scores, start=1):
        user_id = entry['user']
        total_score = entry['total_score']

        if total_score != prev_score:
            rank += 1  # Increase rank only when score changes

        user_rank, _ = UserRank.objects.get_or_create(user_id=user_id)
        user_rank.rank = rank
        user_rank.total_score = total_score
        user_rank.save()

        prev_score = total_score

class QuizAnswer(models.Model):
    submission = models.ForeignKey(QuizSubmission, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)





