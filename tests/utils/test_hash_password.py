from app.utils.password_hash import create_hash_password
import pytest

def test_create_hash_password():
    user_password = "Hsgsgsg3434"
    password = create_hash_password(user_password)

    assert password is not None

def test_user_password_is_none():
    user_password = None

    with pytest.raises(ValueError):
        create_hash_password(user_password)