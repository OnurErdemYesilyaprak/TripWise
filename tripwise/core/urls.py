from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('city/<slug:city_slug>/places/', views.city_places, name='city_places'),
    path('city/<slug:city_slug>/foods/', views.city_foods, name='city_foods'),
    path('city/<slug:city_slug>/stays/', views.city_stays, name='city_stays'),
    path('city/<int:city_id>/fetch-places/', views.fetch_places_view, name='fetch_places'),
    path('city/<int:city_id>/fetch-foods/', views.fetch_foods_view, name='fetch_foods'),
    path('city/<int:city_id>/fetch-stays/', views.fetch_stays_view, name='fetch_stays'),
    path('about/', views.about, name='about'),
]
