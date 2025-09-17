from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title', 'thumbnail', 'watched', 'is_published', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    list_editable = ['is_published']
    readonly_fields = ['watched', 'photo_preview']  # поле с превью
    list_filter = ['category', 'is_published']

    def thumbnail(self, obj):
        """Миниатюра в списке постов"""
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="50" style="object-fit: cover; border-radius: 3px;" />')
        return 'Нет фото'
    thumbnail.short_description = 'Фото'

    def photo_preview(self, obj):
        """Миниатюра над полем photo в редакторе поста"""
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="150" height="150" style="object-fit: cover; border-radius: 5px; margin-bottom: 10px;" />')
        return 'Нет фото'
    photo_preview.short_description = 'Текущее изображение'


admin.site.register(Category)
admin.site.register(Post, PostAdmin)