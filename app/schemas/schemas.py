from pydantic import BaseModel, Field
from typing import Optional

class ProductRequest(BaseModel):
    id: Optional[int] = Field(description="Id is not needed on create", default=None)
    url: str
    telegram_chat_id: str
    target_price: float

    model_config = {
        "json_schema_extra": {
            "example": {
                "url": "https://mercadolivre.com/produto",
                "telegram_chat_id": "1234567890",
                "target_price": 1099.9
            }
        }
    }