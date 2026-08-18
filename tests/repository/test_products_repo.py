from app.repository.product_repo import find_seller_product_in_database, find_product_in_database
from app.database_models.product_model import Products
from app.database_models.seller_model import Sellers

# def test_find_seller_products_returns_empty_list_when_no_products(db_session):
#     seller_id = 2
#     product = find_seller_products_in_database(seller_id, db_session)
#     assert product == []


def test_find_product_successfully_in_database(db_session):

    seller = Sellers(
                id=2,
                name="Hamdan",
                age=22,
                phone_number="03127273747",
                city="Islamabad",
                email="hamdan23@gmail.com",
                password="Hello1245$!"
        )

    db_session.add(seller)
    db_session.commit()
    db_session.refresh(seller)

    product = Products(
        id=2,
        name="Charging-lead",
        price=150,
        weight="12gm",
        colour="White",
        brand="Apple",
        description="This product is very good.",
        quantity=45,
        seller_id=seller.id,
        status="Available"
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    result = find_product_in_database(2, db_session)
    assert result == product
    assert result.id == 2


def test_product_not_found_in_database(db_session):
    result = find_product_in_database(3, db_session)
    assert result == None

def test_find_seller_products_in_database(db_session):
    seller = Sellers(
                id=2,
                name="Hamdan",
                age=22,
                phone_number="03127273747",
                city="Islamabad",
                email="hamdan23@gmail.com",
                password="Hello1245$!"
        )

    db_session.add(seller)
    db_session.commit()
    db_session.refresh(seller)

    product = Products(
        id=2,
        name="Charging-lead",
        price=150,
        weight="12gm",
        colour="White",
        brand="Apple",
        description="This product is very good.",
        quantity=45,
        seller_id=seller.id,
        status="Available"
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    result = find_seller_product_in_database(2, 2, db_session)

    assert result == product

def test_seller_products_not_found_in_database(db_session):
    seller = Sellers(
                id=2,
                name="Hamdan",
                age=22,
                phone_number="03127273747",
                city="Islamabad",
                email="hamdan23@gmail.com",
                password="Hello1245$!"
        )

    db_session.add(seller)
    db_session.commit()
    db_session.refresh(seller)

    result = find_seller_product_in_database(2, 2, db_session)

    assert result == None
