from django.urls import path
from . import views

urlpatterns = [
    path('city/<slug:slug>/', views.city_detail, name='city_detail'),
    path('city/<slug:slug>/<str:content_type>/', views.city_content_detail, name='city_content_detail'),
]
