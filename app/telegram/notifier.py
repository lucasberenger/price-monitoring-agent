from dotenv import load_dotenv
from telegram import Bot
from ..models.models import Product
import os 

load_dotenv()

TELEGRAM_TOKEN=os.getenv("TELEGRAM_TOKEN")
bot=Bot(token=TELEGRAM_TOKEN)

async def notify_product_added(telegram_chat_id: str, product_name: str):
    text = f"✅ The product {product_name} was added successfully!"
    await bot.send_message(chat_id=telegram_chat_id, text=text)

async def notify_price_drop(telegram_chat_id: str, product: Product):
    text = f"📉 The price of {product.product_name} has been dropped to {product.current_price}!\nCheck it out: {product.url}"
    await bot.send_message(chat_id=telegram_chat_id, text=text)

async def notify_product_deleted(telegram_chat_id: str, product: Product):
    text = f"🗑️ The product {product.product_name} has been deleted successfully!"
    await bot.send_message(telegram_chat_id, text=text)