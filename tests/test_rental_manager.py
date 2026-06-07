import pytest

class DummyRentalManager:
    def checkDates(self, rent_date, return_date):
        if return_date < rent_date:
            return False
        return True

def calculate_total_rental_fee(daily_rate, days, age):
    if days < 0:
        raise ValueError("Days cannot be negative")
    
    base_fee = daily_rate * days
    
    if age < 25:
        base_fee += base_fee * 0.15  # %15 Genç sürücü sürşarjı
    if days >= 10:
        base_fee -= base_fee * 0.10  # %10 Uzun dönem indirimi
        
    return base_fee

@pytest.fixture
def rental_manager():
    return DummyRentalManager()

def test_TC_04_check_dates_chronological_error(rental_manager):
    """TC_04: Black-Box (EP - Chronological error)"""
    result = rental_manager.checkDates(rent_date="2026-05-15", return_date="2026-05-12")
    assert result is False, "TC_04 FAILED: Dönüş tarihi, kiralama tarihinden önce olamaz."

def test_TC_05_check_dates_same_day(rental_manager):
    """TC_05: Black-Box (BVA - Boundary condition)"""
    result = rental_manager.checkDates(rent_date="2026-05-15", return_date="2026-05-15")
    assert result is True, "TC_05 FAILED: Aynı gün içinde kiralama (sınır değer) kabul edilmelidir."

def test_TC_09_calc_fee_negative_days():
    """TC_09: White-Box (Path Testing - Exception flow)"""
    with pytest.raises(ValueError):
        calculate_total_rental_fee(daily_rate=1000, days=-2, age=30)

def test_TC_10_calc_fee_standard():
    """TC_10: White-Box (Path Testing - Standard flow)"""
    fee = calculate_total_rental_fee(daily_rate=1000, days=5, age=30)
    assert fee == 5000.0, f"TC_10 FAILED: Beklenen 5000.0, alınan {fee}"

def test_TC_11_calc_fee_discount_surcharge():
    """TC_11: White-Box (Path Testing & Data Flow - DU Pair)"""
    fee = calculate_total_rental_fee(daily_rate=1000, days=10, age=21)
    assert fee == 10350.0, f"TC_11 FAILED: Beklenen 10350.0, alınan {fee}"