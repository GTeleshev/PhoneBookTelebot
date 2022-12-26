from Notes import Notes

notes = Notes()

PBVERSION = '1.1'

def get_notes():
    data_dict = notes.get_all()
    print("Ключ", "Фамилия", "Имя", "Телефон", "Описание", sep="\t")
    for key, value in data_dict.items():
        print(key, value['lastname'], value['firstname'], value['phone'], value['description'], sep="\t")

def add_record():
    data_list = []
    data_list.append(input('Введите фамилию: '))
    data_list.append(input('Введите имя: '))
    data_list.append(input('Введите телефон: '))
    data_list.append(input('Введите описание: '))
    print(data_list)
    notes.add_note(data_list)
    notes.end()


def export():
    while True:
        file_name = input('Введите имя файла (без расширения): ')
        file_type = input('Введите расширение (json / csv, json - по умолчанию): ')
        temp = notes.export_notes(file_name, file_type)
        if temp is not False:
            break


def import_data():
    while True:
        file_name = input('Введите имя файла (с расширением): ')
        file_type = input('Введите расширение (json / csv / sql, json - по умолчанию): ')
        temp = notes.import_notes(file_name, file_type)
        if temp is not False:
            notes.end()
            break

# def search(self, lastname):

def search():
    ln = input('Введите фамилию: ')
    data = notes.search(ln)
    if data == []:
        print('Запись не найдена')
    else:
        print(*data, sep="\n")


def delete_record():
    while True:
        id_ = input('Введите ID: ')
        if id_.isdigit():
            notes.delete_by_id(id_)
            notes.end()
            break

def purge_database():
    notes.clear_all()
    notes.end()

def exit_phonebook():
    notes.end()
    exit()

def check_menu():
    print('Работает функция')


def check_numeric(message, min_, max_):
    out = -100
    check = False
    while not check or out > max_ or out < min_:
        str_out = input(message)
        if not str_out.isdigit():
            check = False
        else:
            out = int(str_out)
            check = True
    return out


def main_menu():
    print(f"Телефонный справочник: {PBVERSION}")
    options = {1: "Добавление записей",
               2: "Вывод на экран",
               3: "Импорт",
               4: "Экспорт",
               5: "Удаление записей",
               6: "Поиск",
               7: "Завершить работу",
               8: "Очистка базы"}
    functions = {1: add_record,
             2: get_notes,
             3: import_data,
             4: export,
             5: delete_record,
             6: search,
             7: exit_phonebook,
             8: purge_database}
    for iter in options.keys():
        print(iter, options[iter])
    option = check_numeric("Выберите действие: ", 1, 8)
    print("Выбрано: ", options[option])
    functions[option]() # можно передавать без аргумента "()"

    user_dec = input('Продолжить - Enter, выйти - exit: ')
    if user_dec == 'exit':
        exit_phonebook()
    else:
        main_menu()
    return option


main_menu()