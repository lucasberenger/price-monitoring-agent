import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv() 

url = os.getenv('URL')

def fetch_page(url):
    response = requests.get(url)
    return response.text

timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    product_name = soup.find('h1', class_='ui-pdp-title').get_text()
    prices: list = soup.find_all('span', class_='andes-money-amount__fraction') 
    new_price: int = int(prices[1].get_text().replace('.', ''))
    old_price: int = int(prices[0].get_text().replace('.', ''))
    installment_price: int = int(prices[2].get_text().replace('.', ''))

    
    return {
        'product_name': product_name,
        'old_price': old_price,
        'new_price': new_price,
        'installment_price': installment_price,
        'timestamp': timestamp
    }

def save_to_dataframe(product_info, df):
    new_row = pd.DataFrame([product_info])
    df = pd.concat([df, new_row], ignore_index=True)
    return df

def create_file_or_append(df):
    df.to_csv('prices.csv', mode='a' if os.path.exists('prices.csv') else 'w',
        header=not os.path.exists('prices.csv'),
        index=False
    )

if __name__ == '__main__':

    df = pd.DataFrame()

    while True:
        page_content = fetch_page(url)
        product_info = parse_page(page_content)
        df = save_to_dataframe(product_info,df)
        create_file_or_append(df)
        time.sleep(120)




