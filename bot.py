import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Настройки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TOKEN = "8169122884:AAEMBsCJ0dFPhHhbo_rMSvLrbK4BI7tvgLw"
BOOSTY_LINK = "https://boosty.to/angel_summer"
CRYPTO_WALLET = "TCpF53TxJR7vGS8nBbMpdsPRd8Lj9rQdwC"

# Цены и типы фото
PHOTOS = {
    'cute': {'price': '15 USDT', 'desc': 'Милое фото 😊'},
    'sexy': {'price': '15 USDT', 'desc': 'Сексуальное фото 🔥'}, 
    'bikini': {'price': '25 USDT', 'desc': 'Бикини 👙'},
    'exclusive': {'price': '45 USDT', 'desc': 'Эксклюзив 💎'}
}

def start(update: Update, context: CallbackContext) -> None:
    menu = [
        [InlineKeyboardButton("📸 Мои фото", callback_data='photos')],
        [InlineKeyboardButton("🌟 Boosty", url=BOOSTY_LINK)],
        [InlineKeyboardButton("💌 Поддержать", callback_data='donate')]
    ]
    update.message.reply_text(
        "Привет, я Angel Summer 😘\nВыбери что тебе интересно:",
        reply_markup=InlineKeyboardMarkup(menu)
    )

def handle_buttons(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if query.data == 'photos':
        show_photos(query)
    elif query.data == 'donate':
        show_donate(query)
    elif query.data == 'back':
        start(update, context)
    elif query.data in PHOTOS:
        show_payment(query)

def show_photos(query):
    buttons = []
    for photo_type, info in PHOTOS.items():
        buttons.append([InlineKeyboardButton(
            f"{info['desc']} - {info['price']}", 
            callback_data=photo_type
        )])
    buttons.append([InlineKeyboardButton("◀️ Назад", callback_data='back')])
    
    query.edit_message_text(
        "Выбери фото 💋\nПосле оплаты пришлю тебе его лично:",
        reply_markup=InlineKeyboardMarkup(buttons))

def show_donate(query):
    text = f"💝 Поддержать меня можно переводом на:\n\n{CRYPTO_WALLET}\n\nСпасибо! 😘"
    query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Назад", callback_data='back')]]))

def show_payment(query):
    photo_type = query.data
    info = PHOTOS[photo_type]
    
    text = (f"💳 Для получения {info['desc'].lower()}:\n"
            f"1. Переведи {info['price']} на {CRYPTO_WALLET}\n"
            f"2. Напиши мне после оплаты\n\n"
            "Я пришлю фото в личку 💋")
    
    query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("◀️ К фото", callback_data='photos')],
            [InlineKeyboardButton("🏠 В начало", callback_data='back')]
        ]))

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(handle_buttons))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
