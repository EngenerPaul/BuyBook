from django.urls import reverse
from django.db import models
from django.db.models import CharField, ForeignKey, ManyToManyField, \
                             ImageField, IntegerField, FloatField, \
                             SlugField, TextField



class Author(models.Model):
    full_name = CharField(max_length=70, verbose_name='Имя')
    slug = SlugField(max_length=70, unique=True, verbose_name='Url')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['full_name']
    
    def __str__(self):
        return "The Author class: " + self.full_name
    
    def get_absolute_url(self):
        return reverse('by_authors', kwargs={'slug': self.slug})

class Genre(models.Model):
    title = CharField(max_length=30, verbose_name='Жанр')
    slug = SlugField(max_length=30, unique=True, verbose_name='Url')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['title']
    
    def __str__(self):
        return "The Genre class: " + self.title

    def get_absolute_url(self):
        return reverse('by_genres', kwargs={"slug": self.slug})


class Book(models.Model):
    title = CharField(max_length=150, verbose_name='Название')
    slug = SlugField(max_length=255, unique=True, verbose_name='Url')
    author = ForeignKey(Author, on_delete=models.PROTECT, verbose_name='Автор')
    genre = ManyToManyField(Genre, blank=True, verbose_name='Жанр')
    cover = ImageField(upload_to='covers/', blank=True, verbose_name='Обложка')
    # note = TextField(blank=True, verbose_name='Описание')
    pages = IntegerField(verbose_name='Количество страниц')
    isbn = CharField(max_length=30, blank=True, verbose_name='ISBN')
    published_at = IntegerField(blank=True, verbose_name='Год издания')
    circulation = IntegerField(blank=True, verbose_name='Тираж')
    cover_type = CharField(max_length=20, blank=True, verbose_name='Тип обложки')
    book_format = CharField(max_length=30, blank=True, verbose_name='Формат')  # размер
    weight = FloatField(blank=True, verbose_name='Вес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено на сайт')

    cost = IntegerField(verbose_name='Стоимость')
    discount = IntegerField(default=0, verbose_name='Скидка')  # проценты
    units_in_stock = IntegerField(default=0, verbose_name='Кол-во в наличии')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at', 'title', ]

    def __str__(self):
        return "The Book class: " + self.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    pass