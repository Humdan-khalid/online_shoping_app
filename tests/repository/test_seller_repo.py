# # tests/test_seller_repo.py

# from unittest.mock import Mock

from app.repository.seller_repo import get_seller_from_token
from unittest.mock import Mock

def test_find_seller_successfully_for_token_verification():
        session = Mock()

        expected_seller = Mock()
        expected_seller.id = 1
        expected_seller.email = "hamdan@gmail.com"

        seller = {
                "id": 1,
                "email": "hamdan@gmail.com"
        }

        mock_result = Mock()

        session.exec.return_value=mock_result

        mock_result.first.return_value=expected_seller

        result = get_seller_from_token(seller, session)

        assert result == expected_seller
        session.exec.assert_called_once()
        mock_result.first.assert_called_once()


def test_find_seller_for_token_verification():
        session = Mock()

        expected_seller = Mock()
        expected_seller.id = 1
        expected_seller.email = "hamdan@gmail.com"

        seller = {
                "id": 1,
                "email": "hamdan@gmail.com"
        }

        mock_result = Mock()

        session.exec.return_value=mock_result

        mock_result.first.return_value=None

        result = get_seller_from_token(seller, session)

        assert result != expected_seller
        session.exec.assert_called_once()
        mock_result.first.assert_called_once()