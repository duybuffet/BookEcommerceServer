from django.contrib import admin

from .models import *


class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 3


class BookGenreInline(admin.TabularInline):
    model = BookGenre
    extra = 3


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 3


class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookAuthorInline]
    list_display = ['name']
    search_fields = ['name']

class BookAdmin(admin.ModelAdmin):
    inlines = [BookGenreInline, BookAuthorInline]
    list_display = ('id', 'isbn', 'title', 'price', 'discount', 'stock')
    search_fields = ['id', 'isbn', 'title', 'price']

class OrderHistoryAdmin(admin.ModelAdmin):
    inlines = [OrderLineInline]
    list_display = ('id', 'fullname', 'order_date', 'status', 'total')
    search_fields = ['id', 'fullname', 'order_date']
    readonly_fields = ('fullname', 'order_date', 'total')
    list_filter = ['status']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'fullname', 'email', 'phone')
    search_fields = ['id', 'username', 'fullname', 'email', 'phone']
    readonly_fields = ('username', 'fullname', 'email', 'phone', 'city', 'district', 'ward', 'postal_code', 'street_number')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['id', 'name']


# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(OrderHistory, OrderHistoryAdmin)