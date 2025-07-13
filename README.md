# Binance Ichimoku Trading Bot Demo (Signal-Only)

This repository provides a **fully transparent demo** of a Binance trading bot based on the Ichimoku strategy with a strict 3-signal confirmation system.  
No real trades are executed—this is for safe testing, learning, and auditing the exact logic that powers the live SaaS bot.

---

## 📊 How Does the Ichimoku Bot Decide to Trade?

The bot uses the Ichimoku indicator and will **enter a simulated BUY or SELL** only if **3 or more of the following confirmations** are present on the current hourly candle:

1. **TK Cross**: Tenkan crosses above (bullish) or below (bearish) Kijun.
2. **Kumo Breakout**: Price is above (bullish) or below (bearish) both cloud lines (Span A and Span B).
3. **Kijun Confirmation**: Price is above (bullish) or below (bearish) the Kijun line.
4. **Chikou Breakout**: Chikou span is above (bullish) or below (bearish) the price 26 periods ago.
5. **Kumo Twist**: Span A crosses above (bullish) or below (bearish) Span B.

**Only when 3 or more bullish (or bearish) confirmations occur simultaneously does the bot signal a trade.**  
All logic is fully visible in the template script logs.

---

## 🚀 How to Use

You have two ways to try the demo bot:

### **Option 1: Telegram Registration (Recommended)**

- Deploy the `telegram_bot_demo.py` bot in the `telegram_bot` folder.
- Complete the full onboarding in Telegram—this creates a config `.json` file for you.
- Use that config file in the `coin_ichimoku_template_demo.py` script to see real-time signals, following the full SaaS logic and onboarding flow.

*(See `telegram_bot/README.md` and `bot_templates/README.md` for setup details.)*

---

### **Option 2: Manual Quickstart**

- Go directly to `bot_templates/coin_ichimoku_template_demo.py`.
- Manually fill the required fields at the top of the script:
  - API key and secret (read-only, required for live data)
  - Coin, username, email, and amount—these do **not** affect demo trading, but must be present.
- Run the script to view live hourly trading signals and all logic in the terminal/log file.

No Telegram registration or config file required for this mode.

---

## 📂 Folder Structure

- `telegram_bot/` – Telegram registration demo bot & setup instructions
- `bot_templates/` – Demo trading bot template and its own README
- `bot_requests/` – Stores config files created by the Telegram bot

---

## 🛡️ Safety & Security

- **No real trades are ever executed.**
- Your Binance API keys are used for *reading* data only—never for trading or withdrawals.
- You can inspect and audit every line of code before use.
- If you see any API error in the log, double-check your API permissions (“Enable Reading”).

---

For step-by-step setup and troubleshooting, see the README files in each subfolder.

---

**Happy (safe) trading! 🚦**

## ❓ Frequently Asked Questions (FAQ)

**What is this project?**  
This repository contains a demo version of a Binance trading bot using the Ichimoku strategy. The demo does **not** place real trades; it only shows you (via logs) when a real bot would buy or sell, so you can fully audit its behavior before considering live trading.

---

**How can I trust this bot?**  
- All logic is open and visible—feel free to inspect the code line-by-line.
- There’s a [live demo video](https://youtu.be/_DzWgm3HBIY) on YouTube showing the entire SaaS flow (Telegram, payment, bot deployment).
- No real funds are touched in demo mode.

---

**Is it safe to share my API keys?**  
For the demo, you don’t need real API keys—use sample data only.  
For the full SaaS service, keys are never given withdrawal permissions and are securely stored on a hardened VPS (see the [Medium post]() for more details).

---

**How does the trading logic work?**  
- The bot analyzes five Ichimoku signals every hour on the 1-hour chart.
- If **3 or more bullish signals**: logs a "would BUY" action.
- If **3 or more bearish signals**: logs a "would SELL" action.
- Check Medium post for more details https://medium.com/@wissammhfz77/binance-ichimoku-trading-bot-frequently-asked-questions-47a15197fbb5

---

**Can I run this bot myself?**  
Yes! This repo includes a standalone demo that you can run locally.  

---

**Which coins are supported?**  
Demo and live versions support BTC, ETH, AVAX, NEAR, and SOL.  
The logic is easily adaptable to other spot pairs.

---

**Can I use this bot for real trading?**  
This repo is **signal/demo only** for safety.  
For the full version (live spot trading, Telegram integration, email alerts), contact me via [Telegram](https://t.me/w1sj0y) or see the [Medium article](https://medium.com/@wissammhfz77/binance-ichimoku-trading-bot-frequently-asked-questions-47a15197fbb5).

---

**What if I want to run multiple bots?**  
Demo version: Run multiple scripts with different settings.  
Full SaaS: One bot per Telegram account for now. Contact if you need multi-bot support.

---

**Why is there no futures trading bot?**  
This project is designed for spot trading only, for lower risk and to encourage sustainable growth.  
Futures trading is higher risk and not supported here.

---

**Who are you?**  
I'm a penetration tester and crypto investor since 2017.  
Credentials: CPTS & CBBH certified.  
My goal: automate a disciplined, transparent strategy (not hype or get-rich-quick schemes).

---

**Where can I see a live demo or learn more?**  
- [Live Demo Video](https://youtu.be/_DzWgm3HBIY)  
- [Medium FAQ & Security Details](https://medium.com/@wissammhfz77/binance-ichimoku-trading-bot-frequently-asked-questions-47a15197fbb5)  
- [Telegram Contact](https://t.me/w1sj0y)

---

*For bugs, suggestions, or business inquiries, open an issue or reach out on Telegram.*

---

