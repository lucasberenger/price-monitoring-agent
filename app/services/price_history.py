from sqlmodel import Session
from app.models.product_models import PriceHistory
from datetime import datetime


def save_price_history(session: Session, product_id: int, price: float) -> PriceHistory:
    price = PriceHistory(product_id=product_id, price=price, scraped_at=datetime.utcnow())
    session.add(price)
    session.commit(price)
    session.refresh(price)

    return price
