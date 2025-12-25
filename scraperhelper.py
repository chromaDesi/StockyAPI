from typing import Any
from bs4 import BeautifulSoup
import requests, random, time
import yfinance as yf

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
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 11; Mobile; rv:89.0) Gecko/89.0 Firefox/89.0"]

#google organizes its finance pages in a specific way, so we can scrape data directly from there
#where it goes stock ticker:exchange code
#example: AAPL:NASDAQ, V:NYSE
#scraped = requests.get(f"https://www.google.com/finance/quote/V:NYSE?hl={random.choice(language_codes)}", headers={"Accept-Language": random.choice(accept_languages)})
#exchangecode = input("Enter exchange code (e.g., NASDAQ, NYSE): ")
#ticker = input("Enter stock ticker symbol (e.g., AAPL, V): ")

def currency_rates() -> Any:
    url = f"https://dd.insiad.com/currency-rates"
    response = requests.get(url, headers={"Accept-Language": random.choice(headers), "User-Agent": random.choice(user_agents)}, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data for currency rates via Finviz")
    return response.json()

def scrape_finviz_detailed(ticker_symbol, pd: str = "d") -> Any:
    if pd.lower() not in ["d", "w", "m"]:
        raise ValueError("Invalid period. Use 'D' for daily, 'W' for weekly, or 'M' for monthly.")
    url = f"https://finviz.com/api/quote.ashx?aftermarket=0&dateFrom=1733029200&dateTo=1767243599&events=false&financialAttachments=&instrument=stock&patterns=false&premarket=0&rev=1766653078813&ticker={ticker_symbol}&timeframe={pd.lower()}"
    response = requests.get(url, headers={"Accept-Language": random.choice(headers), "User-Agent": random.choice(user_agents)}, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data for currency rates via Finviz")
    return response.json()


#<td class="snapshot-td2 w-[8%] " align="left" style=""><b>24.56</b></td>
def scrape_finviz_data(ticker_symbol, pd: str = "d") -> BeautifulSoup:
    if pd.lower() not in ["d", "w", "m"]:
        raise ValueError("Invalid period. Use 'D' for daily, 'W' for weekly, or 'M' for monthly.")
    url = f"https://finviz.com/quote.ashx?t={ticker_symbol}&ty=c&ta=1&p={pd.lower()}"
    response = requests.get(url, headers={"Accept-Language": random.choice(headers), "User-Agent": random.choice(user_agents)}, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data for {ticker_symbol} from Finviz")
    return BeautifulSoup(response.text, 'html.parser')


def scrape_google_stock_data(ticker_symbol, exchange_code, period: str = "1D") -> BeautifulSoup:
    url = f"https://www.google.com/finance/quote/{ticker_symbol}:{exchange_code}?window={period}"
    response = requests.get(url, headers={"Accept-Language": random.choice(headers), "User-Agent": random.choice(user_agents)}, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data for {ticker_symbol}:{exchange_code}")
    return BeautifulSoup(response.text, 'html.parser')

def getGoogleQuote(ticker_symbol: str, exchange_code: str, period: str = "1D") -> dict:
        if period not in ["1D", "5D", "1M", "6M", "YTD", "1Y", "5Y", "MAX"]:
            raise ValueError("Invalid period. Use one of: 1D, 5D, 1M, 6M, YTD, 1Y, 5Y, or MAX when using Google Services")
        soup = scrape_google_stock_data(ticker_symbol, exchange_code, period)
        currprice = soup.find_all('div', class_='fxKbKc')
        pe = soup.find_all('div', class_='P6K39c')
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

def getFinvizQuote(ticker_symbol: str, pd: str) -> dict:
    soup = scrape_finviz_data(ticker_symbol, pd)
    labels = soup.find_all('td', class_='snapshot-td2 cursor-pointer w-[7%]')
    data = soup.find_all('td', class_='snapshot-td2 w-[8%]')
    info = {}
    if not labels or not data or len(labels) != len(data):
        raise ValueError("Unexpected page structure from Finviz")
    for x, y in zip(labels, data):
        if x.text == "Trades":
            continue
        info[x.text] = y.text.strip()
    return info

def greed_index():
    response = requests.get("https://feargreedmeter.com/", headers={"Accept-Language": random.choice(headers), "User-Agent": random.choice(user_agents)}, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data for Greed Index")
    soup = BeautifulSoup(response.text, 'html.parser')
    num = soup.find_all('div', class_="text-center text-4xl font-semibold mb-1 text-white")
    words = {(0, 24) : "Extreme Fear", (25, 44) : "Fear",(45, 55) : "Neutral", (56, 75)  : "Greed", (76, 100) : "Extreme Greed"}
    marked_time = int(time.time())
    greed_value = int(num[0].text) if num else None
    if greed_value is None:
        raise ValueError("Unexpected page structure from Fear and Greed Meter")
    for (low, high), descriptor in words.items():
        if low <= greed_value <= high:
            return {"greed_index": greed_value, "status": descriptor, "timestamp": marked_time}


# Recursive function to handle nested comments
def parse_comments(comment_list, depth=0):
    if not comment_list:
        return

    for comment in comment_list:
        # 'kind' -> 't1' is a comment
        if comment['kind'] == 't1':
            c_data = comment['data']
            
            author = c_data.get('author', '[deleted]')
            body = c_data.get('body', '')
            score = c_data.get('score', 0)
            
            # Create indentation based on depth
            indent = "    " * depth
            prefix = "↳ " if depth > 0 else ""
            
            print(f"{indent}{prefix}User: {author} | Score: {score}")
            print(f"{indent}   {body}")
            print(f"{indent}" + "-" * 20)

            # CHECK FOR REPLIES (Recursion happens here)
            # Reddit sends an empty string "" if there are no replies. 
            # If there ARE replies, it sends a dictionary.
            replies = c_data.get('replies', '')
            if replies:
                # Dig down into the nested listing
                nested_children = replies['data']['children']
                parse_comments(nested_children, depth + 1)
                
        # 'kind' -> 'more' indicates more comments are hidden (pagination)
        elif comment['kind'] == 'more':
            indent = "    " * depth
            count = comment['data'].get('count', 0)
            print(f"{indent}>> [{count} more comments hidden...]")

def get_full_thread(url):
    if not url.endswith('.json'):
        url += '.json'

    headers = {"User-Agent": "RecursiveScraper/1.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Access the comment listing (Index 1)
        top_level_comments = data[1]['data']['children']
        
        print(f"--- Thread: {data[0]['data']['children'][0]['data']['title']} ---\n")
        
        # Start the recursion
        parse_comments(top_level_comments)

    except Exception as e:
        print(f"Error: {e}")

# Run it
'''
url = "https://www.reddit.com/r/gmu/comments/1pr49fl/found_out_i_passed/"
get_full_thread(url)'''

'''
print(getGoogleQuote("V", "NYSE"))
print("--------------New------------------")
print(getFinvizQuote("V", "d"))

print(getGoogleQuote("AAPL", "NASDAQ"))
print(yf.Ticker("AAPL").history(period="5d"))
print(yf.Ticker("AAPL").get_news(count = 1))'''
print(greed_index())