from django.urls import path
from . import views

urlpatterns = [
    path('city/<int:city_id>/', views.city_detail, name='city_detail'),
    path('city/<int:city_id>/<str:content_type>/', views.city_content_detail, name='city_content_detail'),
]
