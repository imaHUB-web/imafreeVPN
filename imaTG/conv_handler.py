# Настраиваем обработчики
from imaTG import GREETING, OFFER, PROBLEM, SOLUTION, TESTIMONIALS, cancel, greeting, offer, problem, solution, start, testimonials


from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, filters


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