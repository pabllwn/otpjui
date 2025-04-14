from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
import asyncio
import nest_asyncio
import os

# تعديل: تطبيق Nest Asyncio بعد استيراد المكتبات الأساسية
nest_asyncio.apply()

# إعداد Flask
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return "Bot is alive!"

# معلومات البوت
TOKEN = "8027706435:AAH36GpgqPFQPX7sDFhgjkbSemLVQkK1Qqw"
CHANNEL_ID = "@LAZARUS_OTP"
ADMIN_USERNAME = "@CKRACKING_MOROCCO"
VALID_KEYS = ["TRIYAL-1234", "DEMLO-9999"]

services = ["Netflix", "PayPal", "Bank", "Coinbase", "Spotify", "cvv", "pin", "crypto", "applepay", "amazon", "microsoft", "venmo", "cashapp", "quadpay"]
names = ["John", "Alice", "Mark", "Sophia", "Leo", "Emma", "Ahmed", "Amine", "Jerry", "Salma", "William", "George", "Peris"]

user_subscriptions = {}

def generate_otp():
    return ''.join(str(random.randint(0, 9)) for _ in range(6))

# رسالة /start
start_message = """
🚀 Welcome to Our Otp Bot 🚀

🔐 ➜ /redeem | Redeem your subscription
⏱ ➜ /plan | Check your subscription

📝 Custom Commands
🧾 ➜ /createscript | Create custom scripts
🔏 ➜ /script [scriptid] | View script
🗣 ➜ /customcall | Call with script

📞 Modules
💳 ➜ /cvv | Capture CVV
🔢 ➜ /pin | Capture PIN
🅿️ ➜ /paypal | Capture Paypal Code
💵 ➜ /cashapp | Capture Cashapp Code
📦 ➜ /amazon | Approval Authentication

🔰 Purchase LAZARUS OTP
🛒 Contact: @CKRACKING_MOROCCO
"""

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Channel", url="https://t.me/LAZARUS_OTP")],
        [InlineKeyboardButton("🛒 Purchase", url="https://t.me/CKRACKING_MOROCCO")]
    ]
    await update.message.reply_text(start_message, reply_markup=InlineKeyboardMarkup(keyboard))

async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_subscriptions:
        await update.message.reply_text("✅ You have an active subscription.")
    else:
        await update.message.reply_text(f"""
🚫 You do not have a subscription.

💵 Plans:
1 Day : $20
2 Days : $30
1 Week : $55
1 Month : $100
Lifetime : $550

Contact {ADMIN_USERNAME} to buy.
        """)

async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args

    if not args:
        await update.message.reply_text("🔑 Please send a key: `/redeem YOUR_KEY`", parse_mode="Markdown")
        return

    key = args[0].strip()
    if key in VALID_KEYS:
        user_subscriptions[user_id] = True
        await update.message.reply_text("✅ Key accepted! Subscription activated.")
    else:
        await update.message.reply_text(
            f"❌ Invalid key.\nPlease contact {ADMIN_USERNAME} to purchase a valid one.",
            parse_mode="Markdown"
        )

async def send_random_messages(bot: Bot):
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
            print("✔️ Sent:", message)
        except Exception as e:
            print("❌ Error sending message:", e)

        await asyncio.sleep(random.randint(300, 600))  # 5-10 دقائق

async def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("plan", plan))
    app.add_handler(CommandHandler("redeem", redeem))

    # Task لإرسال رسائل عشوائية
    asyncio.create_task(send_random_messages(app.bot))

    print("🤖 Bot running...")
    await app.run_polling()

# تشغيل Flask
def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    # تشغيل Flask في Thread منفصل
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # تشغيل بوت تيليغرام
    asyncio.run(run_bot())
