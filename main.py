import os
import requests
from dotenv import dotenv_values

# Load refresh token from .env
env = dotenv_values(".env")
refresh_token = env.get("QUESTRADE_REFRESH_TOKEN")
print("DEBUG: Loaded refresh token:", refresh_token)

# Authenticate to Questrade
def authenticate():
    url = "https://login.questrade.com/oauth2/token"
    params = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    print("DEBUG: Auth response:", data)

    return {
        "access_token": data["access_token"],
        "api_server": data["api_server"]
    }

# Use the authentication response
auth_data = authenticate()
access_token = auth_data["access_token"]
api_server = auth_data["api_server"]

print("✅ Authenticated with API Server:", api_server)
print("✅ Access Token:", access_token[:10] + "...")  # only show first part for safety

# 🔍 Get the symbol ID for a stock (e.g., "AAPL")
def get_symbol_id(symbol):
    url = f"{api_server}v1/symbols/search?prefix={symbol}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    symbols = response.json().get("symbols", [])

    for s in symbols:
        if s["symbol"] == symbol:
            print(f"✅ Found symbol ID for {symbol}: {s['symbolId']}")
            return s["symbolId"]

    raise Exception(f"❌ Symbol {symbol} not found.")

symbol_id = get_symbol_id("AAPL")

