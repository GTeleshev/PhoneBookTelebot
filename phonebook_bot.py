from telebot import TeleBot, types
import Notes
import time

TOKEN = input('Введите бот TOKEN (либо получить через BotFather: https://telegram.me/BotFather): ')

bot = TeleBot(TOKEN)
note = Notes.Notes()
dct = {}


def greeting(msg: types.Message):
    bot.send_message(chat_id=msg.from_user.id, text='\U0001F680 Здравствуйте, функции бота следующие:\n'
                                                    '/start - запуск этого диалога\n'
                                                    '/printall - вывод всей базы\n'
                                                    '/search - поиск по фамилии\n'
                                                    '/export - экспорт всей базы\n'
                                                    '/add - добавление записи\n'
                                                    '/delete - удаление записи\n'
                                                    '/log - печать лога действий пользователя')


def get_time():
    curr = time.localtime()
    strtime = f'{curr.tm_year}.{curr.tm_mon}.{curr.tm_mday} - {curr.tm_hour}:{curr.tm_min}:{curr.tm_sec}'
    return strtime


def log_write(message, string_to_write):
    curr_time = get_time()
    full_str = f'{curr_time}: {string_to_write}\n'
    dct[message.id] = full_str
    doc = open('log.txt', 'a')
    with doc as d:
        doc.write(full_str)


# Функция для сохранения документа, отправленного боту
@bot.message_handler(content_types=['document'])
def answer(msg: types.Message):
    log_write(msg, 'file saved')
    filename = msg.document.file_name
    with open(filename, 'wb') as file:
        file.write(bot.download_file(bot.get_file(msg.document.file_id).file_path))
    bot.send_message(chat_id=msg.from_user.id, text=f'Файл сохранён {msg.document.file_id}')


@bot.message_handler(commands=['start', 'help'])
def answer(msg: types.Message):
    log_write(msg, 'start called')
    greeting(msg)


@bot.message_handler(commands=['printall'])
def answer(msg: types.Message):
    log_write(msg, 'printall called')
    data_dict = note.get_all()
    print(type(data_dict))
    str_to_print = "Ключ \t Фамилия \t Имя \t Телефон \t Описание \n"
    for key, value in data_dict.items():
        str_to_print += f"{key} \t {value['lastname']}  {value['firstname']}  {value['phone']}  {value['description']} \n"
    print(str_to_print)
    bot.send_message(chat_id=msg.from_user.id, text=str_to_print)


@bot.message_handler(commands=['search'])
def answer(msg: types.Message):
    log_write(msg, 'search called')
    mess = bot.send_message(chat_id=msg.from_user.id, text=f'Введите фамилию:')
    bot.register_next_step_handler(mess, return_search)


def return_search(msg: types.Message):
    str_msg = str(msg.text)
    bot.send_message(chat_id=msg.from_user.id, text=f'Ищем: {str_msg}')
    reply_txt = note.search(str_msg)
    if reply_txt != []:
        ostring = 'Ключ \t Фамилия \t Имя \t Телефон \t Описание \n'
        for listdicts in reply_txt:
            for key, value in listdicts.items():
                ostring += f'{key} \t \t {value["lastname"]} \t {value["firstname"]} {value["phone"]} {value["description"]}\n'
        print(ostring)
        log_write(msg, f'search for: {str_msg}')
        bot.send_message(chat_id=msg.from_user.id, text={ostring})
    else:
        log_write(msg, f'empty search for: {str_msg}')
        bot.send_message(chat_id=msg.from_user.id, text='Запись с такой фамилией не найдена')
    return str_msg


@bot.message_handler(commands=['export'])
def answer(msg: types.Message):
    log_write(msg, 'export called')
    filename = 'telegram_export'
    filetype = 'csv'
    fullname = filename + '.' + filetype
    note.export_notes(filename, filetype)
    bot.send_message(chat_id=msg.from_user.id, text=f'Сохранено как: {fullname}')
    document = open(fullname, encoding='utf-8')
    bot.send_document(chat_id=msg.from_user.id, document=document)


@bot.message_handler(commands=['add'])
def answer(msg: types.Message):
    log_write(msg, 'add called')
    global lst
    lst = []
    bot.send_message(chat_id=msg.from_user.id, text='Введите фамилию')
    bot.register_next_step_handler(msg, call_lastname)


def call_lastname(msg: types.Message):
    lst.append(msg.text)
    bot.send_message(chat_id=msg.from_user.id, text='Введите имя')
    bot.register_next_step_handler(msg, call_firstname)


def call_firstname(msg: types.Message):
    lst.append(msg.text)
    bot.send_message(chat_id=msg.from_user.id, text='Введите телефон')
    bot.register_next_step_handler(msg, call_phone)


def call_phone(msg: types.Message):
    lst.append(msg.text)
    bot.send_message(chat_id=msg.from_user.id, text='Введите описание')
    bot.register_next_step_handler(msg, call_description)


def call_description(msg: types.Message):
    lst.append(msg.text)
    bot.send_message(chat_id=msg.from_user.id, text=f'{" ".join(lst)}')
    note.add_note(lst)
    note.end()
    print('post processing lst', lst)


@bot.message_handler(commands=['delete'])
def answer(msg: types.Message):
    log_write(msg, 'delete called')
    bot.send_message(chat_id=msg.from_user.id, text='Введите ключ записи для удаления')
    bot.register_next_step_handler(msg, call_id)


def call_id(msg: types.Message):
    id = msg.text
    note.delete_by_id(id)
    note.end()


@bot.message_handler(commands=['log'])
def answer(msg: types.Message):
    log_write(msg, 'log called')
    bot.send_message(chat_id=msg.from_user.id, text='Вывожу лог')
    print(dct)
    text_to_return = ""
    for keys, values in dct.items():
        text_to_return += f"{values}\n"
    bot.send_message(chat_id=msg.from_user.id, text=f'{text_to_return}')
    doc = open('log.txt', 'r')
    with doc as d:
        bot.send_document(chat_id=msg.from_user.id, document=d)


@bot.message_handler()
def answer(msg: types.Message):
    greeting(msg)


bot.polling()
