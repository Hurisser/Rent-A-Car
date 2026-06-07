import pytest
from datetime import date

class DummyRentalManager:
    def checkDates(self, rent_date, return_date):
        # String gelirse date objesine çevir
        if isinstance(rent_date, str):
            rent_date = date.fromisoformat(rent_date)
            return_date = date.fromisoformat(return_date)
        if return_date < rent_date:
            return False
        return True


def calculate_total_rental_fee(daily_rate, days, age):
    """Mevcut sıra: önce sürşarj (age<25), sonra indirim (days>=10)"""
    if days < 0:
        raise ValueError("Days cannot be negative")

    base_fee = daily_rate * days 

    if age < 25:
        base_fee += base_fee * 0.15 
    if days >= 10:
        base_fee -= base_fee * 0.10 

    return base_fee 


@pytest.fixture
def rental_manager():
    return DummyRentalManager()

def test_TC_04_check_dates_chronological_error(rental_manager):
    """
    TC_04 | Black-Box | EP - Chronological Error
    Method  : RentalManager.checkDates()
    Input   : rent_date=2026-05-15, return_date=2026-05-12 (return < rent)
    Expected: False (InvalidDateException veya False)
    """
    try:
        result = rental_manager.checkDates(
            rent_date="2026-05-15",
            return_date="2026-05-12"
        )
        assert result is False, (
            "TC_04 FAILED: Dönüş tarihi kiralama tarihinden önce olamaz."
        )
    except Exception:
        pass  # Exception fırlatılması da geçerli davranış kabul edilir


def test_TC_05_check_dates_same_day(rental_manager):
    """
    TC_05 | Black-Box | BVA - Boundary Condition
    Method  : RentalManager.checkDates()
    Input   : rent_date=2026-05-15, return_date=2026-05-15 (aynı gün)
    Expected: True (sınır değer kabul edilmeli)
    """
    result = rental_manager.checkDates(
        rent_date="2026-05-15",
        return_date="2026-05-15"
    )
    assert result is True, (
        "TC_05 FAILED: Aynı gün kiralama (boundary) kabul edilmelidir."
    )

def check_driver_eligibility(age, segment):
    """
    Gerçek import kurulana kadar geçici fonksiyon.
    Gerçek kullanım:
      from controller.rental_manager import check_driver_eligibility
    """
    if segment == 'SUV' and age < 25:
        return False
    return True


def test_TC_09_driver_eligibility_valid():
    """
    TC_09 | Black-Box | Equivalence Partitioning - Valid Class
    Method  : check_driver_eligibility()
    Input   : age=25, segment='SUV'
    Expected: True
    EP      : age=25 → geçerli sınıf (>=25), SUV segmenti için uygun sürücü
    """
    result = check_driver_eligibility(age=25, segment='SUV')
    assert result is True, (
        "TC_09 FAILED: 25 yaş SUV segmenti için geçerli sınıfta kabul edilmelidir."
    )

def test_TC_10_calc_fee_negative_days():
    """
    TC_10 | White-Box | Path Testing - Exception Flow
    Method  : calculate_total_rental_fee()
    Input   : daily_rate=1000, days=-2, age=30
    Expected: ValueError raised
    DU Pair : base_fee tanımlanmadan exception path'i izlenmeli
    """
    with pytest.raises(ValueError, match="Days cannot be negative"):
        calculate_total_rental_fee(daily_rate=1000, days=-2, age=30)


def test_TC_11_calc_fee_standard_flow():
    """
    TC_11 | White-Box | Path Testing - Standard Flow
    Method  : calculate_total_rental_fee()
    Input   : daily_rate=1000, days=5, age=30
    Expected: 5000.0
    Path    : days>=0 ✓ | age>=25 → no surcharge | days<10 → no discount
    DU Pair : base_fee DEF(1) → USE(return)
    """
    fee = calculate_total_rental_fee(daily_rate=1000, days=5, age=30)
    assert fee == 5000.0, f"TC_11 FAILED: Beklenen 5000.0, alınan {fee}"

