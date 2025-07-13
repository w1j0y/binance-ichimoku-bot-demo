#!/usr/bin/env python3
"""
Telegram Trading Bot Registration DEMO
--------------------------------------
- Self-hosted for trust: user must add their own bot token.
- Walks through the same steps as the real SaaS registration (username, email, keys, strategy, coin, amount).
- Simulates payment: prompts user to send /confirm to "activate" their bot (no real payment or deployment).
- At payment, explains how payment_checker and bot_deployer work in production.
- Outputs a config file that can be used for manual bot deployment (see README).
- NO actual trading, payment, or SaaS backend is included!
"""

import os
import time
import json
from pathlib import Path
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

# ====== CONFIGURATION ======
COIN_CHOICES = ["ETH", "BTC", "SOL", "AVAX", "NEAR"]
BOT_TOKEN = "PASTE_YOUR_OWN_TELEGRAM_BOT_TOKEN_HERE"  # <-- User must insert their own token here!
DATA_DIR = "./bot_requests"
os.makedirs(DATA_DIR, exist_ok=True)

FEE_TABLE = (
    "💸 *Demo Fees Table*\n"
    "  - $10 USDT for amounts < $1,000\n"
    "  - $20 USDT for $1,000 — $4,999\n"
    "  - $30 USDT for $5,000 — $9,999\n"
    "  - $50 USDT for $10,000+\n"
)

def sanitize_email(email):
    return email.replace('@', '_at_').replace('.', '_dot_')

def make_user_id(username, email):
    return f"{username}_{sanitize_email(email)}"

def strategy_explanation():
    return (
        "🤖 Welcome to the Trading Bot DEMO!\n\n"
        "This bot walks you through the full registration process for our automated crypto trading system.\n"
        "You can try the registration steps, including API key setup and strategy selection, safely on your own machine.\n\n"
        "⚠ *DEMO MODE ONLY!*\n"
        "- Payment and automated deployment are simulated.\n"
        "- Your API keys stay on your computer; nothing is sent externally.\n"
        "- For the SaaS version (with payment, cloud deploy, and support), contact @w1sj0y.\n"
        "- *Never share your API keys with anyone!*\n"
        "- Send /register to start the process"
    )

# Registration states
STATE_USERNAME, STATE_EMAIL, STATE_APIKEY, STATE_APISECRET, STATE_STRATEGY, STATE_COIN, STATE_AMOUNT = range(7)
user_sessions = {}  # chat_id: {'state': ..., 'data': ..., 'expires': ...}

def start_session(cid, state):
    user_sessions[cid] = {'state': state, 'data': {}, 'expires': time.time() + 300}

def expire_session(cid):
    if cid in user_sessions:
        del user_sessions[cid]

def session_expired(cid):
    if cid not in user_sessions:
        return True
    return time.time() > user_sessions[cid]['expires']

def session_update_expiry(cid):
    if cid in user_sessions:
        user_sessions[cid]['expires'] = time.time() + 300

async def start_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(strategy_explanation(), parse_mode="Markdown")

async def register_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    start_session(cid, STATE_USERNAME)
    await update.message.reply_text(
        "📝 Enter a username (3-20 letters/numbers/_):\n"
        "_For demo/testing only. You can use any name here._"
    )

