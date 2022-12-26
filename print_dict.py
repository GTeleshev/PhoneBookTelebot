from Notes import Notes
from tabulate import tabulate
import time

note = Notes()


data = note.get_all()
print(data)
tabdata = tabulate(data)
print(tabdata)
lst1 = [["Ключ", "Фамилия", "Имя", "Телефон","Описание"]]
for keys, val in data.items():
    lst1.append([keys, val["lastname"], val["firstname"], val["phone"], val["description"]])
print(tabulate(lst1))
lst = [['lel','lol','lal'],['1','2','3']]

print(tabulate(lst))

# curr = time.localtime()
# strtime = f'{curr.tm_year}.{curr.tm_mon}.{curr.tm_mday} - {curr.tm_hour}:{curr.tm_min}:{curr.tm_sec}'
# print(curr)
# print(strtime)


# Все записи:
# data_dict = note.get_all()
# print(type(data_dict))
# str_to_print = "Ключ \t Фамилия \t Имя \t Телефон \t Описание \n"
# for key, value in data_dict.items():
#     str_to_print += f"{key} \t {value['lastname']}  {value['firstname']}  {value['phone']}  {value['description']} \n"
#
# print(str_to_print)
# str_to_print1 = tabulate(data_dict)
# print(str_to_print)
# print(str_to_print1)
# from ConnectDb import ConnectDb
# conn = ConnectDb()
# lst = {1: {'lastname': 'ЛиСиЦин', 'firstname': 'Андрей', 'phone': '+74953757413', 'description': 'домашний'}}
# lst1 = conn.all_data_dict
#
# keys = lst.keys()
# print(keys)
# print(lst)
# print(lst1)
# for item in keys:
#     subdict = lst[item]
#     subkeys = subdict.keys()
#     print(f"ID: {item} : {lst[item]}")