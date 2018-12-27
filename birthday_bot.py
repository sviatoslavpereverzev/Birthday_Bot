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
        result['delete_user'] = myresult[2]
        result['name'] = myresult[3]
        result['month_int'] = myresult[4]
        result['month_str'] = myresult[5]
        result['day'] = myresult[6]
        result['offset'] = myresult[7]
        return result

    def add_birthday(self, id):
        birthday = db.get_addition_data(id)
        sql = 'INSERT INTO Birthdays (id, name, month_int, month_str, day) VALUES (%s, %s, %s, %s, %s)'
        mycursor = self.db.cursor()
        user = (birthday['id'], birthday['name'], birthday['month_int'], birthday['month_str'], birthday['day'])
        mycursor.execute(sql, user)
        self.db.commit()
        return True

    def get_birthday(self, sql_filter, offset, id):
        if sql_filter == 'all':
            sql = 'SELECT name, month_str, day FROM Birthdays WHERE id = {} ORDER BY name LIMIT 10 OFFSET {}'.format(id, offset)
        else:
            month = datetime.date.today().month
            today = datetime.date.today().day
            if sql_filter == 'week':
                sql = 'SELECT name, month_str, day FROM Birthdays WHERE id = {} AND month_int = {} AND day BETWEEN {} and {} ORDER BY name LIMIT 10 OFFSET {}'.format(
                    id, month, today, today + 7, offset)
            else:
                sql = 'SELECT name, month_str, day FROM Birthdays WHERE id = {} AND month_int = {} ORDER BY name LIMIT 10 OFFSET {}'.format(
                    id, month, offset)

        mycursor = self.db.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult

    def delete_birthday(self, name, month_str, day, user_id):
        sql = 'DELETE FROM Birthdays WHERE id = {} AND name = "{}" AND month_str = "{}" AND day = {}'.format(user_id,
                                                                                                             name,
                                                                                                             month_str,
                                                                                                             day)
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
        for birthday in birthdays:
            birthday = str(birthday).replace(',', '').replace("'", '').replace('(', '').replace(')', '')
            birthdays_list = birthdays_list + str(offset + 1) + '. ' + birthday + '\n'
            offset += 1
        return birthdays_list

    def get_list_of_birthdays(self, message, sql_filter, user_id):
        offset = db.get_offset(user_id)
        birthdays = db.get_birthday(sql_filter, offset, user_id)
        birthdays_list = db.list_change(birthdays, offset)
        next_birthday = db.get_birthday(sql_filter, offset + 10, user_id)
        if not next_birthday:
            try:
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                      text=birthdays_list)
            except:
                bot.send_message(message.chat.id, birthdays_list)
        else:
            db.set_addition_data('offset', offset + 10, user_id)
            keyboard = keyboards.keybord_next(sql_filter)
            try:
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                      text=birthdays_list, reply_markup=keyboard)
            except:
                bot.send_message(message.chat.id, birthdays_list, reply_markup=keyboard)

    def get_birthdays_for_deletion(self, name, offset, user_id):
        sql = 'SELECT name, month_str, day FROM Birthdays WHERE id = {} and name REGEXP "{}" LIMIT 10 OFFSET {}'.format(
            user_id, name, offset)
        mycursor = self.db.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult

    def get_list_of_birthdays_for_deletion(self, message, name, user_id):
        offset = db.get_offset(user_id)
        birthdays = db.get_birthdays_for_deletion(name, offset, user_id)
        next_birthday = db.get_birthdays_for_deletion(name, offset + 10, user_id)
        if not next_birthday:
            if offset == 0 and not birthdays:
                bot.send_message(message.chat.id, 'Я никого не нашел 🤷‍♂️')
            else:
                if len(birthdays) == 1:
                    value = 'delete_{}_{}_{}'.format(birthdays[0][0], birthdays[0][1], birthdays[0][2])
                    text = 'Убираем "{}" из списка именинников?😳'.format(birthdays[0][0])
                    keyboards.keyboard_delete_y_or_n(message, text, bot, value, 1)
                else:
                    from telebot import types
                    buttons = []
                    keyboard = types.InlineKeyboardMarkup()
                    for names in birthdays:
                        birthday = str(names).replace(',', '').replace("'", '').replace('(', '').replace(')', '')
                        text = str(offset + 1) + '. ' + birthday
                        offset += 1
                        buttons.append(
                            types.InlineKeyboardButton(text=text,
                                                       callback_data='delete_{}_{}_{}'.format(names[0], names[1],
                                                                                              names[2])))
                    for button in buttons:
                        keyboard.add(button)
                    bot.send_message(message.chat.id, 'Выбирай:', reply_markup=keyboard)


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
    # Сделать выборку имен с сортировкой имени по алфавиту
    db.set_addition_data('offset', 0, message.from_user.id)
    db.get_list_of_birthdays(message, 'all', message.from_user.id)


@bot.message_handler(commands=['week'])
def week_birthdays(message):
    bot.send_message(message.chat.id, 'Дни рождения на ближайшие 7 дней:')
    db.set_addition_data('offset', 0, message.from_user.id)
    db.get_list_of_birthdays(message, 'week', message.from_user.id)


@bot.message_handler(commands=['month'])
def month_birthdays(message):
    bot.send_message(message.chat.id, 'Дни рождения в этом месяце:')
    db.set_addition_data('offset', 0, message.from_user.id)
    db.get_list_of_birthdays(message, 'month', message.from_user.id)


@bot.message_handler(commands=['add'])
def add_user(message):
    db.set_addition_data('add_user', '1', message.from_user.id)
    db.set_addition_data('delete_user', '0', message.from_user.id)
    bot.send_message(message.chat.id, 'Добавим нового именинника: \nНапиши кто именинник?')


@bot.message_handler(commands=['delete'])
def delete_user(message):
    bot.send_message(message.chat.id, 'Удаляем лишнее: \nНапиши имя иммениника')
    db.set_addition_data('offset', 0, message.from_user.id)
    db.set_addition_data('delete_user', '1', message.from_user.id)
    db.set_addition_data('add_user', '0', message.from_user.id)


@bot.message_handler(content_types=['text'])
def text(message):
    if bool(db.get_addition_data(message.from_user.id)['add_user']):
        db.set_addition_data('add_user', '0', message.from_user.id)
        db.set_addition_data('name', message.text, message.from_user.id)
        bot.send_message(message.chat.id, 'Именинник: {}'.format(message.text))
        keyboards.keyboard_month(message, 'В каком месяце родился?', bot)

    elif bool(db.get_addition_data(message.from_user.id)['delete_user']):
        db.set_addition_data('delete_user', '0', message.from_user.id)
        db.get_list_of_birthdays_for_deletion(message, message.text, message.from_user.id)

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
        if call.data[5:] == 'all':
            db.get_list_of_birthdays(call.message, 'all', call.from_user.id)
        elif call.data[5:] == 'week':
            db.get_list_of_birthdays(call.message, 'week', call.from_user.id)
        elif call.data[5:] == 'month':
            db.get_list_of_birthdays(call.message, 'month', call.from_user.id)

    elif command == 'delete':
        keyboards.keyboard_delete_y_or_n(call.message, 'Убираем "{}" из списка именинников?😳'.format(value), bot,
                                         call.data)

    elif command == 'deleting':
        if value == 'yes':
            name = call.data.split('_')[-3]
            month_str = call.data.split('_')[-2]
            day = call.data.split('_')[-1]
            db.delete_birthday(name, month_str, day, call.from_user.id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Удалил😎')
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Ok, оставляем☺️')


def main():
    bot.polling()


if __name__ == '__main__':
    main()
