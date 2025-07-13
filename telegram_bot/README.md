# Trading Bot Registration Demo (Telegram Version)

Welcome to the **transparent, demo-only** version of the Trading Bot registration system.  
This project lets you experience the **real user onboarding flow** for our trading bot SaaS—on your own Telegram account, on your own computer, with your own Binance API keys (kept strictly local).

---

## 🚦 Features

- **Full SaaS-like registration flow:** username, email, API key/secret, strategy (Ichimoku), coin, and USDT amount.
- **Payment is simulated:** no actual payment required, just send `/confirm` at the end to finish.
- **Safe for self-hosted demo:** all API keys/config stay on your machine; nothing is uploaded or sent elsewhere.
- **Outputs a user config file** for use with the trading bot demo script (`coin_ichimoku_template_demo.py`).

---

## ⚠ IMPORTANT – DEMO MODE ONLY

- There is **NO live trading** and **NO automated deployment** in this demo.
- Your API keys are never sent outside your computer.
- **Never share your API keys with anyone, including this repo’s maintainer!**
- This demo is for testing, transparency, and trust-building. For production/live trading, use the SaaS version or review all code yourself.

---

## 🔧 How To Install & Use (Linux, Windows, Mac)

### 1. Prepare System & Dependencies

**For Linux/Ubuntu/Kali, run:**

    sudo apt update
    sudo apt install libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git -y

**If Python 3.11 is not already installed, compile it from source:**

    cd /usr/src
    sudo wget https://www.python.org/ftp/python/3.11.8/Python-3.11.8.tgz
    sudo tar xzf Python-3.11.8.tgz
    cd Python-3.11.8
    sudo ./configure --enable-optimizations --with-ensurepip=install
    sudo make altinstall

This will install `/usr/local/bin/python3.11` with pip and venv support.

**Create and activate a virtual environment:**

    /usr/local/bin/python3.11 -m venv telegram_venv
    source telegram_venv/bin/activate

**Install Python libraries:**

    pip install python-telegram-bot==20.7

