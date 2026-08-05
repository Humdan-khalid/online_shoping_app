from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")
test_database_url = os.getenv("TEST_DATABASE_URL")