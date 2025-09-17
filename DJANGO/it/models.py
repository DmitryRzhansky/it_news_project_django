from django.db import models
from django.utils.text import slugify  # для генерации человеко-понятного URL

class Category(models.Model):
    """Категория новостей"""
    title = models.CharField(max_length=255, verbose_name='Название категории')

    def __str__(self):
        # Удобно для админки: при выводе объекта Category будет показываться его название
        return self.title
    
    class Meta():
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    """Новостные посты"""
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(default='Пока ничего нет, но вы держитесь!', verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    # Дата и время создания, автоматически при первом сохранении объекта
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    # Дата и время последнего обновления, автоматически при каждом сохранении объекта
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Изображение')
    # Счётчик просмотров поста
    watched = models.IntegerField(default=0, verbose_name='Количество просмотров')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    # Поле для человеко-понятного URL (slug)
    # unique=True — чтобы slug был уникальным в базе
    # blank=True и null=True позволяют создавать объект без явного slug, он сгенерируется автоматически
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name='ЧПУ (slug)')

    def save(self, *args, **kwargs):
        """
        Переопределяем метод save, чтобы автоматически создавать slug из title.

        Алгоритм:
        1) Если slug пустой, генерируем его из title с помощью slugify.
        2) Проверяем, есть ли уже такой slug в базе.
        3) Если есть — добавляем суффикс -1, -2 и т.д. до уникальности.
        4) Вызываем super().save() для сохранения объекта.
        """
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            counter = 1
            # Проверяем уникальность slug
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        # Удобно для админки и shell: при выводе объекта Post показываем его заголовок
        return self.title
    
    class Meta():
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
