import os
import asyncio
import pandas as pd
import ollama 
from pandas import DataFrame
from dotenv import load_dotenv
from telegram import Bot

load_dotenv() 

MODEL = os.getenv('MODEL')
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
url = os.getenv('URL')
bot = Bot(token=TOKEN)


system_prompt: str = 'You are an assistant that analyzes the prices of a product \
    and make a prediction about the likely price trend in the coming days based on the data.'

df: DataFrame = pd.read_csv('prices.csv')

def user_prompt_for(df: DataFrame) -> str:
    latest_data: DataFrame = df.tail(10)
    product_name: str = latest_data['product_name'].iloc[-1]
    price_history: str = latest_data[['timestamp', 'old_price', 'new_price', 'installment_price']].to_string(index=False)
    user_prompt: str = f'''
The following table shows the price history of {product_name} over the last few days:
{price_history}

Based on the historical data, your task is to analyze the price trends and provide a suggestion. Please follow these guidelines:

1. Identify any downward trend in the new price.
2. If the current discount compared to the old price is 15% or more, suggest: "You should buy now!"
3. If prices are stable or increasing, or if a better discount may come soon, suggest: "You should wait!"
4. If you predict that the price might drop further based on recent trends, explain why and suggest: "You should wait!"

**Your response should include the following**:
- A brief analysis summary of the price trends.
- A table of the most recent prices, highlighting any significant changes.
- A final suggestion, which should be either "You should buy now!" or "You should wait!".
- Include the product URL after your suggestion for easy access to the product page.

Make sure your answer follows this structure:
- **Summary of Analysis**: A concise explanation of the price behavior.
- **Price History**: The recent price table.
- **Final Suggestion**: Your final recommendation based on the analysis, along with the URL{url} of the product.
'''
    
    return user_prompt

def messages_for(df: DataFrame) -> list[dict[str, str]]:
    return [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt_for(df)}
    ]

def analyze_prices(df: DataFrame) -> str:
    messages = messages_for(df)
    responses = ollama.chat(model=MODEL, messages=messages)
    result = responses['message']['content']

    return result

async def send_telegram_message(text: str) -> None:
    await bot.send_message(chat_id=CHAT_ID, text=text)

async def main() -> None:
    result: str = analyze_prices(df)

    if 'buy' in result.lower():
        await send_telegram_message(result)

asyncio.run(main())
    




