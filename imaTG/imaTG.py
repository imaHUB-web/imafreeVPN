import logging
from pickle import BUILD
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# Включаем логирование для отладки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Этапы воронки
GREETING, PROBLEM, SOLUTION, TESTIMONIALS, OFFER = range(5)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Привет! Я рад, что вы здесь. Сегодня я расскажу вам о нашем продукте и о том, "
        "как он может помочь решить вашу проблему. Готовы узнать больше? (Ответьте 'да' для продолжения)"
    )
    return GREETING

# Этап 1: Приветствие и знакомство
async def greeting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text.lower() == 'да':
        await update.message.reply_text(
            "Отлично! Множество людей сталкиваются с этой проблемой, и наш продукт предлагает эффективное решение. "
            "Позвольте рассказать, с какой именно проблемой мы работаем. Продолжить? (Ответьте 'да' для продолжения)"
        )
        return PROBLEM
    else:
        await update.message.reply_text("Напишите 'да', чтобы продолжить.")
        return GREETING

# Этап 2: Информация о проблеме
async def problem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text.lower() == 'да':
        await update.message.reply_text(
            "Многие наши клиенты сталкивались с проблемой [описание проблемы]. Это влияло на их жизнь и работу. "
            "Наш продукт создан, чтобы навсегда решить эту проблему. Хотите узнать, как он это делает? (Ответьте 'да')"
        )
        return SOLUTION
    else:
        await update.message.reply_text("Напишите 'да', чтобы продолжить.")
        return PROBLEM

# Этап 3: Предложение решения
async def solution(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text.lower() == 'да':
        await update.message.reply_text(
            "Наш продукт использует инновационные подходы для решения [описание проблемы]. "
            "Благодаря этому наши клиенты достигают потрясающих результатов. Хотите услышать отзывы? (Ответьте 'да')"
        )
        return TESTIMONIALS
    else:
        await update.message.reply_text("Напишите 'да', чтобы продолжить.")
        return SOLUTION

# Этап 4: Отзывы и кейсы
async def testimonials(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text.lower() == 'да':
        await update.message.reply_text(
            "Вот несколько отзывов наших клиентов:\n"
            "- Клиент А: 'Это изменило мою жизнь!'\n"
            "- Клиент Б: 'Я не ожидал такого результата!'\n"
            "Теперь, когда вы видите, как это работает для других, готовы узнать, как это может помочь вам? (Ответьте 'да')"
        )
        return OFFER
    else:
        await update.message.reply_text("Напишите 'да', чтобы продолжить.")
        return TESTIMONIALS

# Этап 5: Предложение купить
async def offer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text.lower() == 'да':
        await update.message.reply_text(
            "Мы готовы предложить вам специальное предложение! Вы можете приобрести наш продукт со скидкой прямо сейчас. "
            "Напишите 'купить', чтобы получить инструкцию по покупке или 'нет', если у вас остались вопросы."
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text("Напишите 'да', чтобы продолжить.")
        return OFFER

# Команда для завершения беседы или завершения этапов
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Сессия завершена. Спасибо за внимание!")
    return ConversationHandler.END

def main():
    # Создаем приложение и подключаем токен
    app = ApplicationBuilder().token("7329486471:AAEK60PJ680Wwbg46VsLKJ3Vn1tHBlMk4AQ")
    BUILD()  # Замените на ваш токен от BotFather

    # Настраиваем обработчики
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GREETING: [MessageHandler(filters.TEXT & ~filters.COMMAND, greeting)],
            PROBLEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, problem)],
            SOLUTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, solution)],
            TESTIMONIALS: [MessageHandler(filters.TEXT & ~filters.COMMAND, testimonials)],
            OFFER: [MessageHandler(filters.TEXT & ~filters.COMMAND, offer)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Добавляем обработчик для ConversationHandler
    app.add_handler(conv_handler)

    # Добавляем обработчик для ошибок
    app.add_error_handler(lambda update, context: logger.error(f"Произошла ошибка: {context.error}"))

    logger.info("Бот запущен")
    # Запускаем бота
    app.run_polling()

if __name__ == "__main__":
    main()
