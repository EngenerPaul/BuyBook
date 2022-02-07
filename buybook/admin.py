from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Book, Genre, Author, Comment

class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("title",)}
    save_on_top = True
    list_display = ['id', 'title', 'get_cover', 'author', 'cost', 'discount', 'units_in_stock']

    def get_cover(self, obj):
        if obj.cover:
            return mark_safe(f'<img src="{obj.cover.url}" width=50>')
        return '-'

class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("full_name",)}

admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Author, AuthorAdmin)