async def reg_flow(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    if cid not in user_sessions or session_expired(cid):
        expire_session(cid)
        await update.message.reply_text(
            "⏰ Session expired. Send /register to start again."
        )
        return

    session_update_expiry(cid)
    step = user_sessions[cid]['state']
    data = user_sessions[cid]['data']
    text = update.message.text.strip()

    if step == STATE_USERNAME:
        if not (3 <= len(text) <= 20 and text.replace("_","").isalnum()):
            await update.message.reply_text("❌ Invalid username. Try again:")
            return
        data['username'] = text
        user_sessions[cid]['state'] = STATE_EMAIL
        await update.message.reply_text(
            "📧 Enter your email:\n"
            "_For demo/testing only. Any valid-looking email is OK._"
        )
    elif step == STATE_EMAIL:
        if "@" not in text or "." not in text:
            await update.message.reply_text("❌ Invalid email. Try again:")
            return
        data['email'] = text
        user_sessions[cid]['state'] = STATE_APIKEY
        await update.message.reply_text(
            "🔑 Enter your 64-character Binance API KEY:\n\n"
            "⚠️ *IMPORTANT: This must be a real API key from your Binance account.*\n"
            "- Enable only the **Read** permission (demo mode needs no trading/withdrawals)\n"
            "- Set IP to unrestricted (for demo on your machine)\n"
            "- DO NOT enable withdrawals!\n"
            "- If you get API errors later, check that your key is correct and has ‘Read’ enabled."
        )
    elif step == STATE_APIKEY:
        if len(text) != 64 or not text.isalnum():
            await update.message.reply_text("❌ Invalid API key. Try again:")
            return
        data['api_key'] = text
        user_sessions[cid]['state'] = STATE_APISECRET
        await update.message.reply_text(
            "🔏 Enter your 64-character Binance API SECRET:\n"
            "⚠️ *Must match your API KEY. Needed for demo to fetch prices.*"
        )
    elif step == STATE_APISECRET:
        if len(text) != 64 or not text.isalnum():
            await update.message.reply_text("❌ Invalid API secret. Try again:")
            return
        data['api_secret'] = text
        user_sessions[cid]['state'] = STATE_STRATEGY
        await update.message.reply_text(
            "📈 Choose strategy (send: ICHIMOKU):\n"
            "_For demo, only ICHIMOKU is supported._",
            reply_markup=ReplyKeyboardMarkup([["ICHIMOKU"]], one_time_keyboard=True)
        )
    elif step == STATE_STRATEGY:
        if text.upper() != "ICHIMOKU":
            await update.message.reply_text("❌ Only ICHIMOKU is available for the demo. Type ICHIMOKU:")
            return
        data['strategy'] = text.upper()
        user_sessions[cid]['state'] = STATE_COIN
        await update.message.reply_text(
            f"💱 Choose coin (send: {', '.join(COIN_CHOICES)}):\n"
            "_Any coin is fine for demo mode. Choose your favorite._",
            reply_markup=ReplyKeyboardMarkup([[c] for c in COIN_CHOICES], one_time_keyboard=True)
        )
    elif step == STATE_COIN:
        if text.upper() not in COIN_CHOICES:
            await update.message.reply_text(f"❌ Choose one of: {', '.join(COIN_CHOICES)}:")
            return
        data['coin'] = text.upper()
        user_sessions[cid]['state'] = STATE_AMOUNT
        await update.message.reply_text(
            "💵 Enter amount in USDT (≥ 50):\n"
            "_For demo/testing only—no real trades are executed, so you can use any value._\n\n"
            "This amount is just for testing the registration flow.\n\n"
            + FEE_TABLE,
            parse_mode="Markdown"
        )
    elif step == STATE_AMOUNT:
        try:
            amt = float(text)
            if amt < 50:
                raise ValueError
        except:
            await update.message.reply_text("❌ Enter a number ≥ 50:")
            return
        data['amount_usdt'] = amt

        user_id = make_user_id(data['username'], data['email'])
        data['user_id'] = user_id

        # Save config for manual deployment, skip payment
        user_json = {
            "username": data['username'],
            "email": data['email'],
            "api_key": data['api_key'],
            "api_secret": data['api_secret'],
            "strategy": data['strategy'],
            "coin": data['coin'],
            "amount_usdt": data['amount_usdt'],
            "user_id": user_id,
            "demo_mode": True,
        }
        Path(DATA_DIR, f"{user_id}.json").write_text(json.dumps(user_json))
        expire_session(cid)

        # 👉 Explanation of SaaS logic at the payment step:
        payment_window_message = (
            "💸 *Payment step is simulated in DEMO MODE.*\n\n"
            "🔒 In the real SaaS system, after entering your amount, a payment window is locked for 5 minutes.\n"
            "• The *payment_checker* bot monitors your payment during this window.\n"
            "• Once payment is confirmed, a `.signal` file is generated for your registration.\n"
            "• The *bot_deployer* continuously checks for this `.signal` file and, when found, it automatically deploys your personal trading bot instance for you.\n\n"
            "➡ In this DEMO, simply send /confirm to simulate payment and bot deployment."
        )
        await update.message.reply_text(
            payment_window_message,
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )
        user_sessions[cid] = {'state': "PAYMENT", 'data': data, 'expires': time.time() + 600}
    else:
        await update.message.reply_text("Invalid step. Use /register to restart.")

async def confirm_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    # Find last registered user config
    latest_json = None
    for fn in sorted(os.listdir(DATA_DIR), reverse=True):
        if fn.endswith(".json"):
            user_file = Path(DATA_DIR) / fn
            try:
                user_data = json.loads(user_file.read_text())
                if user_data.get("demo_mode") and user_data.get("user_id"):
                    latest_json = user_data
                    break
            except:
                continue
    if not latest_json:
        await update.message.reply_text("No registration found. Please /register first.")
        return

    await update.message.reply_text(
        "✅ Demo payment confirmed!\n\n"
        "If this were the SaaS system, your bot would be automatically deployed for you at this step.\n"
        f"In this DEMO, you can now manually deploy and run the trading bot using your config file "
        f"(`{DATA_DIR}/{latest_json['user_id']}.json`).\n\n"
        "See the README for instructions, and remember: *Never share your API keys!*"
    )

async def any_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    if cid not in user_sessions:
        await update.message.reply_text(strategy_explanation(), parse_mode="Markdown")
        await update.message.reply_text(
            "Send /register to start the registration demo."
        )
    else:
        await update.message.reply_text(
            "Please follow the registration prompts or use /register to reset."
        )

async def text_dispatcher(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    cid = update.effective_chat.id
    if cid in user_sessions:
        await reg_flow(update, ctx)
    else:
        await any_message(update, ctx)

def main():
    # User must insert their own Bot Token for testing.
    if "PASTE_YOUR_OWN_TELEGRAM_BOT_TOKEN_HERE" in BOT_TOKEN or not BOT_TOKEN or len(BOT_TOKEN) < 40:
        print("Please add your own Telegram bot token at the top of the script before running!")
        return 
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("register", register_cmd))
    app.add_handler(CommandHandler("confirm", confirm_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_dispatcher))
    app.add_handler(MessageHandler(filters.ALL, any_message))
    print("🤖 Telegram bot is running (DEMO MODE)…")
    app.run_polling()

if __name__ == "__main__":
    main()

