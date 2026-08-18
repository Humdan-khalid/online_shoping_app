import redis
import json

r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

def get_seller_products_in_cache(seller_id: int):
    key = f"seller:{seller_id}"

    cache_data = r.get(key)

    if not cache_data:
        return None

    return json.loads(cache_data)


def store_seller_products_in_cache(
    seller_id: int,
    seller_products: list
):
    key = f"seller:{seller_id}"

    products_data = [
        product.model_dump(mode="json")
        for product in seller_products
    ]

    r.set(
        key,
        json.dumps(products_data)
    )

def delete_seller_products_in_cache(seller_id: int):
    key = f"seller:{seller_id}"
    return r.delete(key)
    