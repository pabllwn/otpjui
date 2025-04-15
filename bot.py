from fastapi import FastAPI
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import random
import nest_asyncio

nest_asyncio.apply()

# إعدادات البوت
TOKEN = "8027706435:AAEzWtCBhIZPSo66BsC2CALd9X9F5LUVLWo"
CHANNEL_ID = "@LAZARUS_OTP"
ADMIN_USERNAME = "@CKRACKING_MOROCCO"
VALID_KEYS = ["TRIYAL-1234", "DEMLO-9999"]

# خدمات وهمية وأسماء
services = [
    "Netflix", "PayPal", "Bank", "Coinbase", "Spotify", "Cvv", "Pin", "Crypto",
    "Apple Pay", "Amazon", "Microsoft", "Venmo", "Cashapp", "Quadpay", "Bank Of America"
]
names = [
    "John", "Alice", "Mark", "Sophia", "Leo", "Emma", "Ahmed", "Amine",
    "Ahmed", "Jerry", "Salma", "William", "George", "Periz", "Nouh", "John", "Thomas", "Eric", "Mike"
]

user_subscriptions = {}

# FastAPI app
app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Bot is running!"}

# Telegram bot application
app_bot = ApplicationBuilder().token(TOKEN).build()

# توليد OTP
def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

# رسالة البداية
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

# بداية التطبيق
@app.on_event("startup")
async def startup_event():
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("plan", plan))
    app_bot.add_handler(CommandHandler("redeem", redeem))

    await app_bot.initialize()  # هذا هو التعديل المهم
    asyncio.create_task(app_bot.start())  # لا تستخدم run_polling بدون initialize
    asyncio.create_task(send_random_message(app_bot.bot))
