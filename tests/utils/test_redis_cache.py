from app.utils.redis_cache import delete_seller_products_in_cache, store_seller_products_in_cache
from app.database_models.product_model import Products
from app.database_models.seller_model import Sellers
from app.utils.redis_cache import r

def test_seller_product_successfully_deleted_in_cache():
    seller = Sellers(
                id=2,
                name="Hamdan",
                age=22,
                phone_number="03127273747",
                city="Islamabad",
                email="hamdan23@gmail.com",
                password="Hello1245$!"
        )

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

    key = f"seller_id: {product.seller_id}"

    store_seller_products_in_cache(key, [product])
    product_delete = delete_seller_products_in_cache(key)

    assert product_delete == 1
    assert r.get(key) == None