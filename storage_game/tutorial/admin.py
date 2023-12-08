from django.contrib import admin
from .models import KmbButton, KmbSubmenu, KmbContent

class KmbButtonAdmin(admin.ModelAdmin):
    list_display = ('title',)  # поля, которые будут отображаться в списке
    search_fields = ('title',)  # поля, по которым можно искать

admin.site.register(KmbButton, KmbButtonAdmin)

class KmbSubmenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent_button')
    search_fields = ('title', 'parent_button')
    list_filter = ('parent_button',)  # фильтр для быстрого поиска по родительской кнопке

admin.site.register(KmbSubmenu, KmbSubmenuAdmin)

class KmbContentAdmin(admin.ModelAdmin):
    list_display = ('text', 'image_url', 'video_url', 'submenu_id')
    search_fields = ('text', 'submenu_id',)
    list_filter = ('text', 'submenu_id',)  # фильтр для быстрого поиска по родительской кнопке

admin.site.register(KmbContent, KmbContentAdmin)