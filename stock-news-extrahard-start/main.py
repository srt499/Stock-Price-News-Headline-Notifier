import requests
from twilio.rest import Client
import datetime
import html

account_sid = 'ACea0544007d5b68ede2665c8a4f3c5c7b'
auth_token = '91c2df46d523ea16cc8e17fc052810b1'
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY = "T4TDS7ILCBGVYE50"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
parameters = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK,
    "apikey": API_KEY,
    "interval": "60min"
}

stock_response = requests.get("https://www.alphavantage.co/query", params=parameters)
stock_data = stock_response.json()

# Getting last 2 market close highs
yesterday = datetime.date.today() - datetime.timedelta(days=1)
yesterday_date_formatted = f"{yesterday.year}-{yesterday.month}-{yesterday.day} 20:00:00"
day_before = yesterday - datetime.timedelta(days=1)
day_before_date_formatted = f"{day_before.year}-{day_before.month}-{day_before.day} 16:00:00"

yesterdays_high = stock_data["Time Series (60min)"][yesterday_date_formatted]['2. high']
day_before_high = stock_data["Time Series (60min)"][day_before_date_formatted]['2. high']
print(yesterdays_high)
print(day_before_high)

perc_change = float(yesterdays_high) / float(day_before_high)
print(perc_change)

if perc_change < 0.99 or perc_change > 1.01:

    ## STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    news_response = requests.get(f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&from={yesterday}&to={day_before}&sortBy=popularity&apiKey=64586a80e1414e8f9da16ed75ee731e5")
    news_articles = news_response.json()['articles'][:3]

    # STEP 3: Use https://www.twilio.com
    # Send a seperate message with the percentage change and each article's title and description to your phone number.
    if perc_change < 1.00:
        stock_emblem = f"🔻{round((perc_change - 1) * 100, 2)}%"
    else:
        stock_emblem = f"🔺{round((1 - perc_change) * -100, 2)}"
    client = Client(account_sid, auth_token)
    for n in range(len(news_articles)):
        message = client.messages.create(body=f"{STOCK}: {stock_emblem}\n"
                                              f"Headline: {news_articles[n]['title']}\n"
                                              f"Brief: {news_articles[n]['description']}",
                                         from_='+12069446269',
                                         to='+15038878052'
                                         )


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
API Key = T4TDS7ILCBGVYE50"""

