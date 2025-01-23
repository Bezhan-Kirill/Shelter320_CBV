from django.contrib import admin

from dogs.models import Dog, Category


@admin.register(Category)  # регистрация модели панели админа
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    ordering = ('pk', 'name')


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin): # регистрация модели панели админа
    list_display = ('name', 'category')
    list_filter = ('category',)
    ordering = ('name',)
