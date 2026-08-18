from app.repository.seller_repo import get_seller_from_token
from unittest.mock import Mock
from app.database_models.seller_model import CreateSeller, Sellers

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

def test_find_seller_successfully_for_token_verify(db_session):
        seller = Sellers(
                id=2,
                name="Hamdan",
                age=22,
                phone_number="03127273747",
                city="Islamabad",
                email="hamdan@gmail.com",
                password="Hello1245$!"
        )

        db_session.add(seller)
        db_session.commit()
        db_session.refresh(seller)

        seller_login: dict = {
                "id": 2,
                "email": "hamdan@gmail.com"
        }

        result = get_seller_from_token(seller_login, db_session)
        assert result == seller


def test_seller_not_find_successfully_for_token_verify(db_session):

        seller_login: dict = {
                "id": 2,
                "email": "hamdan122@gmail.com"
        }

        result = get_seller_from_token(seller_login, db_session)
        assert result == None