from django.shortcuts import render
from destinations.models import Region, City, PlacePhoto, Place, Food, Stay
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models import Prefetch

def home(request):
    search_query = request.GET.get('search', '')
    region_filter = request.GET.get('region', '')

    cities = City.objects.all()

    if search_query:
        cities = cities.filter(name__icontains=search_query)
    if region_filter:
        cities = cities.filter(region__name__icontains=region_filter)

    featured_cities = cities.filter(is_featured=True)

    regions = Region.objects.all()

    for city in cities:
        first_photo = PlacePhoto.objects.filter(place__city=city).first()
        if first_photo:
            city.photo_url = first_photo.photo_url
        else:
            city.photo_url = None

    for city in featured_cities:
        first_photo = PlacePhoto.objects.filter(place__city=city).first()
        if first_photo:
            city.photo_url = first_photo.photo_url
        else:
            city.photo_url = None

    return render(request, 'home.html', {
        'cities': cities,
        'featured_cities': featured_cities,
        'regions': regions
    })

def city_places(request, city_slug):
    city = get_object_or_404(City, slug=city_slug)
    places = Place.objects.filter(city=city)
    
    for place in places:
        first_photo = PlacePhoto.objects.filter(place=place).first()
        if first_photo:
            place.photo_url = first_photo.photo_url
        else:
            place.photo_url = None
    
    return render(request, 'city_places.html', {
        'city': city,
        'places': places
    })


def city_foods(request, city_slug):
    city = get_object_or_404(City, slug=city_slug)
    foods = Food.objects.filter(city=city).order_by('-rating')
    return render(request, 'city_foods.html', {
        'city': city,
        'foods': foods
    })

def city_stays(request, city_slug):
    city = get_object_or_404(City, slug=city_slug)
    stays = Stay.objects.filter(city=city).order_by('-rating')
    return render(request, 'city_stays.html', {
        'city': city,
        'stays': stays
    })

def about(request):
    return render(request, 'about.html')
