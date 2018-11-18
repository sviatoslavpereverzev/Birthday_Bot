from telebot import types
import calendar

MONTH = [['Декабрь', 'Январь', 'Февраль'], ['Март', 'Апрель', 'Май'], ['Июнь', 'Июль', 'Август'],
         ['Сентябрь', 'Октябрь', 'Ноябрь']]


def keyboard_y_or_n(message, text, bot):
    keyboard = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text='Правильно', callback_data='answer_yes')
    button_no = types.InlineKeyboardButton(text='Что-то не так... ', callback_data='answer_no')
    keyboard.add(button_yes, button_no)
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


def keyboard_day(message, text, month, bot):
    month = int(month)
    button = []
    i = 0
    cal = calendar.Calendar(firstweekday=0)
    keyboard = types.InlineKeyboardMarkup()
    for week in cal.monthdays2calendar(2000, month):
        button.append([])
        for day in week:
            button[i].append(
                types.InlineKeyboardButton(text='{}'.format((' ' if day[0] == False else day[0])),
                                           callback_data='day_{}'.format(day[0])))
        i += 1
    for week in button:
        keyboard.row(week[0], week[1], week[2], week[3], week[4], week[5], week[6])
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


def keyboard_month(message, text, bot):
    keyboard = types.InlineKeyboardMarkup()
    button = []
    i = 0
    for seasons in MONTH:
        button.append([])
        for month in seasons:
            button[i].append(types.InlineKeyboardButton(text='{}'.format(month),
                                                        callback_data='month_{}_{}'.format(month_number(month), month)))
        i += 1
    for seasons in button:
        keyboard.row(seasons[0], seasons[1], seasons[2])
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


def keyboard_command(message, bot):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('/all')
    itembtn2 = types.KeyboardButton('/week')
    itembtn3 = types.KeyboardButton('/month')
    itembtn4 = types.KeyboardButton('/add')
    itembtn5 = types.KeyboardButton('/delete')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
    bot.send_message(message.chat.id, 'Командуй!)', reply_markup=markup, )


def month_number(month):
    for season in MONTH:
        try:
            return 12 if (3 * MONTH.index(season) + season.index(month)) == 0 else (
                    3 * MONTH.index(season) + season.index(month))
        except:
            pass
