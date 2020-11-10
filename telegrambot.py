from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from settings import TG_TOKEN
from telegram import ParseMode

def main():
    my_bot = Updater(TG_TOKEN, use_context=True)

    my_bot.dispatcher.add_handler(CommandHandler('start', sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Москва'), msk))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Тверь'), tver))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Мельбурн'), mel))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Назад'), back))
    my_bot.dispatcher.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Заполнить Анкету'), anketa_start)],
        states={
            "user_name": [MessageHandler(Filters.text, anketa_get_name)],
            "user_age": [MessageHandler(Filters.text, anketa_get_age)],
            "evaluation": [MessageHandler(Filters.regex('1|2|3|4|5'), anketa_get_evaluation)],
            "comment": [MessageHandler(Filters.regex('Пропустить'), anketa_exit_comment),
                        MessageHandler(Filters.text, anketa_comment)],
            },

        fallbacks=[MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document, what)]
    )
    )
    my_bot.start_polling()
    my_bot.idle()

def what(bot, update):
    bot.message.reply_text('Я вас не понимаю, выберите ответ на клавиатуре')

def anketa_comment(bot, update):
    update.user_data['comment'] = bot.message.text
    text ="""Результат Опроса:
    Имя = {name}
    Возраст = {age}
    Оценка = {evaluation}
    Комментарий = {comment}
    """.format(**update.user_data)
    bot.message.reply_text(text, parse_mode=ParseMode.HTML)
    bot.message.reply_text('Спасибо за комментарий', reply_markup=get_keyboard())
    return ConversationHandler.END

def anketa_exit_comment(bot, update):
    text =""" Результат Опроса:
    Имя = {name}
    Возраст = {age}
    Оценка = {evaluation}
    """.format(**update.user_data)
    bot.message.reply_text(text, parse_mode=ParseMode.HTML)
    bot.message.reply_text('Спасибо', reply_markup=get_keyboard())
    return ConversationHandler.END

def anketa_get_evaluation(bot, update):
    update.user_data['evaluation'] = bot.message.text
    reply_keyboard = [['Пропустить']]
    bot.message.reply_text("Напишите комментарий или пропустите",
                           reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return "comment"

def anketa_get_age(bot, update):
    update.user_data['age'] = bot.message.text
    reply_keyboard = [['1','2']]
    bot.message.reply_text("Оставьте отзыв от 1 до 5",
                           reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return "evaluation"

def anketa_get_name(bot, update):
    update.user_data['name'] = bot.message.text
    bot.message.reply_text("Сколько Вам лет?")
    return "user_age"

def anketa_start(bot, update):
    bot.message.reply_text('Имя и Фамилия?')
    return "user_name"

def msk(bot, update):
    my_keyboard = ReplyKeyboardMarkup([['ЮВАО','ЦАО'],['ЮАО','САО'],['Назад']], resize_keyboard=True)
    bot.message.reply_text('Отлично {}! \n'
                           'Ты выбрал Москву \n'
                           'Выбери из меню ниже Округ'.format(bot.message.chat.first_name), reply_markup=my_keyboard)
def tver(bot, update):
    my_keyboard = ReplyKeyboardMarkup([['Пролетарская','Центральный'],['Назад']], resize_keyboard=True)
    bot.message.reply_text('Отлично {}! \n'
                           'Ты выбрал Тверь \n'
                           'Выбери из меню ниже Округ'.format(bot.message.chat.first_name), reply_markup=my_keyboard)
def mel(bot, update):
    my_keyboard = ReplyKeyboardMarkup([['Челси','Франкстон'],['Назад']], resize_keyboard=True)
    bot.message.reply_text('Отлично {}! \n'
                           'Ты выбрал Мельбурн \n'
                           'Выбери из меню ниже Округ'.format(bot.message.chat.first_name), reply_markup=my_keyboard)

def sms(bot, update):
    bot.message.reply_text('Привет {}! \n'
                           'Добро пожаловать \n'
                           'Выбери из меню ниже Город'.format(bot.message.chat.first_name), reply_markup=get_keyboard())
    print(bot.message)

def back(bot, update):
    bot.message.reply_text('Выбери из меню ниже Город'.format(bot.message.chat.first_name), reply_markup=get_keyboard())
    print(bot.message)

def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([['Москва', 'Тверь'], ['Мельбурн','Заполнить Анкету']], resize_keyboard=True)
    return my_keyboard

main()