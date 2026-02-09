from fastapi import Depends, FastAPI
from models import Product
from database import session, engine
from sqlalchemy.orm import Session
import database_models
app=FastAPI()  

database_models.Base.metadata.create_all(bind=engine)
@app.get("/")
def greet():
    return"welcome to telesuko track"

products=[
    Product(id=1,name="phone",description="budget phone",price=99,quantity=10),
    Product(id=2,name="laptop",description="gaming laptop",price=999,quantity=6),
]

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db=session()
    count=db.query(database_models.Product).count()
    if(count==0):
        db=session()
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
    db.commit()
init_db()
@app.get("/products")
def get_all_products(db:Session=Depends(get_db)):
    db_products=db.query(database_models.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id:int, db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        return db_product
    return "product not found"
@app.post("/products")
def add_product(product:Product, db:Session=Depends(get_db)):
    db_product=database_models.Product(**product.model_dump())
    db.commit()
    return db_product

@app.put("/product")

def update_product(id:int,product:Product):
    for i in range (len(products)):
        if(products[i].id==id):
            products[i]=product
            return "prodcut added successfully"
        
    return "no product found"
@app.delete("/product")
def delete_product(id:int):
    for i in range(len(products)):
        if products[i].id==id:
            del products[i]
            return "product deleted successfully"
    return "product not found"

        