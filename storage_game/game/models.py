from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class QuestionStorageGame(models.Model):
    question_text = models.TextField()
    answer1 = models.CharField(max_length=255)
    answer2 = models.CharField(max_length=255)
    answer3 = models.CharField(max_length=255)
    answer4 = models.CharField(max_length=255)
    image_for_question = models.CharField(max_length=255, blank=True, null=True)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

    class Meta:
        db_table = 'questions_storage'


class AnswerStorageGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionStorageGame, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    right_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.question.question_text}"

    class Meta:
        db_table = 'answers_storage'


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Division(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    last_question_id = models.IntegerField(default=0)
    last_question_id_kmb = models.IntegerField(default=0)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'user_profiles'



@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, last_question_id=0, last_question_id_kmb=0)
    else:
        instance.profile.save()



#Для тренировки модели
class QuestionTraining(models.Model):
    question_text = models.CharField(max_length=255)
    answer_1 = models.CharField(max_length=100)
    answer_2 = models.CharField(max_length=100)
    answer_3 = models.CharField(max_length=100)
    answer_4 = models.CharField(max_length=100)
    image_for_question = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.question_text

class AnswerTraining(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionTraining, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=100)
    is_correct = models.BooleanField()
    correct_sequence = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.question.question_text}"


#Курс молодого бойца вопросы и ответы

class KmbQuestionStorage(models.Model):
    question_text = models.TextField()
    answer1 = models.CharField(max_length=255)
    answer2 = models.CharField(max_length=255)
    answer3 = models.CharField(max_length=255)
    answer4 = models.CharField(max_length=255)
    image_for_question = models.CharField(max_length=255, blank=True, null=True)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

    class Meta:
        db_table = 'kmb_questions_storage'


class KmbAnswerStorage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(KmbQuestionStorage, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    right_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.question.question_text}"

    class Meta:
        db_table = 'kmb_answers_storage'

#Управление доступом к результатам

class UserResultsAccess(models.Model):
    is_access_enabled = models.BooleanField(default=False)

class UserResultsKmbAccess(models.Model):
    is_access_enabled = models.BooleanField(default=False)