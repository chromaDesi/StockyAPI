from bs4 import BeautifulSoup
import requests, random

language_codes = ["en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko", "hi"]
headers = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.9",
    "en-CA,en;q=0.9",
    "en-AU,en;q=0.9",
    "en-NZ,en;q=0.9",
    "en-IN,en;q=0.9",
    "en-IE,en;q=0.9",
    "en-SG,en;q=0.9",
    "en-ZA,en;q=0.9",
    "en-PH,en;q=0.9"
]

#google organizes its finance pages in a specific way, so we can scrape data directly from there
#where it goes stock ticker:exchange code
#example: AAPL:NASDAQ, V:NYSE
#scraped = requests.get(f"https://www.google.com/finance/quote/V:NYSE?hl={random.choice(language_codes)}", headers={"Accept-Language": random.choice(accept_languages)})
#exchangecode = input("Enter exchange code (e.g., NASDAQ, NYSE): ")
#ticker = input("Enter stock ticker symbol (e.g., AAPL, V): ")


def scrape_stock_data(ticker_symbol, exchange_code) -> BeautifulSoup:
    url = f"https://www.google.com/finance/quote/{ticker_symbol}:{exchange_code}"
    response = requests.get(url, headers={"Accept-Language": random.choice(headers)}, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data for {ticker_symbol}:{exchange_code}")
    return BeautifulSoup(response.text, 'html.parser')

#<div class="YMlKec fxKbKc">$82.30</div>
    
def jsonWrapper(currprice, pe):
    if not currprice or len(pe) < 7:
        raise ValueError("Unexpected page structure from Google Finance")
    data = {
        "current_price": currprice[0].text,
        "pe_ratio": pe[0].text,
        "day_low": pe[1].text.split(" - ")[0][1:],
        "day_high": pe[1].text.split(" - ")[1][1:],
        "52_week_low": pe[2].text.split(" - ")[0][1:],
        "52_week_high": pe[2].text.split(" - ")[1][1:],
        "Market_cap": pe[3].text,
        "Avg_Volume": pe[4].text,
        "PE_Ratio": pe[5].text,
        "Dividend_yield": pe[6].text
    }
    return data
