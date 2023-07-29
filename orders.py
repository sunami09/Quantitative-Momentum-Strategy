from apikey import *
import json
import requests

# Define the endpoint URL
url = "https://paper-api.alpaca.markets/v2/orders"

# Define your headers
headers = {
    "APCA-API-KEY-ID": apiid,
    "APCA-API-SECRET-KEY": apisecret,
    "Content-Type": "application/json"
}

def order(symbol, shares, side):
    data = {
        "symbol": symbol,
        "qty": shares,
        "side": side,
        "type": "market",
        "time_in_force": "day"
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code != 200:
        print(f"Failed to {side} {symbol} shares")
        