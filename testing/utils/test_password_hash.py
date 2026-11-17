from app.utils.password_hash import create_hash_password, pwd_context
import pytest

def test_create_hash_password(session):
    password = "Kanon121$%#"
    result = create_hash_password(password)

    print(f"Resulttttt: {result}")
    assert result is not None
    assert result != password
    assert pwd_context.verify(password, result) is True 

def test_create_hash_password_with_none(session):
    with pytest.raises(ValueError):
        create_hash_password(None)