from app.repository.product_repo import find_product_in_database, find_seller_product_in_database, update_product_attributes_in_database
from app.database_models.product_model import Products, UpdateProduct
from app.database_models.seller_model import Sellers

def test_product_not_found_in_database(session):
    result = find_product_in_database(1, session)

    assert result == None

def test_product_found_in_database(session):
    new_product = Products(
        name="Petroleum",
        price=500.0,
        colour="White",
        brand="Vaseline",
        description="This cream is very good for skin.",
        quantity=200,
        weight="100gm",
        seller_id=3
    )
    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    result = find_product_in_database(new_product.id, session)

    assert result.name == "Petroleum"
    assert result.brand == "Vaseline"

def test_find_seller_product_in_database(session):
    result = find_seller_product_in_database(1, 5, session)

    assert result == None


def test_seller_product_find_in_database(session):
    new_seller = Sellers(
        name="Alia Sohail",
        age=30,
        phone_number="03123838448",
        city="London",
        email="aliasohial222@gmail.com",
        password="Hello1232"
    )

    session.add(new_seller)
    session.commit()
    session.refresh(new_seller)

    new_product = Products(
        name="Petroleum",
        price=500.0,
        colour="White",
        brand="Vaseline",
        description="This cream is very good for skin.",
        quantity=200,
        weight="100gm",
        seller_id=new_seller.id
    )
    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    result = find_seller_product_in_database(1, 1, session)

    assert result is not None
    assert result.seller_id == new_seller.id
    assert result.id == new_product.id

def test_update_product_attributes(session):
    new_seller = Sellers(
        name="Alia Sohail",
        age=30,
        phone_number="03123838448",
        city="London",
        email="aliasohial222@gmail.com",
        password="Hello1232"
    )

    session.add(new_seller)
    session.commit()
    session.refresh(new_seller)
    
    new_product = Products(
        name="Petroleum",
        price=500.0,
        colour="White",
        brand="Vaseline",
        description="This cream is very good for skin.",
        quantity=200,
        weight="100gm",
        seller_id=new_seller.id
    )
    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    product = UpdateProduct(
        price=520.0,
        quantity=100
    )

    product_update = product.model_dump(exclude_none=True)
    for key, value in product_update.items():
        setattr(new_product, key, value)

    result = update_product_attributes_in_database(new_product, session)

    assert result.price == 520.0
    assert result.name == "Petroleum"

    