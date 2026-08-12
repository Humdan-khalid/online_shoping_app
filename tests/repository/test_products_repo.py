from app.repository.product_repo import find_seller_products_in_database

def test_find_seller_products_returns_empty_list_when_no_products(db_session):
    seller_id = 2
    product = find_seller_products_in_database(seller_id, db_session)
    assert product == []