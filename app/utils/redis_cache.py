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

    print("CACHE GET:", key)
    print("CACHE DATA:", cache_data)

    if not cache_data:
        return None

    json.loads(cache_data)

# def store_seller_products_in_cache(seller_id: int, seller_products: list):
#     key = f"seller_id {seller_id}"

#     product_data = [
#             product.model_dump()
#             for product in seller_products
#             ]

#     r.set(key, 
#           json.dumps(product_data),
#         ex=90
#         )

# import json

# def store_seller_products_in_cache(
#     seller_id: int,
#     seller_products: list
# ):
#     key = f"seller:{seller_id}:products"

#     products_data = [
#         product.model_dump()
#         for product in seller_products
#     ]

#     r.set(
#         key,
#         json.dumps(products_data),
#         ex=90
#     )

import json

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
        json.dumps(products_data),
        ex=90
    )

    print(f"Cache store: {key}")