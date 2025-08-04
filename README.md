# 🛒 Price Tracker

This project is an application that **monitors** product prices from Mercado Livre, **analyzes** recent price trends and sends **notifications** to the user via **Telegram** when price drops are detected.

---

## 🚀 Features

- 🔍 **Web Scraping**: Automatically fetches product name and price data from a product page.
- 📊 **Data Logging**: Saves extracted product data with timestamps into Postgres database for historical tracking.
- 📱 **Telegram Alerts**: Sends smart notifications to the user when price changes meet certain conditions (e.g., significant discount).

---

## 📦 Tech Stack

- **Python 3.12**
- **Fast API**
- **BeautifulSoup**
- **PostgreSQL**
- **Telegram Bot API**
- **React**
- **Tailwind**

---


---

## ⚙️ How It Works

**coming soon**

---

## 📥 Running Locally


1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/price-monitoring-agent.git
   cd price-monitoring-agent
    ```

2. **Create virtual environment and install dependencies**

To create the virtual environment, run ``` python -m venv .venv ```.

Then you need to activate it. 

- Windows users: ```.\.venv\Scripts\activate```
- Linux/Mac: ```source .venv/bin/activate```

Now you have to install the dependencies. Just run ```pip install -r requirements.txt```

4. **Set database url on .env file**

You might have noticed the database url is not being exposed.
To use your personal database url, create a file called .env just as it follows:

```
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/postgres"
```

You can configure the environments variables on the compose file. 

5. **Running Project**

Just run ```uvicorn app.main:app --reload``` and access on http://localhost:8000/. 
To read the documentation: http://localhost:8000/docs/.

## 📊 Sample Output

![telegram_chat](assets/telegram-output.png)

## 📌 Future Improvements
- Create Dockerfile 
- Add price prediction using historical data.
- Multi-product support.
- Deployment in the Cloud (Don't know which one yet)

## 🤖 Author
Developed by Lucas Berenger — feel free to connect or reach out!

v1.1.0