from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask
import asyncio
import threading
import random
import nest_asyncio
import os

nest_asyncio.apply()

# بيانات البوت
TOKEN = "8027706435:AAH36GpgqPFQPX7sDFhgjkbSemLVQkK1Qqw"
CHANNEL_ID = "@LAZARUS_OTP"
ADMIN_USERNAME = "@CKRACKING_MOROCCO"

# بيانات الاشتراك التجريبية (لاحقاً يمكن ربطها بقاعدة بيانات)
valid_keys = ["TRIAL-1234", "VIP-4567"]  # أمثلة مفاتيح
user_subscriptions = {}

# خدمات وهمية
services = [
    "Netflix", "PayPal", "Bank", "Coinbase", "Spotify", "CVV", "PIN", "Crypto",
    "Apple Pay", "Amazon", "Microsoft", "Venmo", "CashApp", "QuadPay"
]

names = [
    "John", "Alice", "Mark", "Sophia", "Leo", "Emma", "Ahmed", "Amine",
    "Jerry", "Salma", "William", "George", "Peris", "Ronnie"
]

# توليد OTP
def generate_otp():
    return ''.join(str(random.randint(0, 9)) for _ in range(6))

# رسالة /start
start_message = """
🚀 Welcome to LAZARUS OTP Bot 🚀

🔐 ➜ /redeem | Redeem your subscription
⏱ ➜ /plan | Check your subscription

🧾 ➜ /createscript | Create custom scripts
🔏 ➜ /script [scriptid] | View script
🗣 ➜ /customcall | Call with script

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
💵 ➜ /cashapp | Capture CashApp Code
💳 ➜ /quadpay | Capture QuadPay Code
📟 ➜ /carrier | Capture Carrier Code
📧 ➜ /email | Grab Email Code
🕖 ➜ /remind | Remind Victim

🗣 ➜ /customvoice | Modify the TTS
❗️ ➜ Example: /customvoice number spoof service name sid language

💎 Extras
◆ ⌨️ ⮞ /recall for re-calling
◆ ❓ ⮞ Use '?' in number field for spoofing
"""

# Flask app لتشغيل البوت دائماً
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Channel", url="https://t.me/LAZARUS_OTP")],
        [InlineKeyboardButton("🛒 Purchase", url=f"https://t.me/{ADMIN_USERNAME.lstrip('@')}")]
    ]
    await update.message.reply_text(start_message, reply_markup=InlineKeyboardMarkup(keyboard))

# /plan command
async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_subscriptions:
        await update.message.reply_text("✅ You already have an active subscription.")
    else:
        plan_message = f"""
❌ You don't have any active subscription.

💳 Available Plans:
💵 1 Day : $20
💵 2 Days : $30
💵 1 Week : $55
💵 2 Weeks : $70
💵 1 Month : $100
💵 3 Months : $250
💵 Lifetime : $550

🔑 To buy a key, DM {ADMIN_USERNAME}
"""
        await update.message.reply_text(plan_message)

# /redeem command
async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    user_id = update.effective_user.id
    if not args:
        await update.message.reply_text("📥 Please enter your subscription key.\nExample: `/redeem YOUR-KEY`", parse_mode="Markdown")
    else:
        key = args[0]
        if key in valid_keys:
            user_subscriptions[user_id] = key
            await update.message.reply_text("✅ Subscription redeemed successfully! You now have access.")
        else:
            await update.message.reply_text(
                f"❌ Invalid key.\nIf you want to purchase a valid subscription, contact {ADMIN_USERNAME}",
                reply_to_message_id=update.message.message_id
            )

# إرسال رسائل وهمية عشوائية
async def send_random_message(bot: Bot):
    while True:
        service = random.choice(services)
        name = random.choice(names)
        otp = generate_otp()
        message = f"""
🔐 OTP Alert!
👤 Name: {name}
🛠 Service: {service}
🔢 OTP: {otp}
"""
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=message)
            print("✅ Sent:", message.strip())
        except Exception as e:
            print("❌ Error sending message:", e)
        await asyncio.sleep(random.randint(300, 900))  # من 5 إلى 15 دقيقة

# تشغيل البوت
async def main():
    app_telegram = ApplicationBuilder().token(TOKEN).build()

    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(CommandHandler("plan", plan))
    app_telegram.add_handler(CommandHandler("redeem", redeem))

    asyncio.create_task(send_random_message(app_telegram.bot))
    print("✅ Bot is running...")
    await app_telegram.run_polling()

# تشغيل Flask و Telegram معاً
if __name__ == '__main__':
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    asyncio.get_event_loop().run_until_complete(main())
    
