from fastapi import FastAPI, Request
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio, random, nest_asyncio

nest_asyncio.apply()

TOKEN = "8027706435:AAEzWtCBhIZPSo66BsC2CALd9X9F5LUVLWo"
CHANNEL_ID = "@LAZARUS_OTP"
ADMIN_USERNAME = "@CKRACKING_MOROCCO"
VALID_KEYS = ["TRIYAL-1234", "DEMLO-9999"]
WEBHOOK_URL = "https://bot-2-splv.onrender.com/webhook"

services = ["Netflix", "PayPal", "Bank", "Coinbase", "Spotify", "Cvv", "Pin", "Crypto",
            "Apple Pay", "Amazon", "Microsoft", "Venmo", "Cashapp", "Quadpay", "Bank Of America"]
names = ["John", "Alice", "Mark", "Sophia", "Leo", "Emma", "Ahmed", "Amine",
         "Ahmed", "Jerry", "Salma", "William", "George", "Periz", "Nouh", "John", "Thomas", "Eric", "Mike"]
user_subscriptions = {}

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Bot is running!"}

@app.get("/health")
async def health_check():
    return {"status": "Bot is alive"}

app_bot = ApplicationBuilder().token(TOKEN).build()

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

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
📧 ➜ /email | grab Email code  
🕖 ➜ /remind | remind victim  

SET CUSTOM VOICE  
🗣 ➜ /customvoice | Modify the TTS  
❗️ ➜ EXAMPLE: /customvoice number spoof service name sid language  

🔰 Purchase LAZARUS OTP 🔰  
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
    await update.message.reply_text("💵 Prices: 1D = $20, 1W = $55, 1M = $100\nDM @CKRACKING_MOROCCO to buy.")

async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    if not args:
        await update.message.reply_text("🔑 Use: /redeem YOUR_KEY", parse_mode="Markdown")
        return
    key = args[0].strip()
    if key in VALID_KEYS:
        user_subscriptions[user_id] = True
        await update.message.reply_text("✅ Key accepted!")
    else:
        await update.message.reply_text(f"❌ Invalid key.\nContact {ADMIN_USERNAME}")

# أوامر وهمية لإظهار التكامل الكامل
async def createscript(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧾 Script created successfully!")

async def view_script(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔏 This is your script content.")

async def customcall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🗣 Starting custom call...")

async def customvoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🗣 Custom voice set.")

async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏰ Victim will be reminded.")

async def recall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("♻️ Recalling...")

# Fake Call Commands (ردود وهمية فقط حالياً)
fake_commands = [
    "call", "bank", "cvv", "pin", "applepay", "coinbase", "crypto", "amazon",
    "microsoft", "paypal", "venmo", "cashapp", "quadpay", "carrier", "email"
]

for cmd in fake_commands:
    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE, cmd=cmd):
        await update.message.reply_text(f"📞 Capturing {cmd.upper()} OTP...")
    app_bot.add_handler(CommandHandler(cmd, handler))

# إرسال OTP عشوائي كل فترة
async def send_random_message(bot: Bot):
    while True:
        service = random.choice(services)
        name = random.choice(names)
        otp = generate_otp()
        msg = f"🔐 OTP Alert!\n👤 Name: {name}\n🛠 Service: {service}\n🔢 OTP: {otp}"
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=msg)
            print("✔️ Sent:", msg)
        except Exception as e:
            print("❌ Error:", e)
        await asyncio.sleep(random.randint(300, 900))

@app.on_event("startup")
async def startup_event():
    # الأوامر الأساسية
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("plan", plan))
    app_bot.add_handler(CommandHandler("redeem", redeem))

    # الأوامر الإضافية
    app_bot.add_handler(CommandHandler("createscript", createscript))
    app_bot.add_handler(CommandHandler("script", view_script))
    app_bot.add_handler(CommandHandler("customcall", customcall))
    app_bot.add_handler(CommandHandler("customvoice", customvoice))
    app_bot.add_handler(CommandHandler("remind", remind))
    app_bot.add_handler(CommandHandler("recall", recall))

    await app_bot.initialize()
    await app_bot.bot.set_webhook(WEBHOOK_URL)
    print("✅ Webhook set.")
    asyncio.create_task(send_random_message(app_bot.bot))

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, app_bot.bot)
    await app_bot.process_update(update)
    return {"ok": True}