**For Windows/Mac:**  
Download Python 3.11.x from [python.org](https://www.python.org/downloads/)  
Create a virtual environment, and install `python-telegram-bot==20.7` with pip as usual.

---

### 2. Set Up Your Telegram Bot

1. Go to [@BotFather](https://t.me/botfather) on Telegram, create a new bot, and copy the Bot Token.
2. Download this repository (clone or download ZIP).
3. Open `telegram_bot_demo.py` in any text editor.  
   Paste your Telegram Bot Token at the line:
       BOT_TOKEN = "PASTE_YOUR_OWN_TELEGRAM_BOT_TOKEN_HERE"

---

### 3. Run the Demo Bot

    python telegram_bot_demo.py

You should see:  
    🤖 Telegram bot is running (DEMO MODE)…

---

### 4. Test the Registration Flow

- Open Telegram, find your new bot, and start a chat.
- Send `/start` then `/register`.
- Follow all prompts: username, email, Binance API key/secret, strategy (**only Ichimoku is available for demo**), coin, and amount.
- When asked for payment, just send `/confirm` (no payment is needed).
- Your config file (e.g., `yourusername_email_dot_com.json`) will be saved in the `./bot_requests/` folder.

---

### 🚀 After Registration: How to Run Your Demo Bot

At the end of registration, your config file (e.g., `yourusername_email_dot_com.json`) will be saved in the `./bot_requests/` folder.

- Use the demo script:

        coin_ichimoku_template_demo.py

- **Supported coins:** BTC, ETH, SOL, AVAX, NEAR

In your script, set the path to your config file:

        CONFIG_FILE = "bot_requests/yourusername_email_dot_com.json"

Then run the demo script:

        python coin_ichimoku_template_demo.py

> ⚡️ **Note:** Only the Ichimoku strategy demo is currently available.  
> The DCA demo script will be provided in a future update.

---

## 🔑 API Key Requirements & Security

For the demo bot to fetch live price data and compute signals, you will need to create a Binance API key and secret.  
**These are used ONLY to read market data. No trades will ever be placed in demo mode.**

**API key settings for demo use:**
- **Enable "Read" permission** (required for price data and indicators)
- **Do NOT enable "Spot & Margin Trading"** (unless you want live trading—demo only needs read access)
- **DO NOT enable withdrawals** (never needed, even for SaaS version)
- **Set IP access to Unrestricted** (for demo/testing on your own machine; restrict as needed for your own security)

> Your API keys are stored only on your own computer and are never sent or uploaded anywhere.

**Security Reminder:**
- Never share your API keys with anyone—including the repo owner or maintainers.
- Always review permissions before creating or reusing an API key.
- You can delete or reset your API keys at any time from your Binance account.

---

## 📝 Frequently Asked Questions

**Q: Does this demo send or store my API keys anywhere?**  
A: No. Your keys and config files are stored **only on your computer** and used only by the bot you run locally.

**Q: How do I use this for live trading?**  
A: This repo is for demo/testing only. For live, cloud-deployed bots with SaaS features, please [contact @w1sj0y on Telegram](https://t.me/w1sj0y).

**Q: What’s the difference between this and the SaaS version?**  
A: SaaS includes:  
    - Real payment & automated user management  
    - Bot deployment & monitoring  
    - Professional email notifications  
    - Error handling & 24/7 uptime  
    - Multi-coin support  
    - Weekly profit/loss reports  
    - Priority support

**Q: Can I see how the real SaaS system works?**  
A: Yes! Check our [video walkthrough](#demo-video) to see all features in action.

---

## 💬 Support & Upgrade

For questions, feedback, or to unlock full SaaS features:
- [Open an issue on GitHub](https://github.com/your-repo)
- [Message @w1sj0y on Telegram](https://t.me/w1sj0y)

---

## ⚠ Security Reminder

- **NEVER** share your real Binance API keys with anyone, including this repo's maintainer.
- Only enable API permissions you need (read and trading only, NO withdrawals).
- Always review and test scripts before using real funds.

---

## 📜 License

This repository is provided for **demo and educational use only**.  
No commercial or production use is permitted without explicit permission.

---

## 🚀 Deploying Your Trading Bot in Demo Mode

In the full SaaS system, your bot would be automatically deployed and managed in the cloud after payment confirmation.

**In this demo, deployment is done manually:**
1. Complete the registration process with the Telegram demo bot and confirm.
2. A configuration file with your registration details will be saved in the `./bot_requests/` folder.
3. Use this file as input for the provided trading bot demo script (`coin_ichimoku_template_demo.py`).
4. Start the demo trading bot manually on your own machine following the instructions in its README section.

> ⚠ **Note:**  
> No bots are deployed automatically in the demo. All trading (and API key usage) happens locally, under your control.

---

## 🏃♂ QUICK SUMMARY: ALL INSTALL/USAGE COMMANDS

    # Install all dependencies and libraries
    sudo apt update && sudo apt install libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git -y

    # Download, compile, and install Python 3.11 with pip/venv support
    cd /usr/src
    sudo wget https://www.python.org/ftp/python/3.11.8/Python-3.11.8.tgz
    sudo tar xzf Python-3.11.8.tgz
    cd Python-3.11.8
    sudo ./configure --enable-optimizations --with-ensurepip=install
    sudo make altinstall

    # Create & activate virtual environment
    /usr/local/bin/python3.11 -m venv telegram_venv
    source telegram_venv/bin/activate

    # Install python-telegram-bot library
    pip install python-telegram-bot==20.7

    # Add your bot token to telegram_bot_demo.py, then:
    python telegram_bot_demo.py

---

## 🎥 Demo Video

A full walkthrough showing all features will be available soon!  
[**Watch the demo here (YouTube link coming soon)**]

---

