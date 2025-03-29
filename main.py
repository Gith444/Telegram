import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from flask import Flask
from threading import Thread

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ваш токен (замените на свой)
TOKEN = "ВАШ_ТОКЕН_ОТ_BOTFATHER"

# Функция для старта бота
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Меню 1", callback_data='menu_1')],
        [InlineKeyboardButton("Меню 2", callback_data='menu_2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Привет! Выберите меню:", reply_markup=reply_markup)

# Обработчик кнопок
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'menu_1':
        keyboard = [
            [InlineKeyboardButton("Подпункт 1", callback_data='submenu_1_1')],
            [InlineKeyboardButton("Подпункт 2", callback_data='submenu_1_2')],
            [InlineKeyboardButton("Подпункт 3", callback_data='submenu_1_3')],
            [InlineKeyboardButton("Назад", callback_data='back_to_start')]
        ]
        query.edit_message_text("Меню 1. Выберите подпункт:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'menu_2':
        keyboard = [
            [InlineKeyboardButton("Подпункт 1", callback_data='submenu_2_1')],
            [InlineKeyboardButton("Подпункт 2", callback_data='submenu_2_2')],
            [InlineKeyboardButton("Подпункт 3", callback_data='submenu_2_3')],
            [InlineKeyboardButton("Назад", callback_data='back_to_start')]
        ]
        query.edit_message_text("Меню 2. Выберите подпункт:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith('submenu_'):
        menu_number, submenu_number = query.data.split('_')[1:3]
        send_image_and_text(query, submenu_number)

    elif query.data == 'back_to_start':
        start(update, context)

# Отправка изображения и текста
def send_image_and_text(query, submenu_number):
    images = {
        '1': 'https://example.com/image1.jpg',
        '2': 'https://example.com/image2.jpg',
        '3': 'https://example.com/image3.jpg'
    }
    texts = {
        '1': 'Описание изображения 1.',
        '2': 'Описание изображения 2.',
        '3': 'Описание изображения 3.'
    }

    image_url = images.get(submenu_number, 'https://example.com/default.jpg')
    text = texts.get(submenu_number, 'Описание отсутствует.')

    query.edit_message_text(text=text)
    query.message.reply_photo(photo=image_url)

# Запуск Flask-сервера для Keep Alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

def run():
    app.run(host="0.0.0.0", port=8080)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    Thread(target=run).start()

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
