import requests


def fetchFullMarketQuote(access_token, base_url, headers, instrument_key):
    fullMarketQuoteUrl = f"{base_url}/v2/market-quote/quotes"

    paramsOfFullMarketQuotes = {
        "instrument_key": instrument_key
    }
    # Fetch data from Upstrox
    responseForFullMarketQuotes = requests.get(fullMarketQuoteUrl, headers=headers, params=paramsOfFullMarketQuotes)

    # Handle response for Full MarketQuote
    if responseForFullMarketQuotes.status_code == 200:
        data = responseForFullMarketQuotes.json()
    else:
        print(f"Error: {responseForFullMarketQuotes.status_code}, Message: {responseForFullMarketQuotes.text}")
    return data
