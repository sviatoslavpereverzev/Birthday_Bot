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
        self.first_name = from_user.first_name
        self.username = from_user.username
        self.last_name = from_user.last_name
        self.language_code = from_user.language_code

    def get_user_info(self):
        user_info = {'id': self.id, 'is_bot': self.is_bot, 'first_name': self.first_name, 'username': self.username,
                     'last_name': self.last_name, 'language_code': self.language_code}
        return user_info

    def get_user_id(self):
        return self.id

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
            self.db = mysql.connector.connect(host='localhost',
                                              user='root',
                                              database='Birthday_bot',
                                              password=MYSQLPASSWORD)
            if self.db.is_connected():
                print('Connected to MySQL database')

        except Error as e:
            print(e)

    def close_connect(self):
        self.db.close()

    def is_there_a_user(self, id):
        sql_select_user = 'SELECT * FROM Users_Birthday_bot WHERE id = {}'.format(id)
        mycursor = self.db.cursor()
        mycursor.execute(sql_select_user)
        myresult = mycursor.fetchall()
        if not myresult:
            print('Нет такого')
            return True
        print(myresult)
        return False

    def add_user_in_table_users(self, user_info):
        sql_add_user = 'INSERT INTO Users_Birthday_bot (first_name, last_name, id, username, is_bot, language_code) VALUES (%s, %s, %s, %s, %s, %s)'
        user = (user_info['first_name'], user_info['last_name'], user_info['id'], user_info['username'],
                user_info['is_bot'], user_info['language_code'])
        mycursor = self.db.cursor()
        mycursor.execute(sql_add_user, user)
        self.db.commit()
        return True

    def add_birthday(self, user):
        mycursor = self.db.cursor()
        sql = 'INSERT INTO id_{} (name, month_int, month_str, day) VALUES (%s, %s, %s, %s)'.format(user.get_user_id())
        user = (user.get_add_user_name(), int(user.get_add_user_month()[0]), user.get_add_user_month()[1],
                int(user.get_add_user_date()))
        mycursor.execute(sql, user)
        self.db.commit()

    def get_birthday(self):
        mycursor = self.db.cursor()
        sql = 'SELECT name, month_str, day FROM Birthday_bot.id_{};'.format(user.get_user_id())
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult


@bot.message_handler(commands=['start'])
def start(message):
    global user, db
    user = User(message.from_user)
    db = ConnectDb()
    db.connected()
    user_info = user.get_user_info()
    if db.is_there_a_user(user_info['id']):
        db.add_user_in_table_users(user_info)
    # db.close_connect()
    bot.send_message(message.chat.id,
                     'Привет {} {}'.format(message.from_user.first_name, message.from_user.last_name))


@bot.message_handler(commands=['commands'])
def commands(message):
    bot.send_message(message.chat.id, 'Вот что я умею:')
    keyboards.keyboard_command(message, bot)


@bot.message_handler(commands=['all'])
def all_birthdays(message):
    bot.send_message(message.chat.id, 'Все дни рождения:')
    birthdays = db.get_birthday()
    for result in birthdays:
        bot.send_message(message.chat.id,
                         '{}'.format(str(result).replace(',', '').replace("'", '').replace('(', '').replace(')', '')))


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
    global user, db
    try:
        user.set_add_new_user(True)
    except NameError:
        user = User(message.from_user)
        db = ConnectDb()
        user.set_add_new_user(True)

    bot.send_message(message.chat.id, 'Добавим нового именинника: \nНапиши кто именинник?')


@bot.message_handler(commands=['delete'])
def delete_user(message):
    bot.send_message(message.chat.id, 'Удаляем лишнее:')
    bot.send_message(message.chat.id, 'Я пока это не умею, но скоро научусь😋')


@bot.message_handler(content_types=['text'])
def last_updates(message):
    global user, db
    user.set_last_update(message.text)
    if user.get_add_new_user():
        user.set_add_new_user(False)
        user.set_add_user_name(user.get_last_update())
        bot.send_message(message.chat.id, 'Именинник: {}'.format(user.get_add_user_name()))
        keyboards.keyboard_month(message, 'В каком месяце родился?', bot)
    else:
        bot.send_message(message.chat.id, 'Я не знаю что ты от меня хочешь 😓\nВот что я умею:')
        start(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global user, db
    command = call.data.split('_')[0]
    value = call.data.split('_')[1]
    if command == 'answer':
        if value == 'yes':
            db.add_birthday(user)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Добавил 😌')


        elif value == 'no':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Давай по новой \nТак кто именинник?')
            global new_user
            new_user = True

    elif command == 'month':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Месяц: {}'.format(call.data.split('_')[-1]))
        user.set_add_user_month([call.data.split('_')[1], call.data.split('_')[-1]])
        month = user.get_add_user_month()[0]
        keyboards.keyboard_day(call.message, 'В какой день?', month, bot)

    elif command == 'day':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='День: {}'.format(value))
        user.set_add_user_date(value)
        user_add = 'Именинник: {}, месяц: {}, день: {}\n'.format(user.get_add_user_name(),
                                                                 user.get_add_user_month()[1],
                                                                 user.get_add_user_date())

        keyboards.keyboard_y_or_n(call.message, (user_add, 'Все правильно? Добавляем?'), bot)


def main():
    bot.polling()


if __name__ == '__main__':
    main()
