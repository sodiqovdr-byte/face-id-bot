import asyncio
import logging
from datetime import datetime
import pytz
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8372984586:AAEBpZ188bnvZbZuJ3HseMXaqy0ar57Kn-8"
YOUR_CHAT_ID = 2058150867
TIMEZONE = "Asia/Tashkent"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
TZ = pytz.timezone(TIMEZONE)

MORNING_MSG = "🌅 *Доброе утро!*\n\n🔒 Не забудь пройти *Face ID*!\nСделай это прямо сейчас 💪"
EVENING_MSG = "🌆 *Добрый вечер!*\n\n🔒 Напоминаю: нужно пройти *Face ID*!\nЗаймёт пару секунд 👍"

async def send_reminder(bot, text):
    try:
        await bot.send_message(chat_id=YOUR_CHAT_ID, text=text, parse_mode="Markdown")
    except Exception as e:
        logger.error("Ошибка: %s", e)

async def scheduler(bot):
    sent_morning = False
    sent_evening = False
    while True:
        now = datetime.now(TZ)
        h, m = now.hour, now.minute
        if h == 9 and m == 0 and not sent_morning:
            await send_reminder(bot, MORNING_MSG)
            sent_morning = True
        if h == 18 and m == 0 and not sent_evening:
            await send_reminder(bot, EVENING_MSG)
            sent_evening = True
        if h == 0 and m == 1:
            sent_morning = False
            sent_evening = False
        await asyncio.sleep(60)

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Бот работает!\n\n⏰ Напоминания:\n• 🌅 9:00 утра\n• 🌆 18:00 вечера")

async def cmd_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔒 *Не забудь пройти Face ID!* ✅", parse_mode="Markdown")

async def post_init(application):
    asyncio.create_task(scheduler(application.bot))

def main():
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("test", cmd_test))
    app.run_polling()

if __name__ == "__main__":
    main()
