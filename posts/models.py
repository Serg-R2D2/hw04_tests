from django.contrib.auth import get_user_model

from django.db import models



User = get_user_model()


class Group(models.Model):
    title = models.CharField('Сообщество', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание')

    class Meta:
        verbose_name_plural = 'Сообщества'
        verbose_name = 'Сообщество'
        ordering = ['title']

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField('Содержание', blank=False, null=True)
    pub_date = models.DateTimeField('Опубликовано', auto_now_add=True)
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='posts', 
        verbose_name='Автор')
    group = models.ForeignKey(
        Group, 
        on_delete=models.SET_NULL, 
        related_name='posts', 
        blank=True, null=True, 
        verbose_name='Сообщество'
        )

    class Meta:
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'
        ordering = ['-pub_date']

    def __str__(self):
       return self.text
