from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Psychotherapist


def methods_normalization(data) -> list:
    """Для корректного отображения списка методов."""
    data = data.replace('{', '').replace('}', '')
    clean_data = data.split(',')
    return clean_data


def main(request):
    """Главная страница."""
    all_psychotherapists = Psychotherapist.objects.all()
    return render(request, 'main/main_page.html', {'all_psychotherapists': all_psychotherapists})


def detail(request, psychotherapist_id):
    """Страница психотерапевта."""
    psychotherapist = get_object_or_404(Psychotherapist, id=psychotherapist_id)
    methods = methods_normalization(psychotherapist.methods)
    return render(request, 'main/page_detail.html', {'psychotherapist': psychotherapist, 'methods': methods})
