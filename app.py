from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
import asyncio
import nest_asyncio
from flask import Flask
import threading

nest_asyncio.apply()

# بيانات البوت
TOKEN = "8027706435:AAF9Wdhshc3PLs7Vc5sN1njmeB4M9aIEVX8"
CHANNEL_ID = "@LAZARUS_OTP"
ADMIN_USERNAME = "@CKRACKING_MOROCCO"
VALID_KEYS = ["EXA7123", "VIPKEY000"]  # ضيف مفاتيح الاشتراك هنا

services = ["Netflix", "PayPal", "Bank", "Coinbase", "Spotify", "cvv", "pin", "crypto", "applepay", "amazon", "microsoft", "venmo", "cashapp", "quadpay"]
names = ["John", "Alice", "Mark", "Sophia", "Leo", "Emma", "Ahmed", "Amine", "Ahmed", "Jerry", "Salma", "William", "George", "Peris"]

# توليد OTP
def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

# رسالة /start
start_message = """
🚀 Welcome to Our Otp Bot 🚀

🔐 ➜ /redeem | Redeem your subscription
⏱ ➜ /plan | Check your subscription

📝  Custom Commands  📝
🧾 ➜ /createscript | Create custom scripts
🔏 ➜ /script [scriptid] | View script
🗣 ➜ /customcall | Call with script

📝 Calling Modules
📞 ➜ /call | Capture PayPal, CoinBase...
🏦 ➜ /bank | Capture OTP Bank
💳 ➜ /cvv | Capture CVV
🔢 ➜ /pin | Capture PIN
🍏 ➜ /applepay | Capture OTP Credit Card
🔵 ➜ /coinbase | Capture 2FA Code
💸 ➜ /crypto | Capture Crypto Code 
📦 ➜ /amazon | Approval Authentication
💻 ➜ /microsoft | Capture Microsoft Code
🅿️ ➜ /paypal | Capture Paypal Code
🏦 ➜ /venmo | Capture Venmo Code
💵 ➜ /cashapp | Capture Cashapp Code
💳 ➜ /quadpay | Capture quadpay Code
📟 ➜ /carrier | Capture carrier Code
📧 ➜ /email | grab Email code
🕖 ➜ /remind | remind victim

SET CUSTOM VOICE
🗣 ➜ /customvoice | Modify the TTS
❗️ ➜ EXAMPLE: /customvoice number spoof service name sid language

🔰  Purchase LAZARUS OTP  🔰
💎 Extras
◆ ⌨️ ⮞ /recall for re calling 
◆ ❓ ⮞ Do '?' on from number for instant random spoof number
"""

# الرد على /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Channel", url="https://t.me/LAZARUS_OTP")],
        [InlineKeyboardButton("🛒 Purchase", url="https://t.me/CKRACKING_MOROCCO")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(start_message, reply_markup=reply_markup)

# الرد على /plan
async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    plan_message = f"""
❌ You don't have any active subscription.

💰 Pricing Plans:
1️⃣ 1 Day: $20
2️⃣ 2 Days: $30
📅 1 Week: $55
🗓 2 Weeks: $70
🗓 1 Month: $100
📅 3 Months: $250
♾ Lifetime: $550

💬 Contact {ADMIN_USERNAME} to buy a subscription.
"""
    await update.message.reply_text(plan_message)

# الرد على /redeem
async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("📝 Please enter your subscription key.\nUsage: `/redeem your_key_here`", parse_mode="Markdown")
    else:
        key = args[0]
        if key in VALID_KEYS:
            await update.message.reply_text("✅ Key is valid! Your subscription has been activated.")
        else:
            await update.message.reply_text(f"❌ Invalid Key!\nPlease contact {ADMIN_USERNAME} for a valid one.", parse_mode="Markdown")

# إرسال رسائل عشوائية إلى القناة
async def send_random_message(bot: Bot):
    while True:
        service = random.choice(services)
        name = random.choice(names)
        otp = generate_otp()
        message = f"""🔐 OTP Alert!
👤 Name: {name}
🛠 Service: {service}
🔢 OTP: {otp}"""
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=message)
            print("Sent:", message)
        except Exception as e:
            print("Error:", e)
        await asyncio.sleep(random.randint(300, 900))

# Flask ل UptimeRobot
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot is running 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# تشغيل البوت
async def main():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    app_tg = ApplicationBuilder().token(TOKEN).build()

    app_tg.add_handler(CommandHandler("start", start))
    app_tg.add_handler(CommandHandler("plan", plan))
    app_tg.add_handler(CommandHandler("redeem", redeem))

    asyncio.create_task(send_random_message(app_tg.bot))

    print("Bot is running...")
    await app_tg.run_polling()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
