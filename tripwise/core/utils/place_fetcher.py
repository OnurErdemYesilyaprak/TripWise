import requests
from django.conf import settings
from destinations.models import Place, PlacePhoto, Food, City, Stay
from urllib.parse import quote
import time
from django.http import JsonResponse
import re


def fetch_places_for_city(city_name, city_object):
    """
    Google Places API'den şehir için gezilecek yerleri çeker ve veritabanına kaydeder.
    """
    try:
        # Şehirdeki gezilecek yerleri çek
        search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        search_params = {
            "query": f"tourist attractions in {city_name}, Turkey",
            "key": settings.GOOGLE_PLACES_API_KEY,
            "type": "tourist_attraction"
        }
        
        print(f"\n{city_name} için turistik yerler aranıyor...")
        
        search_response = requests.get(search_url, params=search_params)
        if search_response.status_code != 200:
            print(f"Arama API hatası: {search_response.text}")
            return False
            
        search_data = search_response.json()
        if not search_data.get("results"):
            print(f"{city_name} için sonuç bulunamadı.")
            return False
        
        saved_places = 0
        skipped_places = 0
        
        for place in search_data.get("results", []):
            # Eğer bu yer zaten kayıtlıysa atla
            if Place.objects.filter(name=place["name"], city=city_object).exists():
                skipped_places += 1
                continue
                
            # Detaylı bilgileri al
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                "place_id": place["place_id"],
                "key": settings.GOOGLE_PLACES_API_KEY,
                "fields": "name,formatted_address,photos,editorial_summary"
            }
            
            details_response = requests.get(details_url, params=details_params)
            if details_response.status_code != 200:
                continue
                
            details = details_response.json().get("result", {})
            
            # Fotoğraf kontrolü
            if not details.get("photos"):
                skipped_places += 1
                continue
            
            # Yeni Place nesnesi oluştur
            place_obj = Place(
                city=city_object,
                name=details.get('name', ''),
                description=details.get('editorial_summary', {}).get('overview', ''),
                address=details.get('formatted_address', '')
            )
            place_obj.save()
            
            # Fotoğrafları kaydet (en fazla 5 fotoğraf)
            for photo in details.get('photos', [])[:5]:
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={photo['photo_reference']}&key={settings.GOOGLE_PLACES_API_KEY}"
                PlacePhoto.objects.create(
                    place=place_obj,
                    photo_url=photo_url
                )
            
            saved_places += 1
            
            # API rate limit'ini aşmamak için bekle
            time.sleep(0.5)
            
        print(f"\n{city_name} için işlem tamamlandı:")
        print(f"- Kaydedilen yer sayısı: {saved_places}")
        print(f"- Atlanan yer sayısı: {skipped_places}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Google Places API hatası: {e}")
        return False
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")
        return False

def fetch_foods_for_city(city_name, city):
    """
    Google Places API'den şehir için yemek mekanlarını çeker ve veritabanına kaydeder.
    """
    
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"restaurants in {city_name}, Turkey",
        "key": settings.GOOGLE_PLACES_API_KEY,
        "language": "tr"
    }

    try:
        # API isteği
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        
        for place in data.get("results", []):
            # Eğer bu işletme zaten kayıtlıysa atla
            if Food.objects.filter(place_id=place["place_id"]).exists():
                continue

           
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                "place_id": place["place_id"],
                "key": settings.GOOGLE_PLACES_API_KEY,
                "language": "tr",
                "fields": "name,formatted_address,formatted_phone_number,website,rating,price_level,photos,reviews"
            }
            
            details_response = requests.get(details_url, params=details_params)
            details_response.raise_for_status()
            details = details_response.json().get("result", {})

            
            food = Food(
                city=city,
                name=place["name"],
                description=details.get("editorial_summary", {}).get("overview", ""),
                image_url=f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={details['photos'][0]['photo_reference']}&key={settings.GOOGLE_PLACES_API_KEY}" if "photos" in details else None,
                place_id=place["place_id"],
                rating=details.get("rating", 0),
                price_level=details.get("price_level", ""),
                address=details.get("formatted_address", ""),
                phone=details.get("formatted_phone_number", ""),
                website=details.get("website", ""),
                categories=[place.get("types", [])]
            )
            food.save()

            
            time.sleep(0.5)

        return True

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Google Places API: {e}")
        return False

def fetch_stays_for_city(city_name, city):
    """
    Google Places API'den şehir için konaklama yerlerini çeker ve veritabanına kaydeder.
    """
    # API endpoint ve parametreler
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"hotels in {city_name}, Turkey",
        "key": settings.GOOGLE_PLACES_API_KEY,
        "language": "tr"
    }

    try:
        # API isteği
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Her bir işletme için
        for place in data.get("results", []):
            # Eğer bu işletme zaten kayıtlıysa atla
            if Stay.objects.filter(place_id=place["place_id"]).exists():
                continue

            # Detaylı bilgileri al
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                "place_id": place["place_id"],
                "key": settings.GOOGLE_PLACES_API_KEY,
                "language": "tr",
                "fields": "name,formatted_address,formatted_phone_number,website,rating,price_level,photos,reviews,types"
            }
            
            details_response = requests.get(details_url, params=details_params)
            details_response.raise_for_status()
            details = details_response.json().get("result", {})

            # Yeni Stay nesnesi oluştur
            stay = Stay(
                city=city,
                name=place["name"],
                description=details.get("editorial_summary", {}).get("overview", ""),
                image_url=f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={details['photos'][0]['photo_reference']}&key={settings.GOOGLE_PLACES_API_KEY}" if "photos" in details else None,
                place_id=place["place_id"],
                rating=details.get("rating", 0),
                price_level=details.get("price_level", ""),
                address=details.get("formatted_address", ""),
                phone=details.get("formatted_phone_number", ""),
                website=details.get("website", ""),
                types=[place.get("types", [])]
            )
            stay.save()

            # API rate limit'ini aşmamak için bekle
            time.sleep(0.5)

        return True

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Google Places API: {e}")
        return False

