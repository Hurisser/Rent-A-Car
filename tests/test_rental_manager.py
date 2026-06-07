import pytest
from unittest.mock import MagicMock

# ──────────────────────────────────────────────
# Mock Uygulamaları (DB / ORM'den izole edilmiş)
# ──────────────────────────────────────────────

class CarManager:
    def __init__(self, db_session):
        self.db = db_session

    def add(self, daily_price):
        if daily_price <= 0:
            raise ValueError("ValidationError")
        self.db.save({"price": daily_price})
        return True


def check_driver_eligibility(age, segment):
    if segment == 'SUV' and age < 25:
        return False
    return True


def calculate_total_rental_fee(daily_rate, days, age):
    if days < 0:
        raise ValueError("Days cannot be negative")

    base_fee = daily_rate * days        # DEF: base_fee

    if age < 25:                        # USE: age
        base_fee += base_fee * 0.15    # USE + DEF: base_fee (genç sürücü sürşarjı)

    if days >= 10:                      # USE: days
        base_fee -= base_fee * 0.10    # USE + DEF: base_fee (uzun dönem indirimi)

    return base_fee                     # USE: base_fee


@pytest.fixture
def car_manager():
    mock_db = MagicMock()
    return CarManager(db_session=mock_db)


# ──────────────────────────────────────────────
# Test Senaryoları (Huriser Ergün)
# ──────────────────────────────────────────────

def test_TC_01_car_add_negative_price(car_manager):
    """
    Test Case ID : TC_01
    Teknik       : Kara Kutu (EP – Geçersiz Sınıf)
    Durum/Sapma  : Orijinal. Planda belirtilen daily_price = -50 birebir kullanıldı.
    """
    with pytest.raises(ValueError, match="ValidationError"):
        car_manager.add(daily_price=-50)


def test_TC_02_car_add_zero_price(car_manager):
    """
    Test Case ID : TC_02
    Teknik       : Kara Kutu (BVA – Alt sınır / geçersiz)
    Durum/Sapma  : Orijinal. Sınır değeri (0) aynen korunmuştur.
    """
    with pytest.raises(ValueError, match="ValidationError"):
        car_manager.add(daily_price=0)


def test_TC_03_car_add_valid_price(car_manager):
    """
    Test Case ID : TC_03
    Teknik       : Kara Kutu (BVA – Alt sınır / geçerli minimum)
    Durum/Sapma  : Orijinal. daily_price = 1 ile True beklentisi plandaki gibidir.
    """
    result = car_manager.add(daily_price=1)
    assert result is True


def test_TC_08_driver_eligibility_underage_suv():
    """
    Test Case ID : TC_08
    Teknik       : Kara Kutu (EP – Geçersiz Sınıf)
    Durum/Sapma  : Orijinal. Yaş (20) ve segment (SUV) değerleri değiştirilmedi.
    """
    result = check_driver_eligibility(age=20, segment='SUV')
    assert result is False


def test_TC_09_driver_eligibility_eligible_suv():
    """
    Test Case ID : TC_09
    Teknik       : Kara Kutu (EP – Geçerli Sınıf)
    Durum/Sapma  : Orijinal. Planda tanımlanan age=25, segment='SUV' parametreleri
                   aynen kullanıldı. 25 yaş minimum eşiği karşıladığından True beklenir.
    """
    result = check_driver_eligibility(age=25, segment='SUV')
    assert result is True


def test_TC_12_calculate_fee_surcharge_and_discount():
    """
    Test Case ID : TC_12
    Teknik       : Beyaz Kutu (Yol Testi + Veri Akışı – DU Çifti)
    Durum/Sapma  : Orijinal. daily_rate=1000, days=10, age=21 parametreleri korundu.

    Tetiklenen yürütme yolu (Path C – her iki dal da aktif):
      base_fee = 1000 × 10             = 10 000,0   ← DEF
      age < 25  → += 10000 × 0.15     = 11 500,0   ← USE + DEF (sürşarj dalı)
      days >= 10 → -= 11500 × 0.10    = 10 350,0   ← USE + DEF (indirim dalı)
      return base_fee                               ← USE

    DU çiftleri:
      base_fee: (def @ ilk hesap) → (use @ sürşarj)
      base_fee: (def @ sürşarj)   → (use @ indirim)
      base_fee: (def @ indirim)   → (use @ return)
    """
    result = calculate_total_rental_fee(daily_rate=1000, days=10, age=21)
    assert result == 10350.0