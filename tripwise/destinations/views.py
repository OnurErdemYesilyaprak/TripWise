from django.shortcuts import render, get_object_or_404
from .models import City, Place, PlacePhoto, Food, Stay

def city_detail(request, slug):
    city = City.objects.get(slug=slug)
    places = Place.objects.filter(city=city).prefetch_related('photos')
    return render(request, 'city_detail.html', {
        'city': city,
        'places': places
    })

def city_content_detail(request, slug, content_type):
    city = get_object_or_404(City, slug=slug)

    titles = {
        'place': 'Gezilecek Yerler',
        'food': 'Yenilecek Yemekler',
        'stay': 'Kalınacak Yerler',
        'activity': 'Aktiviteler'
    }

    title = titles.get(content_type, 'İçerik')
    
    # Get the appropriate data based on content_type
    if content_type == 'place':
        content_data = Place.objects.filter(city=city).prefetch_related('photos')
        template_name = 'city_places.html'
    elif content_type == 'food':
        content_data = Food.objects.filter(city=city)
        template_name = 'city_foods.html'
    elif content_type == 'stay':
        content_data = Stay.objects.filter(city=city)
        template_name = 'city_stays.html'
    else:
        content_data = []
        template_name = 'city_content_detail.html'  # fallback

    return render(request, template_name, {
        'city': city,
        'title': title,
        'content_type': content_type,
        'places': content_data if content_type == 'place' else [],
        'foods': content_data if content_type == 'food' else [],
        'stays': content_data if content_type == 'stay' else []
    })