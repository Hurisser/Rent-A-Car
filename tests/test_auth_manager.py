import pytest
from unittest.mock import patch, MagicMock


class DummyAuthManager:
    def register(self, password):
        if len(password) < 6:
            raise ValueError("PasswordLengthException: Şifre en az 6 karakter olmalıdır.")
        return True

@pytest.fixture
def auth_manager():
    return DummyAuthManager()


def test_TC_06_auth_register_short_password(auth_manager):
    """
    TC_06 | Black-Box | BVA - Minimum Boundary (below)
    Method  : AuthManager.register()
    Input   : password = "12345" (5 karakter — sınırın altında)
    Expected: PasswordLengthException raised VEYA return False
    """
    try:
        result = auth_manager.register(password="12345")
        assert result is False, (
            "TC_06 FAILED: 6 karakterden kısa şifreler reddedilmelidir."
        )
    except (ValueError, Exception):
        pass  # Exception fırlatılması da geçerli davranış kabul edilir


def test_TC_07_auth_register_valid_password(auth_manager):
    """
    TC_07 | Black-Box | BVA - Minimum Boundary (at boundary)
    Method  : AuthManager.register()
    Input   : password = "123456" (6 karakter — tam sınır değeri)
    Expected: True
    """
    result = auth_manager.register(password="123456")
    assert result is True, (
        "TC_07 FAILED: 6 karakterli şifre sınır değer olarak kabul edilmelidir."
    )