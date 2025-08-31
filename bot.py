import os, asyncio
from telegram import Update, ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from db import get_user, latest_ads

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome. Use /latest or /subscribe to get premium alerts.")

async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    if not user or not user.get("paid"):
        await update.message.reply_text("You must pay to access premium data. Buy here: https://your-lemon-link")
        return
    args = context.args
    platform = args[0] if args else None
    ads = latest_ads(limit=5, platform=platform)
    if not ads:
        await update.message.reply_text("No recent ads found. Try again later.")
        return
    for a in ads:
        msg = f"*{a.get('title','Ad')}* \n{a.get('ad_url')}\nMetrics: {a.get('metrics')}"
        await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("pong")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("latest", latest))
    app.add_handler(CommandHandler("ping", ping))
    app.run_polling()

if __name__ == "__main__":
    main()
