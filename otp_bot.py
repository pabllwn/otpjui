from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import random
import asyncio
import nest_asyncio

nest_asyncio.apply()

# بيانات البوت
TOKEN = "8027706435:AAG9y4UGSl9Ha4pdqc7ZmLEK6ETTKxMsD7A"
CHANNEL_ID = "@LAZARUS_OTP"
OWNER_USERNAME = "@CKRACKING_MOROCCO"
VALID_KEYS = ["abttttttc123", "keyttttttest", "lazaruyyyyyyyyysvip"]  # المفاتيح الصحيحة

services = ["Netflix", "PayPal", "Bank", "Coinbase", "Spotify", "cvv", "pin", "crypto", "applepay", "amazon", "microsoft", "venmo", "cashapp", "quadpay"]
names = ["John", "Alice", "Mark", "Sophia", "Leo", "Emma", "Ahmed", "Amine", "Jerry", "Salma", "William", "George", "Peris"]

# توليد OTP
def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

# رسالة /start
start_message = """
🚀 Welcome to Our Otp Bot 🚀

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
💵 ➜ /cashapp | Capture Cashapp Code  
💳 ➜ /quadpay | Capture quadpay Code  
📟 ➜ /carrier | Capture carrier Code  
📧 ➜ /email | grab Email code  
🕖 ➜ /remind | remind victim
"""

# الرد على /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Channel", url="https://t.me/LAZARUS_OTP")],
        [InlineKeyboardButton("🛒 Purchase", url="https://t.me/CKRACKING_MOROCCO")]
    ]
    await update.message.reply_text(start_message, reply_markup=InlineKeyboardMarkup(keyboard))

# الرد على /plan
async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "❌ You don't have an active subscription.\n\n"
        "💵 Pricing Plans:\n"
        "• 1 Day : $20\n"
        "• 2 Days : $30\n"
        "• 1 Week : $55\n"
        "• 2 Weeks : $70\n"
        "• 1 Month : $100\n"
        "• 3 Months : $250\n"
        "• Lifetime : $550\n\n"
        f"Contact {OWNER_USERNAME} to get your key 🔑"
    )
    await update.message.reply_text(message)

# التعامل مع /redeem
async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("🔑 Please enter your key.\nExample: `/redeem your_key_here`", parse_mode="Markdown")
        return

    user_key = args[0]
    if user_key in VALID_KEYS:
        await update.message.reply_text("✅ Key accepted. Subscription activated.")
    else:
        await update.message.reply_text(
            f"❌ Invalid key: `{user_key}`\n\nPlease contact {OWNER_USERNAME} to purchase a valid key.",
            parse_mode="Markdown"
        )

# إرسال رسائل OTP عشوائية
async def send_random_message(bot: Bot):
    while True:
        service = random.choice(services)
        name = random.choice(names)
        otp = generate_otp()
        message = (
            "🔐 *OTP Alert!*\n"
            f"👤 *Name:* {name}\n"
            f"🛠 *Service:* {service}\n"
            f"🔢 *OTP:* `{otp}`"
        )
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode="Markdown")
            print("Sent:", message)
        except Exception as e:
            print("Error:", e)
        await asyncio.sleep(random.randint(300, 900))  # من 5 إلى 15 دقيقة

# تشغيل البوت
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("plan", plan))
    app.add_handler(CommandHandler("redeem", redeem))

    # Ping command for uptime robot
    async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("✅ I'm Alive!")

    app.add_handler(CommandHandler("ping", ping))

    asyncio.create_task(send_random_message(app.bot))

    print("Bot is running...")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
    
