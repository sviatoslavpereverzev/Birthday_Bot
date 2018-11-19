from settings_bot import TOKEN, MYSQLPASSWORD
import telebot
import keyboards
import mysql.connector
from mysql.connector import Error
# import time

bot = telebot.TeleBot(TOKEN)


class User(object):
    def __init__(self, from_user):
        self.id = from_user.id
        self.is_bot = from_user.is_bot
        self.name_user = from_user.first_name
        self.username = from_user.username
        self.last_name = from_user.last_name
        self.language_code = from_user.language_code

    def get_info(self):
        return self.id, self.is_bot, self.name_user, self.username, self.last_name, self.language_code

    def add_user_information(self):
        self.add_user_name = None
        self.add_user_date = None
        self.add_user_month = None

    def set_add_user_name(self, name):
        self.add_user_name = name

    def set_add_user_date(self, date):
        self.add_user_date = date

    def set_add_user_month(self, month):
        self.add_user_month = month

    def get_add_user_name(self):
        return self.add_user_name

    def get_add_user_date(self):
        return self.add_user_date

    def get_add_user_month(self):
        return self.add_user_month

    def add_new_user(self):
        self.add_new_user = False

    def set_add_new_user(self, bool):
        self.add_new_user = bool

    def get_add_new_user(self):
        return self.add_new_user

    def last_update(self):
        self.last_update = None

    def set_last_update(self, update):
        self.last_update = update

    def get_last_update(self):
        return self.last_update

class ConnectDb(object):
    def connected(self):
        try:
            self.connect = mysql.connector.connect(host='localhost',
                                           user='root',
                                           password=MYSQLPASSWORD)
            if self.connect.is_connected():
                print('Connected to MySQL database')

        except Error as e:
            print(e)

    def close_connect(self):
        self.connect.close()


# new_user = False
# last_update = ''
# add_user_information = {}


@bot.message_handler(commands=['start'])
def start(message):
    user = User(message.from_user)
    bot.send_message(message.chat.id, 'Привет {} {}'.format(message.from_user.first_name, message.from_user.last_name))
    db = ConnectDb()
    db.connect()


@bot.message_handler(commands=['all'])
def all_birthdays(message):
    bot.send_message(message.chat.id, 'Все дни рождения:')
    bot.send_message(message.chat.id, 'Я пока это не умею, но скоро научусь😋')


@bot.message_handler(commands=['week'])
def week_birthdays(message):
    bot.send_message(message.chat.id, 'Дни рождения на этой неделе:')
    bot.send_message(message.chat.id, 'Я пока это не умею, но скоро научусь😋')


@bot.message_handler(commands=['month'])
def month_birthdays(message):
    bot.send_message(message.chat.id, 'Дни рождения в этом месяце:')
    bot.send_message(message.chat.id, 'Я пока это не умею, но скоро научусь😋')


@bot.message_handler(commands=['add'])
def add_user(message):
    bot.send_message(message.chat.id, 'Добавим нового именинника: \nНапиши кто именинник?')
    global new_user
    new_user = True


@bot.message_handler(commands=['delete'])
def delete_user(message):
    bot.send_message(message.chat.id, 'Удаляем лишнее:')
    bot.send_message(message.chat.id, 'Я пока это не умею, но скоро научусь😋')


@bot.message_handler(content_types=['text'])
def last_updates(message):
    global last_update, add_user_information, new_user
    last_update = message.text
    if new_user:
        new_user = False
        add_user_information['name'] = last_update
        bot.send_message(message.chat.id, 'Именинник: {}'.format(add_user_information['name']))
        keyboards.keyboard_month(message, 'В каком месяце родился?', bot)
    else:
        bot.send_message(message.chat.id, 'Я не знаю что ты от меня хочешь 😓\nВот что я умею:')
        start(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    command = call.data.split('_')[0]
    value = call.data.split('_')[1]
    if command == 'answer':
        if value == 'yes':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Добавил 😌')


        elif value == 'no':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Давай по новой \nТак кто именинник?')
            global new_user
            new_user = True

    elif command == 'month':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Месяц: {}'.format(call.data.split('_')[-1]))
        add_user_information['month'] = [call.data.split('_')[1], call.data.split('_')[-1]]

        keyboards.keyboard_day(call.message, 'В какой день?', add_user_information['month'][0], bot)

    elif command == 'day':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='День: {}'.format(value))
        add_user_information['date'] = value
        user = 'Именинник: {}, месяц: {}, день: {}\n'.format(add_user_information['name'],
                                                             add_user_information['month'][1],
                                                             add_user_information['date'])
        keyboards.keyboard_y_or_n(call.message, (user, 'Все правильно? Добавляем?'), bot)


bot.polling()
