# Trading Bot Demo Template (Signal-Only Version)

This project provides a **safe, transparent demo** of the trading bot’s signal logic.  
No real trades are placed—use it to evaluate, audit, and test the strategies with your own Binance API keys (kept strictly local).

---

## 🚀 Quick Start Setup

**1. Install Python and System Requirements**

- Make sure Python 3.8+ is installed (works on Linux, Mac, and Windows).
- For Linux/Kali/Ubuntu, first install system dependencies:
    
        sudo apt update
        sudo apt install python3 python3-pip python3-venv

**2. Create & Activate a Virtual Environment (Recommended)**

- In your bot template folder, run:

        python3 -m venv bot_venv
        source bot_venv/bin/activate         # On Windows: bot_venv\Scripts\activate

**3. Install Required Python Libraries**

        pip install python-binance pandas

---

## 🚦 Two Ways to Try the Demo Bot

You can use the demo bot via either of these options:

---

### Option 1: Use the Telegram Demo Bot (Recommended)

1. **Register with the Telegram demo bot** to generate a config file with your API key, coin, and strategy.
2. **Find your config file** in the `./bot_requests/` directory after you complete `/register` and `/confirm` in Telegram.
3. **Set the `CONFIG_FILE` variable** in the demo script to point to your generated file:

        CONFIG_FILE = "bot_requests/yourusername_email_dot_com.json"

4. **Run the demo bot.**  
   Your trade signals will be logged locally—no trades will be executed.

---

### Option 2: Manual Setup (Quick Start)

1. **Edit the demo bot script directly.**
2. **Define your `user_config` dictionary** at the top of the script (see example below).
3. **No config file or Telegram registration needed!**

        user_config = {
            # These fields are for logging/completeness. For demo mode, they do not affect anything.
            "username": "anything",          # can be anything for demo
            "email": "demo@email.com",       # can be anything for demo
            "amount_usdt": 100,              # any positive number; no real trading
            "strategy": "ICHIMOKU",          # only ICHIMOKU is supported in demo

            # These MUST be valid to fetch price data:
            "api_key": "YOUR_API_KEY",       # must be a real Binance API key with 'Read' enabled
            "api_secret": "YOUR_API_SECRET", # must match above

            "coin": "BTC"                    # Supported: BTC, ETH, SOL, AVAX, NEAR
        }

**⚠️ Only the `api_key` and `api_secret` must be correct for demo mode!**  
If these are wrong or missing permissions, the script will show API errors in the log.

---

## 🛠 API Key Requirements & Security

To fetch live price data and generate signals, you need a Binance API key and secret.

**API key settings for demo use:**
- **Enable only "Read" permission** (needed to fetch price data)
- **DO NOT enable withdrawals** (never needed—even for live trading)
- **No need to enable "Spot & Margin Trading"** for demo; only "Read" is required
- **Set IP access to Unrestricted** (for demo/testing on your own machine; restrict if you wish for extra safety)

> Your API keys are stored only on your own computer and never sent or uploaded anywhere.

**Security Reminder:**
- Never share your API keys with anyone—including this repo's maintainer.
- Always review and reset/delete API keys from your Binance account as needed.

---

## 🚨 Troubleshooting

- If you see any **API errors** in your bot log, it almost always means your API key/secret are incorrect, or **the API key is missing 'Read' permission** in the Binance dashboard.
- Double-check that you have enabled 'Read' access, that your keys are entered correctly, and that you’ve copied them from the correct Binance account.

---

## ❗ Demo Limitations

- The demo bot **never places real trades**—it only prints and logs trade signals for your review.
- Your API keys are used for data fetching only, and nothing leaves your machine.

---

## 📁 Using Your Config File with the Demo Bot

If you use the Telegram demo bot, after sending `/confirm`, a config file will be created for you in the `./bot_requests/` directory.  
This file contains all the necessary information for the demo trading bot script.

**Typical file location:**  
    ./bot_requests/yourusername_email_dot_com.json

**How to use it:**
1. Note the exact path and filename for your config JSON.
2. In your demo bot script (e.g., `coin_ichimoku_template_demo.py`), set the `CONFIG_FILE` variable accordingly:

        CONFIG_FILE = "bot_requests/yourusername_email_dot_com.json"

3. Run the script to evaluate signals and bot logic.  
   No trades will be executed—signals are printed to your screen and saved to a log file.

---

### 📝 Example Config File

Your config file might look like:

        {
          "username": "btcuser",
          "email": "btcuser@gmail.com",
          "api_key": "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6A7B8C9D0E1F2",
          "api_secret": "F2E1D0C9B8A7Z6Y5X4W3V2U1T0S9R8Q7P6O5N4M3L2K1J0I9H8G7F6E5D4C3B2A1",
          "strategy": "ICHIMOKU",
          "coin": "BTC",
          "amount_usdt": 100,
          "user_id": "btcuser_btcuser_at_gmail_dot_com",
          "demo_mode": true
        }

---

### 📄 How the Config is Referenced in the Demo Bot

In the demo trading bot script, your config is loaded like this:

        import json

        CONFIG_FILE = "bot_requests/yourusername_email_dot_com.json"  # <- Set to your config filename

        with open(CONFIG_FILE) as f:
            user_config = json.load(f)

        # Use values from user_config in your script
        symbol            = user_config.get("coin", "BTC") + "USDT"
        trade_amount_usdt = float(user_config.get("amount_usdt", 100))
        api_key           = user_config.get("api_key")
        api_secret        = user_config.get("api_secret")
        # ...etc.

---

## 📝 Pro Tips

- **Manual setup** is fast and flexible for quick testing or sharing with others.
- **Telegram demo** lets you experience the full SaaS-style onboarding flow.

---

## ⚠ Security Reminder

- **NEVER** share your real Binance API keys with anyone, including this repo's maintainer.
- Only enable API permissions you need (read-only for demo; never withdrawals).
- Always review and test scripts before using real funds or keys.

---

## 📜 License

This repository is provided for **demo and educational use only**.  
No commercial or production use is permitted without explicit permission.

---

