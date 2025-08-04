from pydantic import BaseModel

class ProductRequest(BaseModel):
    url: str
    telegram_chat_id: str
    target_price: float