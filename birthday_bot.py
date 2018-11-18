from settings_bot import TOKEN
import telebot
import keyboards

# import time

bot = telebot.TeleBot(TOKEN)
new_user = False
last_update = ''
add_user_information = {}


@bot.message_handler(commands=['start'])
def start(message):
    keyboards.keyboard_command(message, bot)


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
        bot.send_message(message.chat.id, 'Я не знаю что ты от меня хочешь 😓\nВот что я умею:' )
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
