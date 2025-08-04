from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import datetime

class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    product_name: str
    url: str
    current_price: float
    old_price: float
    last_scraped_at: Optional[datetime] = None
    alert: Optional["Alert"] = Relationship(
        back_populates="product", 
        sa_relationship_kwargs={'uselist': False},
        cascade_delete=True
    )
    price_history: list["PriceHistory"] = Relationship(back_populates="product", cascade_delete=True)

class PriceHistory(SQLModel, table=True):
    __tablename__ = "price_history"

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id")
    price: float
    scraped_at: datetime = Field(default_factory=datetime.utcnow)
    product: Optional["Product"] = Relationship(back_populates="price_history")

class Alert(SQLModel, table=True):
    __tablename__ = "alerts"

    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id", unique=True)
    telegram_chat_id: str
    target_price: float
    is_active: bool = True
    product: Optional[Product] = Relationship(back_populates="alert")
    