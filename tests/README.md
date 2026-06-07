# Rent-A-Car - Test Implementation (Phase 2)

Bu proje, BIMU3926 Software Testing and Quality dersi Phase 2 ödevi kapsamında test edilmiştir.

## Test Ortamının Kurulumu
1. Python sanal ortamını aktif edin.
2. Gerekli kütüphaneleri kurmak için: `pip install -r requirements.txt`

## Testleri Çalıştırma
Tüm testleri hızlı ve özet bir şekilde çalıştırmak için aşağıdaki komutu kullanın:
`pytest -q`

## Özellikler
* **MVC Mimarisi:** Veri (Model), iş mantığı (Controller) ve kullanıcı arayüzünün (View) birbirinden tamamen izole edildiği temiz kod yapısı.
* **JSON Veri Kalıcılığı:** Veritabanı bağımlılığı olmadan, verilerin hafif ve hızlı bir şekilde JSON formatında saklanması/okunması.
* **Gelişmiş İş Mantığı:** Yaş ve araç segmentine göre sürücü uygunluk kontrolleri, dinamik kiralama ücreti (sürşarj ve indirimler) hesaplamaları.
* **Test Edilebilirlik:** İş mantığı katmanı, `pytest` ve `unittest.mock` kullanılarak dış bağımlılıklardan (JSON okuma/yazma) izole edilerek test edilmiştir.

## Proje Yapısı
```text
RENT-A-CAR/
├── controller/          # İş mantığı, validasyonlar ve hesaplama algoritmaları
├── data/                # JSON veri tabanı dosyaları
├── model/               # Python veri modelleri (Car, User, Rental vb.)
├── view/                # Kullanıcı etkileşim arayüzü (Console/CLI)
├── tests/               # pytest ile yazılmış Phase 2 birim testleri
|   ├── README.md
│   ├── test_auth_manager.py
│   ├── test_car_manager.py
│   └── test_rental_manager.py
├── main.py              # Uygulamanın ana başlangıç noktası
└── requirements.txt     # Proje bağımlılıkları (pytest vb.)