import requests
from django.conf import settings
from destinations.models import Place, PlacePhoto, Food, City, Stay
from urllib.parse import quote
import time
from django.http import JsonResponse


def fetch_places_for_city(city_name, city_object):
    """
    OpenTripMap API'den şehir için gezilecek yerleri çeker ve veritabanına kaydeder.
    Sadece fotoğraf veya açıklama bilgisi olan yerler kaydedilir.
    """
    try:
        # Şehir adını İngilizce'ye çevir
        city_name_mapping = {
            "İstanbul": "Istanbul",
            "İzmir": "Izmir",
            "Mersin": "Mersin",
            "Ankara": "Ankara",
            "Antalya": "Antalya",
            "Bursa": "Bursa",
            "Adana": "Adana",
            "Gaziantep": "Gaziantep",
            "Konya": "Konya",
            "Diyarbakır": "Diyarbakir",
            "Eskişehir": "Eskisehir",
            "Şanlıurfa": "Sanliurfa",
            "Samsun": "Samsun",
            "Denizli": "Denizli",
            "Kahramanmaraş": "Kahramanmaras",
            "Van": "Van",
            "Malatya": "Malatya",
            "Erzurum": "Erzurum",
            "Batman": "Batman",
            "Elazığ": "Elazig",
            "Sivas": "Sivas",
            "Giresun": "Giresun",
            "Trabzon": "Trabzon",
            "Kayseri": "Kayseri",
            "Manisa": "Manisa",
            "Aydın": "Aydin",
            "Muğla": "Mugla",
            "Tekirdağ": "Tekirdag",
            "Balıkesir": "Balikesir",
            "Kocaeli": "Kocaeli",
            "Sakarya": "Sakarya",
            "Edirne": "Edirne",
            "Çanakkale": "Canakkale",
            "Hatay": "Hatay",
            "Osmaniye": "Osmaniye",
            "Burdur": "Burdur",
            "Isparta": "Isparta",
            "Afyonkarahisar": "Afyonkarahisar",
            "Uşak": "Usak",
            "Kütahya": "Kutahya",
            "Rize": "Rize",
            "Artvin": "Artvin",
            "Ordu": "Ordu",
            "Sinop": "Sinop",
            "Kastamonu": "Kastamonu",
            "Zonguldak": "Zonguldak",
            "Bartın": "Bartin",
            "Karabük": "Karabuk",
            "Bolu": "Bolu",
            "Düzce": "Duzce",
            "Bayburt": "Bayburt",
            "Gümüşhane": "Gumushane",
            "Erzincan": "Erzincan",
            "Kars": "Kars",
            "Ağrı": "Agri",
            "Iğdır": "Igdir",
            "Ardahan": "Ardahan",
            "Bitlis": "Bitlis",
            "Muş": "Mus",
            "Bingöl": "Bingol",
            "Tunceli": "Tunceli",
            "Elazığ": "Elazig",
            "Malatya": "Malatya",
            "Diyarbakır": "Diyarbakir",
            "Şanlıurfa": "Sanliurfa",
            "Gaziantep": "Gaziantep",
            "Mardin": "Mardin",
            "Batman": "Batman",
            "Siirt": "Siirt",
            "Şırnak": "Sirnak",
            "Adıyaman": "Adiyaman",
            "Kilis": "Kilis"
        }
        
        english_city_name = city_name_mapping.get(city_name, city_name)
        
        # Şehirdeki gezilecek yerleri çek
        search_url = "https://api.opentripmap.com/0.1/en/places/radius"
        search_params = {
            "radius": 5000,  # 5km yarıçap
            "limit": 50,
            "apikey": settings.OPENTRIPMAP_API_KEY,
            "format": "json"
        }
        
        # Önce şehrin koordinatlarını al
        geocode_url = "https://api.opentripmap.com/0.1/en/places/geoname"
        geocode_params = {
            "name": english_city_name,
            "country": "TR",
            "apikey": settings.OPENTRIPMAP_API_KEY
        }
        
        print(f"\nGeocode API İsteği:")
        print(f"URL: {geocode_url}")
        print(f"Parametreler: {geocode_params}")
        
        geocode_response = requests.get(geocode_url, params=geocode_params)
        print(f"\nGeocode API Yanıt Kodu: {geocode_response.status_code}")
        
        if geocode_response.status_code != 200:
            print(f"Geocode API Yanıtı: {geocode_response.text}")
            return False
            
        geocode_data = geocode_response.json()
        lat = geocode_data.get('lat')
        lon = geocode_data.get('lon')
        
        if not lat or not lon:
            print(f"Şehir koordinatları bulunamadı: {english_city_name}")
            return False
            
        search_params['lon'] = lon
        search_params['lat'] = lat
        
        print(f"\nArama API İsteği:")
        print(f"URL: {search_url}")
        print(f"Parametreler: {search_params}")
        
        time.sleep(1)  # Rate limit için bekle
        
        search_response = requests.get(search_url, params=search_params)
        print(f"\nArama API Yanıt Kodu: {search_response.status_code}")
        
        if search_response.status_code != 200:
            print(f"Arama API Yanıtı: {search_response.text}")
            return False
            
        search_data = search_response.json()
        print(f"\nArama API Yanıtı: {search_data}")
        
        if not search_data:
            print(f"Sonuç bulunamadı.")
            return False
        
        saved_places = 0
        skipped_places = 0
        
        for place in search_data:
            print(f"\nİşlenen yer: {place.get('name')}")
            
            # Eğer bu yer zaten kayıtlıysa atla
            if Place.objects.filter(opentripmap_id=place['xid']).exists():
                print(f"Bu yer zaten kayıtlı: {place.get('name')}")
                continue
                
            # Detaylı bilgileri al
            details_url = f"https://api.opentripmap.com/0.1/en/places/xid/{place['xid']}"
            details_params = {
                "apikey": settings.OPENTRIPMAP_API_KEY
            }
            
            print(f"Detay URL: {details_url}")
            print(f"Detay Parametreleri: {details_params}")
            
            time.sleep(1)  # Rate limit için bekle
            
            details_response = requests.get(details_url, params=details_params)
            print(f"Detay Yanıt Kodu: {details_response.status_code}")
            
            if details_response.status_code != 200:
                print(f"Detay Yanıtı: {details_response.text}")
                continue
                
            details = details_response.json()
            print(f"Detay Yanıtı: {details}")
            
            # Fotoğraf ve açıklama kontrolü
            has_photo = 'preview' in details and 'source' in details['preview']
            has_description = 'wikipedia_extracts' in details and 'text' in details['wikipedia_extracts']
            
            if not (has_photo or has_description):
                print(f"Fotoğraf ve açıklama bilgisi olmadığı için atlanıyor: {details.get('name', '')}")
                skipped_places += 1
                continue
            
            # Yeni Place nesnesi oluştur
            place_obj = Place(
                city=city_object,
                name=details.get('name', ''),
                description=details.get('wikipedia_extracts', {}).get('text', '') if has_description else '',
                opentripmap_id=place['xid'],
                rating=details.get('rate', 0),
                review_count=0,  # OpenTripMap'te review sayısı yok
                category=details.get('kinds', '').split(',')[0] if 'kinds' in details else '',
                subcategory=details.get('kinds', '').split(',')[1] if 'kinds' in details and len(details['kinds'].split(',')) > 1 else '',
                price_tier='',  # OpenTripMap'te fiyat bilgisi yok
                website=details.get('url', ''),
                phone=details.get('phone', ''),
                address=details.get('address', {}).get('road', '') + ', ' + details.get('address', {}).get('city', ''),
                latitude=details.get('point', {}).get('lat', 0),
                longitude=details.get('point', {}).get('lon', 0),
                hours={}  # OpenTripMap'te çalışma saatleri yok
            )
            place_obj.save()
            print(f"Yer kaydedildi: {place_obj.name}")
            saved_places += 1
            
            # Fotoğrafları kaydet
            if has_photo:
                photo_url = details['preview']['source']
                PlacePhoto.objects.create(
                    place=place_obj,
                    photo_url=photo_url
                )
                print(f"Fotoğraf kaydedildi: {photo_url}")
            
            # API rate limit'ini aşmamak için bekle
            time.sleep(1)
            
        print(f"\n{city_name} için işlem tamamlandı:")
        print(f"- Kaydedilen yer sayısı: {saved_places}")
        print(f"- Atlanan yer sayısı: {skipped_places}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"OpenTripMap API hatası: {e}")
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

