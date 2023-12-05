from django.contrib import admin
from .models import QuestionStorageGame, AnswerStorageGame, UserProfile, Position

admin.site.register(QuestionStorageGame)
admin.site.register(Position)

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
    list_display = ('user', 'full_name', 'city', 'position', 'last_question_id')
    list_filter = ('position',)
    search_fields = ('full_name', 'city')
    fields = ('user', 'full_name', 'city', 'position', 'last_question_id')
    actions = ['set_last_question_id_to_zero']

    def set_last_question_id_to_zero(self, request, queryset):
        queryset.update(last_question_id=0)
    set_last_question_id_to_zero.short_description = "Установить last_question_id в 0 для выбранных пользователей"