from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound
from app.models.models import Product

def list_all_products(session: Session) -> list[Product]:
    statement = select(Product)
    result = session.exec(statement).all()

    return result


def list_product_by_id(session: Session, id: int) -> Product:
    statement = select(Product).where(Product.id == id)
    result = session.exec(statement).first()

    return result


def add_product(session: Session, data: dict) -> Product:
    new_product = Product(**data)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    return new_product

def delete_product(session: Session, id: int) -> Product:
    statement = select(Product).where(Product.id == id)
    result = session.exec(statement)
    product = result.one()

    if not product:
        raise NoResultFound()

    session.delete(product)
    session.commit()

    return product
