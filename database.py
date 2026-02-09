from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

DB_USER = "postgres"
DB_PASSWORD = quote_plus("Vaish@2003")  # encode special chars
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "telesuko"

DB_URL= f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)

session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
