from settings_bot import TOKEN
import telebot
from telebot import types
import calendar
import time

bot = telebot.TeleBot(TOKEN)
new_user = False
MONTH = [['Декабрь', 'Январь', 'Февраль'], ['Март', 'Апрель', 'Май'], ['Июнь', 'Июль', 'Август'],
         ['Сентябрь', 'Октябрь', 'Ноябрь']]


def keyboard_y_or_n(message, text):
    keyboard = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text='Yes', callback_data='name_yes')
    button_no = types.InlineKeyboardButton(text='No', callback_data='name_no')
    keyboard.add(button_yes, button_no)
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


def keyboard_day(message, text, month):
    keyboard = types.InlineKeyboardMarkup()
    cal = calendar.Calendar(firstweekday=0)
    button = []
    i = 0
    for week in cal.monthdays2calendar(2000, month):
        button.append([])
        for day in week:
            button[i].append(
                types.InlineKeyboardButton(text='{}'.format((' ' if day[0] == False else day[0])),
                                           callback_data='{}'.format(day[0])))
        i += 1
    for week in button:
        keyboard.row(week[0], week[1], week[2], week[3], week[4], week[5], week[6])
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


def keyboard_month(message, text):
    keyboard = types.InlineKeyboardMarkup()
    button = []
    i = 0
    for seasons in MONTH:
        button.append([])
        for month in seasons:
            button[i].append(types.InlineKeyboardButton(text='{}'.format(month), callback_data='{}'.format(month)))
        i += 1
    for seasons in button:
        keyboard.row(seasons[0], seasons[1], seasons[2])
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


def keyboard_command(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('/all')
    itembtn2 = types.KeyboardButton('/week')
    itembtn3 = types.KeyboardButton('/month')
    itembtn4 = types.KeyboardButton('/add')
    itembtn5 = types.KeyboardButton('/delete')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
    bot.send_message(message.chat.id, 'Choose command:', reply_markup=markup, )


@bot.message_handler(commands=['start'])
def keyborad(message):
    keyboard_month(message, 'smmm')


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
        keyboard_y_or_n(message, text)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'name_yes':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Next step')
    elif call.data == 'name_no':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Try again')
        global new_user
        new_user = True


bot.polling()
