from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('city/<slug:city_slug>/places/', views.city_places, name='city_places'),
    path('city/<slug:city_slug>/foods/', views.city_foods, name='city_foods'),
    path('city/<slug:city_slug>/stays/', views.city_stays, name='city_stays'),
    path('about/', views.about, name='about'),
]
