from settings_bot import TOKEN
import telebot
from telebot import types
import time

bot = telebot.TeleBot(TOKEN)
upd = bot.get_updates()
new_user = False


@bot.message_handler(commands=['start'])
def keybord(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('/all')
    itembtn2 = types.KeyboardButton('/week')
    itembtn3 = types.KeyboardButton('/month')
    itembtn4 = types.KeyboardButton('/add')
    itembtn5 = types.KeyboardButton('/delete')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
    bot.send_message(message.chat.id, 'Choose command:', reply_markup=markup, )


@bot.message_handler(commands=['all'])
def all_birthdays(message):
    bot.send_message(message.chat.id, 'All birthdays:')


@bot.message_handler(commands=['week'])
def week_birthdays(message):
    bot.send_message(message.chat.id, 'Birthdays on this week:')


@bot.message_handler(commands=['month'])
def month_birthdays(message):
    bot.send_message(message.chat.id, 'Birthdays on this month:')


@bot.message_handler(commands=['add'])
def add_user(message):
    bot.send_message(message.chat.id, 'Add a new birthday: \nWrite whose birthday-')
    global new_user
    new_user = True


@bot.message_handler(commands=['delete'])
def delete_user(message):
    bot.send_message(message.chat.id, 'Delete birthday:')


@bot.message_handler(content_types=['text'])
def last_message(message):
    lm = message.text
    global new_user
    if new_user:
        new_user = False
        keyboard = types.InlineKeyboardMarkup()
        button_yes = types.InlineKeyboardButton(text='Yes', callback_data='name_yes')
        button_no = types.InlineKeyboardButton(text='No', callback_data='name_no')
        keyboard.add(button_yes, button_no)
        bot.send_message(message.chat.id, '{}\nThis is the name? '.format(lm), reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'name_yes':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Next step')
    elif call.data == 'name_no':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Try again')
        global new_user
        new_user = True


bot.polling()
