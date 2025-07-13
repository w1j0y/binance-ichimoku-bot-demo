#!/usr/bin/env python3
"""
BTC Ichimoku Strategy Demo Bot (SIGNAL-ONLY VERSION)
====================================================
This script will NOT place any real orders and will NOT execute trades.
It is provided so users can audit, test, and review the actual signal logic
used by the SaaS bot—without risk, for transparency and trust.

- Option 1: Reads config from the user registration JSON (created via Telegram bot).
- Option 2: Manual config — just edit the fields below (no JSON required).
- Fetches live 1-hour BTC/USDT price data via Binance API (for signal logic only).
- Prints/logs when BUY, SELL, or HOLD signals would be triggered according to strategy.
- NO order execution, NO API trading permissions required!
- Use for demo/evaluation only.

Copyright (c) 2025
"""

import os
import time
import logging
import json
import pandas as pd
from datetime import datetime
from binance.client import Client

# === CONFIGURATION ===

USE_MANUAL_CONFIG = False  # Set to True to use manual config below, False to load from config JSON

# ----- Option 2: MANUAL CONFIG (edit these values directly) -----
user_config = {
    "username": "yourname",
    "email": "your@email.com",
    "api_key": "YOUR_API_KEY",
    "api_secret": "YOUR_API_SECRET",
    "strategy": "ICHIMOKU",
    "coin": "BTC",             # e.g. BTC or ETH (no USDT here)
    "amount_usdt": 100,
    "demo_mode": True,
}

# ----- Option 1: LOAD FROM JSON FILE (Telegram bot method) -----
CONFIG_FILE = "./bot_requests/demo_demo_at_email_dot_com.json"  # Edit this if not using manual config and include full path for .json file

# === CONFIG LOAD LOGIC ===
def get_config():
    if USE_MANUAL_CONFIG:
        # Check if user_config is filled properly
        required = ["username", "email", "api_key", "api_secret", "strategy", "coin", "amount_usdt"]
        for field in required:
            if not user_config.get(field):
                print(f"[CONFIG ERROR] Please fill in '{field}' in the manual user_config at the top of the script.")
                exit(1)
        return user_config
    else:
        if not os.path.exists(CONFIG_FILE):
            raise FileNotFoundError(
                f"Config file {CONFIG_FILE} not found.\n"
                "After registering with the Telegram demo bot, copy your config JSON to this path, "
                "or set USE_MANUAL_CONFIG = True to use manual config."
            )
        with open(CONFIG_FILE) as f:
            loaded = json.load(f)
        # Check for fields
        required = ["username", "email", "api_key", "api_secret", "strategy", "coin", "amount_usdt"]
        for field in required:
            if not loaded.get(field):
                print(f"[CONFIG ERROR] Field '{field}' is missing in your JSON file {CONFIG_FILE}.")
                exit(1)
        return loaded

user = get_config()

symbol            = user.get("coin", "BTC").upper() + "USDT"
interval          = Client.KLINE_INTERVAL_1HOUR
trade_amount_usdt = float(user.get("amount_usdt", 100))
api_key           = user.get("api_key")
api_secret        = user.get("api_secret")

client = Client(api_key, api_secret)

data_dir = "demo_bot_data"
os.makedirs(data_dir, exist_ok=True)
botlog_file = os.path.join(data_dir, f"{symbol.lower()}_ichimoku_signals.log")

# === LOGGING ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(botlog_file)
    ]
)

logging.warning("*********** DEMO MODE: NO TRADES WILL BE EXECUTED ***********")
logging.warning("This script will only print/log signals for transparency/testing.")
logging.warning("If you see a 'BUY' or 'SELL' signal, it's for demonstration purposes only.")

# === Ichimoku Calculation (unchanged) ===
def calculate_ichimoku(df):
    high_9 = df['high'].rolling(window=9).max()
    low_9 = df['low'].rolling(window=9).min()
    tenkan = (high_9 + low_9) / 2

    high_26 = df['high'].rolling(window=26).max()
    low_26 = df['low'].rolling(window=26).min()
    kijun = (high_26 + low_26) / 2

    span_a = ((tenkan + kijun) / 2).shift(26)
    high_52 = df['high'].rolling(window=52).max()
    low_52 = df['low'].rolling(window=52).min()
    span_b = ((high_52 + low_52) / 2).shift(26)
    chikou = df['close'].shift(-26)

    return tenkan, kijun, span_a, span_b, chikou

# === Get Data ===
def get_klines():
    klines = client.get_klines(symbol=symbol, interval=interval, limit=100)
    df = pd.DataFrame(klines, columns=[
        'open_time','open','high','low','close','volume',
        'close_time','qav','num_trades','tbbav','tbqav','ignore'
    ])
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    return df

