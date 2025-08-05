from bs4 import BeautifulSoup
from sqlmodel import Session, create_engine
from ..models.models import Product
from dotenv import load_dotenv
import os 
import time
import requests

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
}

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

def save_data(data: dict) -> dict:
    with Session(engine) as session:
        new_product_info = Product(**data)
        session.add(new_product_info)
        session.commit()
        session.refresh(new_product_info)

        return new_product_info.model_dump()