from django.urls import reverse
from django.db import models
from django.db.models import CharField, ForeignKey, ManyToManyField, \
                             ImageField, IntegerField, FloatField, \
                             SlugField, TextField, DateTimeField, \
                             BooleanField, \
                             CASCADE, SET_NULL
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from datetime import datetime, timedelta



class Author(models.Model):
    """List of book authors"""

    full_name = CharField(max_length=70, verbose_name='Имя')
    slug = SlugField(max_length=70, unique=True, verbose_name='Url')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['full_name']
    
    def __str__(self):
        return f"The Author class: {self.full_name}"


class Genre(models.Model):
    """List of book genres"""

    title = CharField(max_length=30, verbose_name='Жанр')
    slug = SlugField(max_length=30, unique=True, verbose_name='Url')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['title']
    
    def __str__(self):
        return f"The Genre class: {self.title}"

    def get_absolute_url(self):
        return reverse('genre_page', kwargs={"slug": self.slug})


class Book(models.Model):
    """List of books (products)"""

    title = CharField(max_length=150, verbose_name='Название')
    slug = SlugField(max_length=255, unique=True, verbose_name='Url')
    author = ForeignKey(Author, on_delete=models.PROTECT, verbose_name='Автор')
    genre = ManyToManyField(Genre, blank=True, verbose_name='Жанр')
    cover = ImageField(upload_to='covers/', blank=True, verbose_name='Обложка')
    note = TextField(blank=True, verbose_name='Описание')
    pages = IntegerField(verbose_name='Количество страниц')
    isbn = CharField(max_length=30, blank=True, verbose_name='ISBN')
    published_at = IntegerField(blank=True, verbose_name='Год издания')
    circulation = IntegerField(blank=True, verbose_name='Тираж')
    cover_type = CharField(max_length=20, blank=True, verbose_name='Тип обложки')
    book_format = CharField(max_length=30, blank=True, verbose_name='Формат')  # размер
    weight = FloatField(blank=True, verbose_name='Вес')
    created_at = DateTimeField(auto_now_add=True, verbose_name='Добавлено на сайт')

    cost = IntegerField(verbose_name='Стоимость')
    discount = IntegerField(default=0, verbose_name='Скидка')  # проценты
    units_in_stock = IntegerField(default=0, verbose_name='Кол-во в наличии')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at', 'title', ]

    def __str__(self):
        return f"The Book class: {self.title}"

    def get_absolute_url(self):
        return reverse('book_detail_page', kwargs={'slug': self.slug})


class Comment(models.Model):
    """List of book commentaries"""

    user = ForeignKey(User, on_delete=CASCADE, 
                      verbose_name='Автор комментария', related_name='comments')
    book = ForeignKey(Book, on_delete=CASCADE, verbose_name='Книга', 
                      related_name='comments')
    text = TextField(max_length=1000, verbose_name='Комментарий')
    estimate = IntegerField(verbose_name='Оценка', 
                            validators=(MinValueValidator(0), MaxValueValidator(5)))
    created_at = DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created_at', )

    def __str__(self):
        return f"The Comment class: {self.user}"


class Basket(models.Model):
    """List of books (products) in shopping basket"""

    book_id = ForeignKey(Book, on_delete=CASCADE, verbose_name='Книга', 
                         related_name='basket_books')
    user_id = ForeignKey(User, on_delete=CASCADE, verbose_name='Пользователь', 
                         related_name='basket_user')
    quantity = IntegerField(default=1, verbose_name='Количество', 
                            validators=(MinValueValidator(0), MaxValueValidator(50)))
    created_at = DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        ordering = ('user_id', 'book_id', )

    def __str__(self):
        return f"The Basket class: id = {self.pk}"


class Marked(models.Model):
    """List of marked books (products)"""

    book_id = ForeignKey(Book, on_delete=CASCADE, verbose_name='Книга', 
                         related_name='marked_books')
    user_id = ForeignKey(User, on_delete=CASCADE, verbose_name='Пользователь', 
                         related_name='marked_user')
    created_at = DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Закладки'
        verbose_name_plural = 'Закладки'
        ordering = ('user_id', 'book_id', )

    def __str__(self):
        return f"The Marked class: id = {self.pk}"


class Order(models.Model):
    """List of orders"""

    user_id = ForeignKey(User, on_delete=SET_NULL, null=True, 
                         verbose_name='Пользователь', related_name='orders_by_user')
    book_id = ManyToManyField(Book, verbose_name='Книги', related_name='orders_by_book')
    address = CharField(max_length=250, blank=True, verbose_name='Адрес')  
    # address blank=True because it's pet-project
    postcode = CharField(max_length=20, blank=True, verbose_name='Почтовый индекс')  
    # postcode blank=True - same way
    created_at = DateTimeField(auto_now_add=True, verbose_name='Дата оформления заказа')
    date_of_receipt = DateTimeField(default=datetime.now()+timedelta(days=14), 
                                    verbose_name='Дата получения заказа')
    activity = BooleanField(default=True, verbose_name='Заказ активен?')
    was_received = BooleanField(default=False, verbose_name='Заказ доставлен?')
    total_cost = IntegerField(verbose_name='Общая стоимость', 
                              validators=(MinValueValidator(0), MaxValueValidator(100_000)))

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created_at', )

    def __str__(self):
        return f"The Order class: id = {self.pk}"

class OrderDetails(models.Model):
    """List of details (books quantities) about orders"""

    order_id = ForeignKey(Order, on_delete=CASCADE, verbose_name='Заказ', 
                          related_name='books')
    book_id = ForeignKey(Book, on_delete=SET_NULL, null=True, verbose_name='Книга', 
                         related_name='orders')
    quantity = IntegerField(default=1, verbose_name='Количество', 
                            validators=(MinValueValidator(0), MaxValueValidator(50)))
    cost = IntegerField(verbose_name='Стоимость')

    class Meta:
        verbose_name = 'Детали заказов'
        verbose_name_plural = 'Детали заказов'
        ordering = ('-order_id', 'book_id', )

    def __str__(self):
        return f"The OrderDetails class: id = {self.pk}"
