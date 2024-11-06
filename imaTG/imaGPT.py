import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# Включаем логирование для отладки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Статусы для автоворонки
WAITING_FOR_CODE = 1

# Список активных кодов доступа
ACCESS_CODES = {'18.03.05': True}  # Замените '18.03.05' на реальный код доступа

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Команда /start запущена")
    await update.message.reply_text(
        "Добро пожаловать! Чтобы получить доступ к боту, введите код доступа. "
        "Если у вас нет кода, свяжитесь с поддержкой для его покупки."
    )
    return WAITING_FOR_CODE

# Проверка кода доступа и отображение кнопок
async def check_access_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()
    if code in ACCESS_CODES and ACCESS_CODES[code]:
        ACCESS_CODES[code] = False  # Код используется один раз
        # Кнопки для дальнейшего взаимодействия
        keyboard = [
            ["Информация", "Помощь"],
            ["Связаться с поддержкой", "Закрыть"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text(
            "Код принят! Теперь у вас есть доступ к боту.",
            reply_markup=reply_markup
        )
        logger.info("Код принят, доступ предоставлен")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Неверный код доступа. Попробуйте снова.")
        logger.info("Неверный код доступа введен")
        return WAITING_FOR_CODE

# Обработка команд кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if user_text == "Информация":
        await update.message.reply_text("Здесь будет информация о сервисе.")
    elif user_text == "Помощь":
        await update.message.reply_text("Чем могу помочь?")
    elif user_text == "Связаться с поддержкой":
        await update.message.reply_text("Для связи с поддержкой напишите на email@example.com.")
    elif user_text == "Закрыть":
        await update.message.reply_text("Сессия завершена. Вы можете снова ввести /start для нового доступа.")
        return ConversationHandler.END

# Обработка ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Произошла ошибка: {context.error}")

def main():
    # Создаем приложение и подключаем токен
    app = Application.builder().token("7665733928:AAGt_kh9J8o6SsCRcreat9UYoMitzGvK8uo").build()  # Замените на ваш токен от BotFather

    # Настраиваем обработчики
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_FOR_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_access_code)],
        },
        fallbacks=[],
    )
    
    # Обработчик для кнопок и сообщений
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))
    app.add_error_handler(error_handler)

    logger.info("Бот запущен")
    # Запускаем бота
    app.run_polling()

if __name__ == "__main__":
    main()
