from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from flask import Flask
import random
import asyncio
import nest_asyncio

nest_asyncio.apply()

# بيانات البوت
TOKEN = "8027706435:AAH36GpgqPFQPX7sDFhgjkbSemLVQkK1Qqw"
CHANNEL_ID = "@LAZARUS_OTP"
OWNER_USERNAME = "@CKRACKING_MOROCCO"

# Flask لتشغيل دائم
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot is running!"

services = [
    "Netflix", "PayPal", "Bank", "Coinbase", "Spotify", "cvv", "pin", "crypto",
    "applepay", "amazon", "microsoft", "venmo", "cashapp", "quadpay"
]

names = [
    "John", "Alice", "Mark", "Sophia", "Leo", "Emma", "Ahmed", "Amine",
    "Jerry", "Salma", "William", "George", "Peris"
]

# توليد OTP
def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

# رسالة /start
start_message = """
🚀 Welcome to Our Otp Bot 🚀

🔐 ➜ /redeem | Redeem your subscription  
⏱ ➜ /plan | Check your subscription

📝 Custom Commands  
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
📧 ➜ /email | Grab Email code  
🕖 ➜ /remind | Remind victim  

SET CUSTOM VOICE  
🗣 ➜ /customvoice | Modify the TTS  
❗️ Example: /customvoice number spoof service name sid language  

🔰 Purchase LAZARUS OTP 🔰  
💎 Extras  
⌨️ /recall for re-calling  
❓ Use '?' on from number for random spoof
"""

# رد على /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Channel", url="https://t.me/LAZARUS_OTP")],
        [InlineKeyboardButton("🛒 Purchase", url="https://t.me/CKRACKING_MOROCCO")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(start_message, reply_markup=reply_markup)

# رد على /plan
async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ You currently have no active subscription.")
    await update.message.reply_text(f"""
💳 Subscription Plans:

💵 1 Day    : $20  
💵 2 Days  : $30  
💵 1 Week  : $55  
💵 2 Weeks : $70  
💵 1 Month : $100  
💵 3 Months: $250  
💵 Lifetime: $550

🔑 To purchase a key, contact {OWNER_USERNAME}
    """)

# الرد على /redeem
async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("🔑 Please provide your key.\nExample: `/redeem ABCD1234`", parse_mode="Markdown")
    else:
        key = context.args[0]
        # تحقق من صحة المفتاح (هنا عشوائي، غيّر الشرط حسب القاعدة)
        if key.lower() != "validkey":
            await update.message.reply_text(
                f"❌ Invalid Key: `{key}`\n\nPlease contact {OWNER_USERNAME} to purchase a valid key.",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("✅ Key accepted! Subscription activated.")

# إرسال رسائل OTP عشوائية
async def send_random_message(bot: Bot):
    while True:
        service = random.choice(services)
        name = random.choice(names)
        otp = generate_otp()
        message = f"""🔐 *OTP Alert!*

👤 *Name:* {name}  
🛠 *Service:* {service}  
🔢 *OTP:* `{otp}`"""

        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")
            print("Sent:", message)
        except Exception as e:
            print("Error sending message:", e)
        await asyncio.sleep(random.randint(300, 900))  # كل 5 إلى 15 دقيقة

# تشغيل البوت
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("plan", plan))
    app.add_handler(CommandHandler("redeem", redeem))

    asyncio.create_task(send_random_message(app.bot))

    print("Bot is running...")
    await app.run_polling()

# تشغيل Flask و البوت
if __name__ == '__main__':
    import threading

    threading.Thread(target=lambda: app_flask.run(host="0.0.0.0", port=8080)).start()
    asyncio.get_event_loop().run_until_complete(main())
  
