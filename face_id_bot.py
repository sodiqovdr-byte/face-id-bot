
import asyncio
import logging
from datetime import datetime
import pytz
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, JobQueue

BOT_TOKEN = 8372984586:AAEBpZ188bnvZbZuJ3HseMXaqy0ar57Kn-8
YOUR_CHAT_ID = 2058150867
TIMEZONE = "Asia/Tashkent"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_morning(context):
    await context.bot.send_message(
        chat_id=YOUR_CHAT_ID,
        text="🌅 *Доброе утро!*\n\n🔒 Не забудь пройти *Face ID*! 💪",
        parse_mode="Markdown"
    )

async def send_evening(context):
    await context.bot.send_message(
        chat_id=YOUR_CHAT_ID,
        text="🌆 *Добрый вечер!*\n\n🔒 Не забудь пройти *Face ID*! 👍",
        parse_mode="Markdown"
    )

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Бот работает!\n\n⏰ Напоминания:\n• 🌅 9:00 утра\n• 🌆 18:00 вечера"
    )

async def cmd_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔒 Не забудь пройти Face ID! ✅")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("test", cmd_test))
    
    tz = pytz.timezone(TIMEZONE)
    app.job_queue.run_daily(send_morning, time=datetime.strptime("09:00", "%H:%M").time().replace(tzinfo=tz))
    app.job_queue.run_daily(send_evening, time=datetime.strptime("18:00", "%H:%M").time().replace(tzinfo=tz))
    
    app.run_polling()

if __name__ == "__main__":
    main()
