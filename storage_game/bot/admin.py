from django.contrib import admin
from .models import AssistantButton, Submenu

class AssistantButtonAdmin(admin.ModelAdmin):
    list_display = ('title', 'response_text', 'image_url')  # поля, которые будут отображаться в списке
    search_fields = ('title',)  # поля, по которым можно искать

admin.site.register(AssistantButton, AssistantButtonAdmin)

class SubmenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'response_text', 'image_url', 'parent_button')
    search_fields = ('title',)
    list_filter = ('parent_button',)  # фильтр для быстрого поиска по родительской кнопке

admin.site.register(Submenu, SubmenuAdmin)
