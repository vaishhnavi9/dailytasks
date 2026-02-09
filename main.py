from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Product
from database import SessionLocal, engine
import database_models

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def greet():
    return {"message": "Welcome to Telesuko Track"}


products = [
    Product(id=1, name="phone", description="budget phone", price=99, quantity=10),
    Product(id=2, name="laptop", description="gaming laptop", price=999, quantity=6),
]

def init_db():
    db = SessionLocal()
    if db.query(database_models.Product).count() == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
    db.close()

init_db()


@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    return db.query(database_models.Product).all()

@app.get("/product/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db_product = database_models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.put("/product/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.model_dump().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/product/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(
        database_models.Product.id == id
    ).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}


        
