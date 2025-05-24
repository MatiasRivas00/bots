from telegram import Update
from telegram.ext import ContextTypes

from app.controllers.money import create_transaction_from_message, week_summary, month_summary, year_summary
from app.controllers.user import get_user_by_telegram_id
from app.bot_money.utils import parse_transaction_to_reply, parse_summary_to_reply

from app.core.logger import logger

async def handle_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Mensaje recibido: {update.message.text}")
    try:
        message = update.message.text.replace("/t", "")
        user = get_user_by_telegram_id(update.message.from_user.id)
        transaction = create_transaction_from_message(message, user.id)
        reply_transaction = parse_transaction_to_reply(transaction)
        logger.info(f"Respuesta enviada: {reply_transaction}")
        await update.message.reply_text(reply_transaction)
    except Exception as e:
        logger.error(f"Error al procesar el mensaje: {e}")
        await update.message.reply_text(str(e))

async def handle_week_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user_by_telegram_id(update.message.from_user.id)
    summary = week_summary(user.id)
    reply_summary = parse_summary_to_reply(summary)
    await update.message.reply_text(f"```\n{reply_summary}\n```", parse_mode='MarkdownV2')

async def handle_month_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user_by_telegram_id(update.message.from_user.id)
    summary = month_summary(user.id)
    reply_summary = parse_summary_to_reply(summary)
    await update.message.reply_text(f"```\n{reply_summary}\n```", parse_mode='MarkdownV2')

async def handle_year_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user_by_telegram_id(update.message.from_user.id)
    summary = year_summary(user.id)
    reply_summary = parse_summary_to_reply(summary)
    await update.message.reply_text(f"```\n{reply_summary}\n```", parse_mode='MarkdownV2')
