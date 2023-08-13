# {"last_name": "Пупкин", "name": "Василий", "surname": "Степаныч", "tel_num": "+79143701845"}
# {"last_name": "Орленок", "name": "Егор", "surname": "Юрьевич", "tel_num": "+79243138022"}
# {"last_name": "Иванов", "name": "Иван", "surname": "Иванович", "tel_num": "8885557676"}
# {"last_name": "Петров", "name": "Иннокентий", "surname": "Витальевич", "tel_num": "2465265465462"}

# Заметка должна:
# содержать идентификатор, заголовок, тело заметки и дату/время создания или
# последнего изменения заметки.

import os
import json
from prettytable import PrettyTable
from datetime import datetime

# App constant settings
NOTE_BOOK_VERSION = '1.0'
NOTE_BOOK_FILE_NAME = "note_book.txt"
NOTE_BOOK_FILE_PATH = "" + NOTE_BOOK_FILE_NAME
NOTE_BOOK_TABLE_LEN = 60

# Titles
TITLE_NAME_NOTE_BOOK = "Заметки v."
TITLE_MENU = "МЕНЮ"

# Phone book table rows
LIST_TABLE_COLUMNS = (
    "ID",
    "Заголовок",
    "Текст заметки",
    "Дата",
    "Время"
)

# Menu items
MENU_ITEMS = (
    "Показать все заметки",
    "Добавить запись",
    "Удалить запись",
    "Выйти из программы"
)

# JSON note struct
JS_NOTE_ID = "id"
JS_NOTE_TITLE = "title"
JS_NOTE_BODY = "body"
JS_NOTE_DATE = "data"
JS_NOTE_TIME = "time"



def file_check_ok():
    if(os.path.exists(NOTE_BOOK_FILE_PATH) \
    and os.path.isfile(NOTE_BOOK_FILE_PATH)) \
    and (os.path.getsize(NOTE_BOOK_FILE_PATH) != 0):
        return True
    
    return False

def write_data(data:list):
    try:
        with open(NOTE_BOOK_FILE_PATH, "w", encoding="UTF-8") as file:
            for line_note in data:
                line = json.dumps(line_note, ensure_ascii=False) + '\n'
                file.write(line)
    except: 
        print(f'Возникли ошибки при чтении файла {NOTE_BOOK_FILE_PATH}')    

# Read phone book file
def read_data(data:list):
    data.clear()
    if(file_check_ok()):
        try:
            with open(NOTE_BOOK_FILE_PATH, "r", encoding="UTF-8") as file:
                for line in file:
                    jstring = line.strip()
                    note_line = json.loads(jstring)
                    data.append(note_line)
        except: 
            print(f'Возникли ошибки при чтении файла {NOTE_BOOK_FILE_PATH}')    
            return False
    else:
         print(f"Файл заметок (\"{NOTE_BOOK_FILE_PATH}\") пуст или не найден в дирректории!!!")    
         return False
            
    return True        

# Print one note as table 
def print_note_table(note:list):
        note_table = PrettyTable(LIST_TABLE_COLUMNS)
        note_table.add_row([                
                note[JS_NOTE_ID], 
                note[JS_NOTE_TITLE], 
                note[JS_NOTE_BODY], 
                note[JS_NOTE_DATE],
                note[JS_NOTE_TIME]
        ])
        print(note_table)

# Note book output to terminal         
def screen(data:list):
    itm_num = 0
    note_book_table = PrettyTable(LIST_TABLE_COLUMNS)

    if(read_data(data)):
        for idx in data:
            note_book_table.add_row([ 
                idx[JS_NOTE_ID], 
                idx[JS_NOTE_TITLE], 
                idx[JS_NOTE_BODY], 
                idx[JS_NOTE_DATE],
                idx[JS_NOTE_TIME]
            ])
    else:
        pass        
    
    print(note_book_table)   

