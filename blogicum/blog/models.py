from django.db import models

from users.models import MyUser


class PublishedModel(models.Model):
    is_published = models.BooleanField('Опубликовано',
                                       default=True,
                                       help_text='Снимите галочку, '
                                                 'чтобы скрыть публикацию.')
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True


class Category(PublishedModel):
    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField('Идентификатор',
                            unique=True,
                            help_text='Идентификатор страницы для URL; '
                                      'разрешены символы латиницы, '
                                      'цифры, дефис '
                                      'и подчёркивание.')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField('Название места', max_length=256)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishedModel):
    title = models.CharField('Заголовок', max_length=256)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата и время публикации',
                                    help_text='Если установить дату и '
                                              'время в будущем — можно делать '
                                              'отложенные публикации.')
    author = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        null=True,
    )
    location = models.ForeignKey(Location,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 verbose_name='Местоположение',)
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Категория',)

    image = models.ImageField('Фото', upload_to='posts_images', blank=True)

    class Meta:
        default_related_name = 'posts'
        ordering = ('-pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField('Текст поздравления')
    post = models.ForeignKey(Post,
                             related_name='comments',
                             on_delete=models.CASCADE,
                             )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'коментарий'
        verbose_name_plural = 'Коментарии'

    def __str__(self):
        return self.author
