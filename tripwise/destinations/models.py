from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities')
    slug = models.SlugField(blank=True,null=True)
    is_featured = models.BooleanField(default=False)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name


class Place(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='places')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.city.name}"

 

class PlacePhoto(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='photos')
    photo_url = models.URLField(max_length=500)
    

    def __str__(self):
        return f"Photo for {self.place.name}"

class Food(models.Model):
    city = models.ForeignKey(City, related_name='foods', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    place_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    rating = models.FloatField(default=0)
    price_level = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    categories = models.JSONField(default=list, blank=True)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Stay(models.Model):
    city = models.ForeignKey(City, related_name='stays', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    place_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    rating = models.FloatField(default=0)
    price_level = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    types = models.JSONField(default=list, blank=True)
    
    
    def __str__(self):
        return self.name



