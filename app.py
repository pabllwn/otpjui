from flask import Flask
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
import asyncio
import nest_asyncio
from threading import Thread
import os  # ضروري باش نستعمل متغير PORT

nest_asyncio.apply()

# Flask App
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running!"

# Telegram Bot Config
TOKEN = "8027706435:AAG9y4UGSl9Ha4pdqc7ZmLEK6ETTKxMsD7A"
CHANNEL_ID = "@LAZARUS_OTP"
ADMIN_USERNAME = "@CKRACKING_MOROCCO"
VALID_KEYS = ["TRIYAL-1234", "DEMLO-9999"]

services = [
    "Netflix", "PayPal", "Bank", "Coinbase", "Spotify", "Cvv", "Pin", "Crypto",
    "Apple Pay", "Amazon", "Microsoft", "Venmo", "Cashapp", "Quadpay", "Bank Of America"
]

names = [
    "John", "Alice", "Mark", "Sophia", "Leo", "Emma", "Ahmed", "Amine",
    "Ahmed", "Jerry", "Salma", "William", "George", "Periz", "Nouh", "John", "Thomas", "Eric", "Mike"
]

user_subscriptions = {}

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
⌨️ /recall for re-calling
❓ Use `?` in number to spoof random number
"""

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Channel", url="https://t.me/LAZARUS_OTP")],
        [InlineKeyboardButton("🛒 Purchase", url=f"https://t.me/{ADMIN_USERNAME.lstrip('@')}")]
    ]
    await update.message.reply_text(start_message, reply_markup=InlineKeyboardMarkup(keyboard))

async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
LAZARUS-O-T-P CALL ☎️ 🌐
With a very good prices: 

💵 1 Day : $20
💵 2 Days : $30
💵 1 Week : $55
💵 2 Weeks : $70
💵 1 Month : $100
💵 3 Months : $250
💵 Lifetime : $550

DM @CKRACKING_MOROCCO to get your key 🗝  
🤖 BOT: @lazzaruss_bot  
✉️ Support: @CKRACKING_MOROCCO
""")

async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if not args:
        await update.message.reply_text("🔑 Please send a key like this: `/redeem YOUR_KEY`", parse_mode="Markdown")
        return

    key = args[0].strip()
    if key in VALID_KEYS:
        user_subscriptions[user_id] = True
        await update.message.reply_text("✅ Key accepted! Subscription activated.")
    else:
        await update.message.reply_text(f"❌ Invalid key.\nPlease contact {ADMIN_USERNAME} to purchase a valid one.")

# إرسال رسائل عشوائية للقناة
async def send_random_message(bot: Bot):
    while True:
        service = random.choice(services)
        name = random.choice(names)
        otp = generate_otp()
        message = f"🔐 OTP Alert!\n👤 Name: {name}\n🛠 Service: {service}\n🔢 OTP: {otp}"
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=message)
            print("✔️ Sent:", message)
        except Exception as e:
            print("❌ Error:", e)
        await asyncio.sleep(random.randint(300, 900))

# تشغيل البوت
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("plan", plan))
    app.add_handler(CommandHandler("redeem", redeem))

    asyncio.create_task(send_random_message(app.bot))

    print("🤖 Bot is running...")
    await app.run_polling()

# تشغيل Flask والسيرفر (بمنفذ متوافق مع Render)
def run_flask():
    port = int(os.environ.get("PORT", 5000))  # استخدام المنفذ من البيئة
    flask_app.run(host="0.0.0.0", port=port)

if __name__ == '__main__':
    Thread(target=run_flask).start()
    asyncio.get_event_loop().run_until_complete(main())
