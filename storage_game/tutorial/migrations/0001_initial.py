# Generated by Django 5.0 on 2023-12-07 05:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KmbButton',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название кнопки')),
                ('response_text', models.TextField(verbose_name='Текст ответа')),
                ('image_url', models.URLField(blank=True, null=True, verbose_name='Ссылка на изображение')),
                ('video_url', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='KmbSubmenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название пункта подменю')),
                ('response_text', models.TextField(verbose_name='Текст ответа для подменю')),
                ('image_url', models.URLField(blank=True, null=True, verbose_name='Ссылка на изображение для подменю')),
                ('video_url', models.URLField(blank=True)),
                ('parent_button', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submenus', to='tutorial.kmbbutton')),
            ],
        ),
    ]