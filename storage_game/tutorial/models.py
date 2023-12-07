from django.db import models

class KmbButton(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название кнопки")
    response_text = models.TextField(verbose_name="Текст ответа")
    image_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на изображение")
    video_url = models.URLField(blank=True)

    def __str__(self):
        return self.title

class KmbSubmenu(models.Model):
    parent_button = models.ForeignKey(KmbButton, on_delete=models.CASCADE, related_name='submenus')
    title = models.CharField(max_length=200, verbose_name="Название пункта подменю")
    response_text = models.TextField(verbose_name="Текст ответа для подменю")
    image_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на изображение для подменю")
    video_url = models.URLField(blank=True)

    def __str__(self):
        return self.title

class KmbContent(models.Model):
    submenu = models.ForeignKey(KmbSubmenu, on_delete=models.CASCADE, related_name='content')
    text = models.TextField(verbose_name="Текст контента")
    image_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на изображение")
    video_url = models.URLField(blank=True, null=True, verbose_name="Ссылка на видео")

    def __str__(self):
        return f'Контент для {self.submenu.title}'
