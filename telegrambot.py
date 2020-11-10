from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TG_TOKEN, TG_API_URL
def main():
    my_bot = Updater(TG_TOKEN, TG_API_URL, use_context=True)

    my_bot.dispatcher.add_handler(CommandHandler('start', sms))
    my_bot.start_polling()
    my_bot.idle()

def sms(bot, update):
    bot.message.reply_text('Привет {}! \n'
                           'Добро пожаловать с лучший сервис'.format(bot.message.chat.first_name))
    print(bot.message)
main()