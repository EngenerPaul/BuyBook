from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Book, Genre, Author, Comment, Basket, Marked, Order, OrderDetails

class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("title", ), }  # automatical creation slug using title
    save_on_top = True  # button save on top of the page
    list_display = ('id', 'title', 'get_cover', 'author', 
                    'cost', 'discount', 'units_in_stock', )  # title of the columns in common list
    list_display_links = ('id', 'title', 'get_cover', )  # create links on the column
    search_fields = ('title', )  # create searche field on the top

    def get_cover(self, obj):
        if obj.cover:
            return mark_safe(f'<img src="{obj.cover.url}" width=50>')
        return '-'


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', )


class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("full_name",)}
    list_display = ('full_name', )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'estimate', )
    readonly_fields = ('text', 'estimate', )


class BasketAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'user_id', 'quantity', )


class MarkedAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'user_id', )


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'activity', 'was_received', 'total_cost', )


class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'book_id', 'quantity', 'cost', )


admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(Marked, MarkedAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetails, OrderDetailsAdmin)
