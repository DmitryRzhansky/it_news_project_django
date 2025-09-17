from django.shortcuts import render
from .models import Category, Post

def index(request):
    """Главная страница"""
    posts = Post.objects.all()
    categories = Category.objects.all()  # Получаем все категории
    context = {
        'title': 'Главная страница',
        'posts': posts,
        'categories': categories,  # Передаем категории отдельно
    }
    return render(request, 'it/index.html', context)
