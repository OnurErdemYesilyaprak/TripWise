## TripWise – Türkiye Gezi Rehberi (Öğrenci Projesi)

TripWise, Türkiye'nin dört bir yanındaki gezilecek yerleri, yemek mekânlarını ve konaklama seçeneklerini keşfetmeyi kolaylaştıran bir web uygulamasıdır. Proje, kullanıcı dostu bir arayüz ile şehir bazlı içerikleri sunar ve verileri Google Places API üzerinden derler.

Uygulama, bir dönem ödevi kapsamında geliştirilmiş olup; arayüzde Tailwind CSS, sunucu tarafında Python/Django ve veritabanı olarak SQLite kullanır.

---

### Ekip ve Projenin Amacı

Bu proje, Amasya Üniversitesi Bilgisayar Mühendisliği öğrencileri tarafından bir ders ödevi olarak hazırlanmıştır. Amaç, Türkiye'nin gezilecek yerlerini tanıtmak ve keşfi kolaylaştıracak bir rehber sunmaktır.

- Onur Erdem Yeşilyaprak
- Ali Faruk Kahraman
- Enes Birer
- Atıf Samed Karaca

Projenin temel hedefleri:
- Şehirler için “Gezilecek Yerler, Yemekler, Konaklama” içeriklerini listelemek
- Google Places API ile temel bilgileri ve görselleri göstermek
- Basit ve modern bir arayüzle gezinmeyi kolaylaştırmak

---

### Kurulum ve Çalıştırma

Önkoşullar:
- Python 3.11+ (tercihen 3.13)
- Bir Google Places API anahtarı (Billing açık ve doğru kısıtlamalarla)

Depoyu yerel makinenize aldıktan sonra aşağıdaki adımları izleyin.

1) Sanal ortam oluşturma ve etkinleştirme

- Windows (PowerShell):
```powershell
cd C:\Users\Enes\Desktop\TripWise\tripwise
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- macOS/Linux (bash/zsh):
```bash
cd ~/Desktop/TripWise/tripwise
python -m venv .venv
source .venv/bin/activate
```

2) Bağımlılıkların kurulumu

```bash
pip install -r requirements.txt
```

3) Ortam değişkeni (Google Places API)

Uygulama `python-decouple` ile ortam değişkeninden anahtarı okur. Aşağıdaki seçeneklerden birini kullanabilirsiniz:

- Geçici olarak terminal oturumunda tanımlama:
  - Windows (PowerShell):
    ```powershell
    $env:GOOGLE_PLACES_API_KEY = "YOUR_API_KEY"
    ```
  - macOS/Linux:
    ```bash
    export GOOGLE_PLACES_API_KEY="YOUR_API_KEY"
    ```

- Ya da `.env` dosyası (proje kökü veya `tripwise/tripwise` ile aynı seviyede):
  ```env
  GOOGLE_PLACES_API_KEY=YOUR_API_KEY
  ```

4) Veritabanı migrasyonları

```bash
cd C:\Users\Enes\Desktop\TripWise\tripwise
python manage.py migrate
```

5) Geliştirme sunucusunu çalıştırma

```bash
python manage.py runserver 127.0.0.1:8000
```

Notlar:
- Eğer `manage.py` bulunamadı hatası alırsanız, komutu `C:\Users\Enes\Desktop\TripWise` dizininde (içinde `manage.py` olan kökte) çalıştırdığınızdan emin olun. Yapı şu şekildedir:
  - `C:\Users\Enes\Desktop\TripWise\manage.py`
  - `C:\Users\Enes\Desktop\TripWise\tripwise\...` (Django proje paketi)
- `ALLOWED_HOSTS` geliştirmede `"*"` olarak ayarlanmıştır. Üretimde uygun domain(ler) ile sınırlandırın.
- Google Places API görselleri tarayıcıdan çağrılır. API anahtarınızın referrer/IP kısıtlamaları doğru yapılandırılmalıdır; aksi hâlde görseller 403/404 dönebilir.

---

### Lisans ve Haklar

Bu proje eğitim/öğrenci projesi olarak hazırlanmıştır. Kod ve içerikler “olduğu gibi” sunulur; herhangi bir garanti verilmez. Ticari kullanım veya yeniden dağıtım yapmadan önce proje ekibinden izin almanız önerilir.

Görseller Google Places API üzerinden elde edildiğinden, ilgili servislerin kullanım şartları ve lisansları ayrıca geçerlidir. API sağlayıcılarının politika ve kota limitlerine dikkat ediniz.

---

### Hakkımda (Enes Birer)

Merhaba, ben Enes Birer. Amasya Üniversitesi Bilgisayar Mühendisliği öğrencisiyim. TripWise projesinde geliştirme ve uygulama mimarisi konularında görev aldım. Geri bildirim, öneri veya katkılarınız için memnuniyetle iletişime geçebilirsiniz.


