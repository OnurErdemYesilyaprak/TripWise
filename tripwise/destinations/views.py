from django.shortcuts import render, get_object_or_404
from .models import City

def city_detail(request, city_id):
    city = get_object_or_404(City, id=city_id)
    return render(request, 'city_detail.html', {'city': city})

def city_content_detail(request, city_id, content_type):
    city = get_object_or_404(City, id=city_id)

    titles = {
        'place': 'Gezilecek Yerler',
        'food': 'Yenilecek Yemekler',
        'stay': 'Kalınacak Yerler',
        'activity': 'Aktiviteler'
    }

    title = titles.get(content_type, 'İçerik')

    return render(request, 'city_content_detail.html', {
        'city': city,
        'title': title,
        'content_type': content_type
    })