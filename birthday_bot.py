from settings_bot import TOKEN
import telebot
import keyboards
import time

bot = telebot.TeleBot(TOKEN)
new_user = False


@bot.message_handler(commands=['start'])
def start(message):
    keyboards.keyboard_month(message, 'smmm', bot)


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
        text = '{}\nThis is the name? '.format(lm)
        keyboards.keyboard_y_or_n(message, text, bot)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'name_yes':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Next step')
    elif call.data == 'name_no':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Try again')
        global new_user
        new_user = True


bot.polling()
