from settings_bot import TOKEN, MYSQLPASSWORD
import telebot
import keyboards
import mysql.connector
from mysql.connector import Error
import datetime

bot = telebot.TeleBot(TOKEN)


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
        result['offset'] = myresult[6]
        return result

    def add_birthday(self, id):
        birthday = db.get_addition_data(id)
        sql = 'INSERT INTO Birthdays (id, name, month_int, month_str, day) VALUES (%s, %s, %s, %s, %s)'
        mycursor = self.db.cursor()
        user = (birthday['id'], birthday['name'], birthday['month_int'], birthday['month_str'], birthday['day'])
        mycursor.execute(sql, user)
        self.db.commit()
        return True

    def get_birthday(self, filter, offset, id):
        if filter == 'all':
            sql = 'SELECT name, month_str, day FROM Birthdays WHERE id = {}  LIMIT 10 OFFSET {}'.format(id, offset)
        else:
            month = datetime.date.today().month
            today = datetime.date.today().day
            if filter == 'week':
                sql = 'SELECT name, month_str, day FROM Birthdays WHERE id = {} AND month_int = {} AND day BETWEEN {} and {}'.format(
                    id, month, today, today + 7)
            else:
                sql = 'SELECT name, month_str, day FROM Birthdays WHERE id = {} AND month_int = {}'.format(id, month)

        mycursor = self.db.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult

    def deletr_birhday(self, name, id):
        sql = 'DELETE FROM Birthdays WHERE id = {} AND name = {}'.format(id, name)
        mycursor = self.db.cursor()
        mycursor.execute(sql)
        self.db.commit()
        return True

    def get_offset(self, id):
        sql = 'SELECT offset FROM Addition_data Where id = {}'.format(id)
        mycursor = self.db.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchone()
        offset = int(str(myresult).replace('(', '').replace(',', '').replace(')', ''))
        return offset

    def list_change(self, birthdays, offset):
        birthdays_list = ''
        offset
        for birthday in birthdays:
            birthday = str(birthday).replace(',', '').replace("'", '').replace('(', '').replace(')', '')
            birthdays_list = birthdays_list + str(offset + 1) + '. ' + birthday + '\n'
            offset += 1
        return birthdays_list


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
    birthdays = db.get_birthday('all', 0, message.from_user.id)
    db.set_addition_data('offset', 0, message.from_user.id)
    birthdays_list = db.list_change(birthdays, 0)
    next_birthday = db.get_birthday('all', 0 + 11, message.from_user.id)
    if not next_birthday:
        bot.send_message(message.chat.id, birthdays_list)
    else:
        offset = db.get_offset(message.from_user.id)
        db.set_addition_data('offset', offset + 10, message.from_user.id)
        keyboards.keybord_next(message, bot, birthdays_list)


@bot.message_handler(commands=['week'])
def week_birthdays(message):
    bot.send_message(message.chat.id, 'Дни рождения на ближайшие 7 дней:')
    birthdays = db.get_birthday('week', message.from_user.id)
    for result in birthdays:
        bot.send_message(message.chat.id,
                         '{}'.format(
                             str(result).replace(',', '').replace("'", '').replace('(', '').replace(')', '')))


@bot.message_handler(commands=['month'])
def month_birthdays(message):
    bot.send_message(message.chat.id, 'Дни рождения в этом месяце:')
    birthdays = db.get_birthday('month', message.from_user.id)
    for result in birthdays:
        bot.send_message(message.chat.id,
                         '{}'.format(
                             str(result).replace(',', '').replace("'", '').replace('(', '').replace(')', '')))


@bot.message_handler(commands=['add'])
def add_user(message):
    db.set_addition_data('add_user', '1', message.from_user.id)
    bot.send_message(message.chat.id, 'Добавим нового именинника: \nНапиши кто именинник?')


@bot.message_handler(commands=['delete'])
def delete_user(message):
    bot.send_message(message.chat.id, 'Удаляем лишнее: \nНапиши имя иммениника')
    bot.send_message(message.chat.id, 'Я пока это не умею, но скоро научусь😋')


@bot.message_handler(content_types=['text'])
def text(message):
    # try:
    if bool(db.get_addition_data(message.from_user.id)['add_user']):
        db.set_addition_data('add_user', '0', message.from_user.id)
        db.set_addition_data('name', message.text, message.from_user.id)
        bot.send_message(message.chat.id, 'Именинник: {}'.format(message.text))
        keyboards.keyboard_month(message, 'В каком месяце родился?', bot)

    else:
        bot.send_message(message.chat.id, 'Я не знаю что ты от меня хочешь 😓\nВот что я умею:')
        commands(message)
    # except:
    #     bot.send_message(message.chat.id, 'Чё это вообще такое? 😳\nВот что я умею:')
    #     commands(message)



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
            db.set_addition_data('add_user', '1', call.message.chat.id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Давай по новой \nТак кто именинник?')


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
    elif command == 'next':
        if call.data[5:] == 'all_birthdays':
            offset = db.get_offset(call.from_user.id)
            birthdays = db.get_birthday('all', offset, call.from_user.id)
            birthdays_list = db.list_change(birthdays, offset)
            next_birthday = db.get_birthday('all', offset + 11, call.from_user.id)
            if not next_birthday:
                bot.send_message(call.message.chat.id, birthdays_list)
            else:
                offset = db.get_offset(call.from_user.id)
                db.set_addition_data('offset', offset + 10, call.from_user.id)
                keyboards.keybord_next(call.message, bot, birthdays_list)


def main():
    bot.polling()


if __name__ == '__main__':
    main()
