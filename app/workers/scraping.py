from bs4 import BeautifulSoup
from sqlmodel import Session, create_engine, select
from app.models.product_models import PriceHistory, Product
from app.core.logger import setup_logger
from dotenv import load_dotenv
import os 
import time
import requests

load_dotenv()

logger = setup_logger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

COOLDOWN = os.getenv("COOLDOWN")

engine = create_engine(DATABASE_URL)

timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
}

def get_all_products() -> list[Product]:
    with Session(engine) as session:
        statement = select(Product)
        products = session.exec(statement).all()
    
    return products

def fetch_page(url: str) -> str:
    response = requests.get(url, headers=headers)
    return response.text

def parse_page(html: str, url: str) -> dict:
    soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
    product_name: str = soup.find('h1', class_='ui-pdp-title').get_text()
    prices: list = soup.find_all('span', class_='andes-money-amount__fraction') 
    current_price: int = int(prices[1].get_text().replace('.', ''))
    first_price: int = int(prices[0].get_text().replace('.', ''))

    
    data = {
        'product_name': product_name,
        'url': url,
        'current_price': float(current_price),
        'first_price': float(first_price),
        'last_scraped_at': timestamp
    }

    return data

    
def update_product(session: Session, product: Product, new_data: dict):
    product.first_price = product.current_price
    product.current_price = new_data['current_price']
    product.last_scraped_at = timestamp

    session.add(product)

def add_price_history(session: Session, product: Product):
    price_entry = PriceHistory(
        product_id=product.id,
        price=product.current_price
    )

    session.add(price_entry)

def main():
    logger.info("Scraping has been initialized")
    while True:
        products = get_all_products()
        with Session(engine) as session:
            for product in products:
                html = fetch_page(product.url)
                new_data = parse_page(html, product.url)

                if new_data['current_price'] != product.current_price:
                    update_product(session, product, new_data)
                    add_price_history(session, product)

            session.commit()

            time.sleep(int(COOLDOWN))


if __name__ == '__main__':
    main()