# Delete entry in phone book
def delete_entry(data:list):
    list_len = len(data)
    note_book_table = PrettyTable(LIST_TABLE_COLUMNS)
    
    if file_check_ok():
        entry_id = int(input("Введите ID записи для удаления: "))
        for note_index in range(list_len):
            if (int(data[note_index][JS_NOTE_ID]) == entry_id):
                print('Вы действительно хотите удалить: ')
                print_note_table(data[note_index])
                user_answer = input('Да(Д) / Нет(Н) ?: ')       
                            
                if(user_answer.lower() == 'д'):
                    data.pop(note_index)
                    write_data(data)
                    break
                elif(user_answer.lower() == 'н'):
                    print("Удаление отменено, выходим в меню.")
                    break
                else:
                    print("Ответ не определён, выходим в меню.")
                    break
            elif(note_index == list_len - 1):
                print("ID заметки не найден!")
                break
    else:
        print("Ошибка удаления записи (Файл отсутствует либо пуст)")        

#Add new entry to phoe book
def add_entry(data:list):
    list_len = len(data) + 1
    entry = dict()
    
    # format_dict = {"last_name": "Пупкин", "name":"Василий", "surname":"Степаныч", "tel_num":"+79143701845"}
    title_name = input("Ведите Заголовок: ")
    note_text = input("Ведите Заметку: ")

    
    entry[JS_NOTE_ID] = str(list_len)
    entry[JS_NOTE_TITLE] = title_name
    entry[JS_NOTE_BODY] = note_text
    entry[JS_NOTE_DATE] = str(datetime.now().date())
    entry[JS_NOTE_TIME] = str(datetime.now().time())
    
    try:
        with open(NOTE_BOOK_FILE_PATH, "a", encoding="UTF-8") as file:
            line = json.dumps(entry, ensure_ascii=False) + '\n'
            file.write(line)
    except  : 
        print(f'Возникли ошибки при записи файла файла {NOTE_BOOK_FILE_PATH}')
        return
    
    print("Запись успешно добавлена")       

# Output menu to terminal
def menu():
    item_num = 0
    note_book_list = list()
    # need_exit  = False     

    # while not need_exit:
    while True:
        print()
        print(f"{'=' * int((NOTE_BOOK_TABLE_LEN / 2) - (len(TITLE_NAME_NOTE_BOOK) + 2))} {TITLE_NAME_NOTE_BOOK} {NOTE_BOOK_VERSION} {'=' * int((NOTE_BOOK_TABLE_LEN / 2) - 3)}")
        
        if(file_check_ok() == False or read_data(note_book_list) == False):
            print('Файл заметок пуст или отсутствует, для начала создайте заметку!')

        print(f"{'-' * int((NOTE_BOOK_TABLE_LEN / 2) - (len(TITLE_MENU) + 3))} {TITLE_MENU} {'-' * (int(NOTE_BOOK_TABLE_LEN / 2) + 2)}")
        


        for m_itm in range(len(MENU_ITEMS)):
            print(f'[{m_itm + 1}] {MENU_ITEMS[m_itm]}')
            
        print('-' * NOTE_BOOK_TABLE_LEN)
        
        item_num = int(input('Введите пункт меню: '))
        if item_num > len(MENU_ITEMS):
            print("Неверный ввод, повторите попытку!")
        else:
            if item_num == 1:
                if(read_data(note_book_list)):
                    screen(note_book_list)
                # print('-' * NOTE_BOOK_TABLE_LEN)

            elif item_num == 2:
                add_entry(note_book_list)
                read_data(note_book_list)
                screen(note_book_list)
                
            elif item_num == 3:
                delete_entry(note_book_list)
                screen(note_book_list)

            elif item_num == 4:
                exit()
 
        print('=' * NOTE_BOOK_TABLE_LEN)        
# Main app
def main():
    os.system('cls') # Clear terminal
    menu()


if __name__ == '__main__':
    main()
    # print(file_check())