from sqlmodel import SQLModel, create_engine

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False}
)