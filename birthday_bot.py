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
        self.db = mysql.connector.connect(host='localhost',
                                          user='root',
                                          database='Birthday_bot',
                                          password=MYSQLPASSWORD)

        try:
            if self.db.is_connected():
                print('Connected to MySQL database')

        except Error as e:
            print(e)

    # def close_connect(self):
    #     self.db.close()

    def is_there_a_user(self, id):
        sql = 'SELECT * FROM Users_Birthday_bot WHERE id = {}'.format(id)
        mycursor = self.db.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        if not myresult:
            print('Нет такого')
            return False
        print(myresult)
        return True

    def add_user_in_table_users(self, info):
        sql = 'INSERT INTO Users_Birthday_bot (first_name, last_name, id, username, is_bot, language_code) VALUES (%s, %s, %s, %s, %s, %s)'
        user = (info.first_name, info.last_name, info.id, info.username, info.is_bot, info.language_code)
        mycursor = self.db.cursor()
        mycursor.execute(sql, user)
        self.db.commit()
        return True

    def add_user_in_addition_data(self, id):
        sql = 'INSERT INTO Addition_data (id, add_user) VALUES ({}, False)'.format(id)
        mycursor = self.db.cursor()
        mycursor.execute(sql)
        self.db.commit()
        return True

    def set_addition_data(self, column, value, id):
        sql = 'UPDATE Addition_data SET {} = "{}" WHERE id = {}'.format(column, value, id)
        mycursor = self.db.cursor()
        mycursor.execute(sql)
        self.db.commit()
        return True

    def get_addition_data(self, id):
        sql = 'SELECT  * FROM Addition_data Where id = {}'.format(id)
        mycursor = self.db.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchone()
        result = {}
        result['id'] = myresult[0]
        result['add_user'] = myresult[1]
        result['name'] = myresult[2]
        result['month_int'] = myresult[3]
        result['month_str'] = myresult[4]
        result['day'] = myresult[5]
        result['year_of_birth'] = myresult[6]
        result['next_function'] = myresult[7]
        return result

    # def get_addition_data(self, id):
    #     sql = 'SELECT  add_user FROM Addition_data Where id = {}'.format(id)
    #     mycursor = self.db.cursor()
    #     mycursor.execute(sql)
    #     myresult = mycursor.fetchone()

    def add_birthday(self, id):
        birthday = db.get_addition_data(id)
        sql = 'INSERT INTO Birthdays (id, name, month_int, month_str, day) VALUES (%s, %s, %s, %s, %s)'
        mycursor = self.db.cursor()
        user = (birthday['id'], birthday['name'], birthday['month_int'], birthday['month_str'], birthday['day'])
        mycursor.execute(sql, user)
        self.db.commit()

    def get_birthday(self):
        mycursor = self.db.cursor()
        sql = 'SELECT name, month_str, day FROM Birthday_bot.id_{};'.format(user.get_user_id())
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult

    # def create_user_db(self, id):
    #     try:
    #         mycursor = self.db.cursor()
    #         sql = 'CREATE TABLE id_{} (name VARCHAR(255), month_int INTEGER(2), month_str VARCHAR(25), day INTEGER(2), year_of_birth INTEGER(4), remind_month BOOL DEFAULT 0, remind_week BOOL DEFAULT 0, remind_day BOOL DEFAULT 0)'.format(
    #             id)
    #         mycursor.execute(sql)
    #     except mysql.connector.errors.ProgrammingError:
    #         print('Таблица id_{} уже есть!'.format(id))


db = ConnectDb()
db.connected()


@bot.message_handler(commands=['start'])
def start(message):
    if db.is_there_a_user(message.from_user.id) is False:
        db.add_user_in_table_users(message.from_user)
        db.add_user_in_addition_data(message.from_user.id)

    bot.send_message(message.chat.id,
                     'Привет, {} {} 👋'.format(message.from_user.first_name, message.from_user.last_name))


@bot.message_handler(commands=['commands'])
def commands(message):
    bot.send_message(message.chat.id, 'Вот что я умею:')
    keyboards.keyboard_command(message, bot)


@bot.message_handler(commands=['all'])
def all_birthdays(message):
    pass
    # global user, db
    # user = User(message.from_user)
    # db = ConnectDb()
    # db.connected()
    # bot.send_message(message.chat.id, 'Все дни рождения:')
    # birthdays = db.get_birthday()
    # for result in birthdays:
    #     bot.send_message(message.chat.id,
    #                      '{}'.format(
    #                          str(result).replace(',', '').replace("'", '').replace('(', '').replace(')', '')))


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
    db.set_addition_data('add_user', '1', message.from_user.id)
    # global user, db
    # try:
    #     # get user scenario status from db or Global Static Config Class
    #     user.set_add_new_user(True)
    # except NameError:
    #     user = User(message.from_user)
    #     # db = ConnectDb()
    #     user.set_add_new_user(True)

    bot.send_message(message.chat.id, 'Добавим нового именинника: \nНапиши кто именинник?')


@bot.message_handler(commands=['delete'])
def delete_user(message):
    bot.send_message(message.chat.id, 'Удаляем лишнее:')
    bot.send_message(message.chat.id, 'Я пока это не умею, но скоро научусь😋')


@bot.message_handler(content_types=['text'])
def last_updates(message):
    if bool(db.get_addition_data(message.from_user.id)['add_user']):
        db.set_addition_data('add_user', '0', message.from_user.id)
        db.set_addition_data('name', message.text, message.from_user.id)
        bot.send_message(message.chat.id, 'Именинник: {}'.format(message.text))
        keyboards.keyboard_month(message, 'В каком месяце родился?', bot)

    else:
        bot.send_message(message.chat.id, 'Я не знаю что ты от меня хочешь 😓\nВот что я умею:')
        commands(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    command = call.data.split('_')[0]
    value = call.data.split('_')[1]
    if command == 'answer':
        if value == 'yes':
                db.add_birthday(call.message.chat.id)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Добавил 😌')


        elif value == 'no':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Давай по новой \nТак кто именинник?')
            global new_user
            new_user = True

    elif command == 'month':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Месяц: {}'.format(call.data.split('_')[-1]))
        db.set_addition_data('month_int', call.data.split('_')[1], call.message.chat.id)
        db.set_addition_data('month_str', call.data.split('_')[2], call.message.chat.id)
        keyboards.keyboard_day(call.message, 'В какой день?', call.data.split('_')[1], bot)

    elif command == 'day':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='День: {}'.format(value))
        db.set_addition_data('day', call.data.split('_')[1], call.message.chat.id)

        user_add = 'Именинник: {}, месяц: {}, день: {}\n'.format(db.get_addition_data(call.message.chat.id)['name'],
                                                                 db.get_addition_data(call.message.chat.id)[
                                                                     'month_str'],
                                                                 db.get_addition_data(call.message.chat.id)['day'])

        keyboards.keyboard_y_or_n(call.message, (user_add, 'Все правильно? Добавляем?'), bot)


def main():
    # db = ConnectDb()
    # db.connected()
    # db_connect = mysql.connector.connect(host='localhost',
    #                                               user='root',
    #                                               database='Birthday_bot',
    #                                               password=MYSQLPASSWORD)
    bot.polling()


if __name__ == '__main__':
    main()
