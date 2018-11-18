from settings_bot import TOKEN
import telebot
import keyboards
import time

bot = telebot.TeleBot(TOKEN)
new_user = False
last_update = ''


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
def last_updates(message):
    global last_update, add_user_name, new_user
    last_update = message.text
    if new_user:
        new_user = False
        text = '{}\nThis is the name? '.format(last_update)
        keyboards.keyboard_y_or_n(message, text, bot)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    print(call.data)
    if call.data == 'answer_yes':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Next step')
        add_user_name = last_update
        choose_month(call.message, 'Mecяц', bot)

    elif call.data == 'answer_no':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Try again')
        global new_user
        new_user = True

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    print(call.data)


def choose_month(message, text, bot):
    keyboards.keyboard_month(message, text, bot)



bot.polling()
