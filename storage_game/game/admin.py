from django.contrib import admin
from .models import QuestionStorageGame, AnswerStorageGame, UserProfile, Position, AnswerTraining, QuestionTraining, KmbAnswerStorage, KmbQuestionStorage

admin.site.register(QuestionStorageGame)
admin.site.register(Position)

class QuestionTrainingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in QuestionTraining._meta.fields]
    list_filter = [field.name for field in QuestionTraining._meta.fields if field.name != 'image_for_question']  # исключаем поле изображения

admin.site.register(QuestionTraining, QuestionTrainingAdmin)

class AnswerTrainingAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AnswerTraining._meta.fields]
    list_filter = [field.name for field in AnswerTraining._meta.fields]

admin.site.register(AnswerTraining, AnswerTrainingAdmin)

@admin.register(AnswerStorageGame)
class AnswerStorageGameAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'right_answer')
    list_filter = ('user', 'question', 'right_answer')
    search_fields = ('user__username', 'question__question_text')
    actions = ['clear_answers']

    def clear_answers(self, request, queryset):
        queryset.delete()
    clear_answers.short_description = "Очистить таблицу с ответами пользователей"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'city', 'position', 'last_question_id', 'last_question_id_kmb')
    list_filter = ('position',)
    search_fields = ('full_name', 'city')
    fields = ('user', 'full_name', 'city', 'position', 'last_question_id', 'last_question_id_kmb')
    actions = ['set_last_question_id_to_zero']

    def set_last_question_id_to_zero(self, request, queryset):
        queryset.update(last_question_id=0)
    set_last_question_id_to_zero.short_description = "Установить last_question_id в 0 для выбранных пользователей"

class KmbQuestionStorageAdmin(admin.ModelAdmin):
        list_display = ('question_text', 'correct_answer')
        search_fields = ('question_text',)

admin.site.register(KmbQuestionStorage, KmbQuestionStorageAdmin)

class KmbAnswerStorageAdmin(admin.ModelAdmin):
        list_display = ('user', 'question', 'answer', 'right_answer')
        search_fields = ('user__username', 'question__question_text')

admin.site.register(KmbAnswerStorage, KmbAnswerStorageAdmin)