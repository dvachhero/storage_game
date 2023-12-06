from django.db import models

class AssistantButton(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название кнопки")
    response_text = models.TextField(verbose_name="Текст ответа")
    image_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на изображение")

    def __str__(self):
        return self.title

class Submenu(models.Model):
    parent_button = models.ForeignKey(AssistantButton, on_delete=models.CASCADE, related_name='submenus')
    title = models.CharField(max_length=200, verbose_name="Название пункта подменю")
    response_text = models.TextField(verbose_name="Текст ответа для подменю")
    image_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на изображение для подменю")

    def __str__(self):
        return self.title