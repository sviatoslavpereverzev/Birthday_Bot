from settings_bot import TOKEN
import telebot
from telebot import types

bot = telebot.TeleBot(TOKEN)
upd = bot.get_updates()

print(upd)


@bot.message_handler(commands=['start'])
def keybord(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('/all')
    itembtn2 = types.KeyboardButton('/week')
    itembtn3 = types.KeyboardButton('/month')
    itembtn4 = types.KeyboardButton('/add')
    itembtn5 = types.KeyboardButton('/delete')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
    print(message)
    bot.send_message(message.chat.id, "Choose command:", reply_markup=markup, )


@bot.message_handler(commands=['all'])
def add_user(message):
    bot.send_message(message.chat.id, "All birthdays:")


@bot.message_handler(commands=['week'])
def add_user(message):
    bot.send_message(message.chat.id, "Birthdays on this week:")


@bot.message_handler(commands=['month'])
def add_user(message):
    bot.send_message(message.chat.id, "Birthdays on this month:")


@bot.message_handler(commands=['add'])
def add_user(message):
    bot.send_message(message.chat.id, "Add a new birthday:")
    bot.send_message(message.chat.id, "Write whose birthday:")


@bot.message_handler(commands=['delete'])
def add_user(message):
    bot.send_message(message.chat.id, "Delete birthday:")


bot.polling()
