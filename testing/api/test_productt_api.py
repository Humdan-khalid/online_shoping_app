from app.database_models.product_model import Products
from app.database_models.seller_model import Sellers
from app.repository.seller_repo import seller_data_save_in_database

def test_create_new_product_successfully(client, seller, session):
    new_seller = Sellers(
        name="Hamdan",
        age=22,
        city="Karachi",
        phone_number="03192930393",
        email="hamdan@gmail.com",
        password="Bismillah2830"
    )
    session.add(new_seller)
    session.commit()
    session.refresh(new_seller)

    new_product = Products(
        name="Hand free",
        price=500,
        weight="0.10gm",
        colour="white",
        brand="Ronin",
        description="This hand free sound is very smooth and soft.",
        quantity=1
    )

    data = client.post("/product", json=new_product.model_dump(mode="json"),
                        headers={"Authorization": f"Bearer {seller}"}
    )


    print(f"SSSStatus code: {data.status_code}")
    
    result = data.json()

    assert data.status_code == 201

    assert result["name"] == "Hand free"