# === Main Signal Logic ===
def check_signals(df):
    tenkan, kijun, span_a, span_b, chikou = calculate_ichimoku(df)
    close = df['close']
    price = close.iloc[-2]
    signals = []

    # TK Cross
    if tenkan.iloc[-2] > kijun.iloc[-2]:
        signals.append('tk_bullish')
        logging.info("✔ Tenkan > Kijun (Bullish TK Cross)")
    elif tenkan.iloc[-2] < kijun.iloc[-2]:
        signals.append('tk_bearish')
        logging.info("✔ Tenkan < Kijun (Bearish TK Cross)")
    else:
        logging.info("✘ No TK Cross")

    # Kumo Breakout
    if price > span_a.iloc[-2] and price > span_b.iloc[-2]:
        signals.append('kumo_bullish')
        logging.info("✔ Price above Span A and B (Bullish Kumo Breakout)")
    elif price < span_a.iloc[-2] and price < span_b.iloc[-2]:
        signals.append('kumo_bearish')
        logging.info("✔ Price below Span A and B (Bearish Kumo Breakout)")
    else:
        logging.info("✘ No Kumo Breakout")

    # Kijun Cross
    if price > kijun.iloc[-2]:
        signals.append('kijun_bullish')
        logging.info("✔ Price > Kijun (Bullish Kijun Cross)")
    elif price < kijun.iloc[-2]:
        signals.append('kijun_bearish')
        logging.info("✔ Price < Kijun (Bearish Kijun Cross)")
    else:
        logging.info("✘ No Kijun Cross")

    # Chikou Breakout (add logging here)
    try:
        if chikou.iloc[-2] > df['close'].iloc[-28]:
            signals.append('chikou_bullish')
            logging.info("✔ Chikou > Price 26 periods ago (Bullish Chikou Breakout)")
        elif chikou.iloc[-2] < df['close'].iloc[-28]:
            signals.append('chikou_bearish')
            logging.info("✔ Chikou < Price 26 periods ago (Bearish Chikou Breakout)")
        else:
            logging.info("✘ No Chikou Breakout")
    except IndexError:
        logging.warning("⚠ Not enough data for Chikou check")

    # Kumo Twist (add logging here)
    if span_a.iloc[-1] > span_b.iloc[-1] and span_a.iloc[-2] <= span_b.iloc[-2]:
        signals.append('twist_bullish')
        logging.info("✔ Bullish Kumo Twist")
    elif span_a.iloc[-1] < span_b.iloc[-1] and span_a.iloc[-2] >= span_b.iloc[-2]:
        signals.append('twist_bearish')
        logging.info("✔ Bearish Kumo Twist")
    else:
        logging.info("✘ No Kumo Twist")

    return signals

# === Main Loop ===
def main():
    print("\n*********** DEMO MODE: NO TRADES WILL BE EXECUTED ***********")
    print("This script ONLY prints/logs signals for transparency/testing.")
    print("If you see a 'BUY' or 'SELL' signal, it is NOT an actual order.\n")

    print(f"🚀 Starting Ichimoku DEMO Signal Bot for {symbol}...")
    print(f"{'Using manual config.' if USE_MANUAL_CONFIG else f'Reading config from: {CONFIG_FILE}'}")
    print(f"Signals will be printed here and also saved in: {botlog_file}\n")

    state = 'NONE'  # last action: 'BUY', 'SELL', or 'NONE'

    while True:
        try:
            df = get_klines()
            price = df['close'].iloc[-1]
            signals = check_signals(df)
            bullish = sum(1 for s in signals if 'bullish' in s)
            bearish = sum(1 for s in signals if 'bearish' in s)

            logging.info(f"📈 Current Price: {price:.2f}")
            logging.info(f"📊 Signals: {signals}")
            logging.info(f"✔ Bullish: {bullish} | ❌ Bearish: {bearish} | 🕓 Last action: {state}")

            # Demo logic: Print what would happen, but do NOT trade!
            if state in ['SELL', 'NONE']:
                if bullish >= 3:
                    logging.info(f"🚦 DEMO SIGNAL: [BUY] Would trigger BUY at {price:.2f} (if live)")
                    state = 'BUY'
                else:
                    logging.info(f"🤝 DEMO SIGNAL: [HOLD] No buy, not enough bullish signals ({bullish}/3).")
            elif state == 'BUY':
                if bearish >= 3:
                    logging.info(f"🚦 DEMO SIGNAL: [SELL] Would trigger SELL at {price:.2f} (if live)")
                    state = 'SELL'
                else:
                    logging.info(f"🤝 DEMO SIGNAL: [HOLD] No sell, not enough bearish signals ({bearish}/3).")

            print("---")
            time.sleep(60*60)  # Wait 1 hour (match 1h timeframe)
        except Exception as e:
            logging.error(f"Main loop error: {e}")
            time.sleep(60)

if __name__ == '__main__':
    main()

