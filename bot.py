from fastapi import FastAPI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import random

# إعداد البوت
TOKEN = "توكن_البوت_ديالك"
CHANNEL_ID = "@channel_id"
ADMIN_USERNAME = "@admin_username"
VALID_KEYS = ["TRIAL-1234", "DEMO-9999"]

services = [
    "Netflix", "PayPal", "Bank", "Coinbase", "Spotify", "Cvv", "Pin", "Crypto",
    "Apple Pay", "Amazon", "Microsoft", "Venmo", "Cashapp", "Quadpay", "Bank Of America"
]

names = [
    "John", "Alice", "Mark", "Sophia", "Leo", "Emma", "Ahmed", "Amine",
    "Jerry", "Salma", "William", "George", "Periz", "Nouh", "Thomas", "Eric", "Mike"
]

user_subscriptions = {}

# FastAPI app
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bot is running!"}

# OTP Generator
def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

# رسائل البوت
start_message = """
🚀 Welcome to Our Otp Bot 🚀

🔐 ➜ /redeem | Redeem your subscription  
⏱ ➜ /plan | Check your subscription  

📝  Custom Commands  
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

🔰  Purchase LAZARUS OTP  
💎 Extras  
⌨️ /recall for re-calling  
❓ Use `?` in number to spoof random number
"""

# أوامر البوت
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

# إرسال رسائل عشوائية
async def send_random_message(bot):
    while True:
        service = random.choice(services)
        name = random.choice(names)
        otp = generate_otp()
        message = f"🔐 OTP Alert!\n👤 Name: {name}\n🛠 Service: {service}\n🔢 OTP: {otp}"
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=message)
        except Exception as e:
            print("❌ Error:", e)
        await asyncio.sleep(random.randint(300, 900))  # كل 5 إلى 15 دقيقة

# تشغيل البوت تلقائياً مع FastAPI
@app.on_event("startup")
async def startup_event():
    from telegram.ext import ApplicationBuilder
    app_bot = ApplicationBuilder().token(TOKEN).build()

    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("plan", plan))
    app_bot.add_handler(CommandHandler("redeem", redeem))

    asyncio.create_task(send_random_message(app_bot.bot))
    asyncio.create_task(app_bot.run_polling())
