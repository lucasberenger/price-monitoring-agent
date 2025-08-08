from sqlmodel import Session
from app.models.product_models import Alert

def create_alert(session: Session, 
                 product_id: int, 
                 telegram_chat_id: str, 
                 target_price: float) -> Alert:
    
    alert = Alert(product_id=product_id, telegram_chat_id=telegram_chat_id, target_price=target_price)
    session.add(alert)
    session.commit()
    session.refresh(alert)

    return alert