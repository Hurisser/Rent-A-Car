import pytest

class DummyAuthManager:
    """Gerçek kodun yerine geçen geçici sınıftır."""
    def register(self, password):
        if len(password) < 6:
            return False 
        return True

@pytest.fixture
def auth_manager():
    return DummyAuthManager()

def test_TC_06_auth_register_short_password(auth_manager):
    """TC_06: Black-Box (BVA - Min boundary 6)"""
    result = auth_manager.register(password="12345")
    assert result is False, "TC_06 FAILED: 6 karakterden kısa şifreler reddedilmelidir."

def test_TC_07_auth_register_valid_password(auth_manager):
    """TC_07: Black-Box (BVA - Min boundary 6)"""
    result = auth_manager.register(password="123456")
    assert result is True, "TC_07 FAILED: 6 karakterli şifre sınır değer olarak kabul edilmelidir."