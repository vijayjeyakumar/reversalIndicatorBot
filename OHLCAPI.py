import requests


def fetchOHLC(access_token, base_url, headers, instrument_key):
    ohlc_url = f"{base_url}/v2/market-quote/ohlc"

    # Define query parameters
    paramsOfOHLC = {
        "instrument_key": instrument_key,
        "interval": 'I1'
    }

    # Fetch data from Upstrox
    responseForOHLC = requests.get(ohlc_url, headers=headers, params=paramsOfOHLC)

    # Handle response for OHLC
    if responseForOHLC.status_code == 200:
        data = responseForOHLC.json()

    else:
        print(f"Error: {responseForOHLC.status_code}, Message: {responseForOHLC.text}")

    return data

