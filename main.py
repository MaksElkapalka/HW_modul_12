from collections import UserDict
from datetime import datetime
import pickle

class Field:

    def __init__(self, value):
        self.value = value

    def __getitem__(self, key=None):
        return self.value

    def __setitem__(self, key, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        self.value = name
        
class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and int(value):
            self.value = value
        else:
            raise ValueError
        
    def __setitem__(self, key, value):
        if len(value) == 10 and int(value):
            self.value = value
        else:
            raise ValueError
        
class Birthday(Field):
    def __init__(self, value):
        if value is None:
            self.value = None
        else:
            try:
                valid = datetime.strptime(str(value), '%d.%m.%Y')
                self.value = value
            except ValueError:
                print(f'ValueError: enter date of birth in the format "DD.MM.YYYY"')

    def __setitem__(self, key, value):
        try:
            valid = datetime.strptime(str(value), '%d.%m.%Y')
            self.value = value
        except ValueError:
            print(f'ValueError: enter date of birth in the format "DD.MM.YYYY"')
    

class Record:
    
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)
    
    def save_decorator(func): # зберігає зміни в файлі
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            book.save_to_file()
        return wrapper

    @save_decorator
    def add_phone(self, value):
        phone = Phone(value)
        self.phones.append(phone)

    @save_decorator
    def remove_phone(self, value):
        result = []
        for i in self.phones:
            if str(i) != value:
                result.append(i)            
        self.phones = result    
    
    @save_decorator
    def edit_phone(self, old_phone, new_phone):
        valid_phone = Phone(new_phone)
        result = []
        flag = True

        for i in self.phones:
            if str(i) == old_phone:
                result.append(valid_phone)
                flag = False
            else:
                result.append(i)

        self.phones = result
        if flag:
            raise ValueError

    def find_phone(self, value):
        for i in self.phones:
            if str(i) == value:
                return i

    @save_decorator       
    def add_birthday(self, value):
        self.birthday = Birthday(value)

    def days_to_birthday(self):
        if str(self.birthday) != 'None':
            birthday = datetime.strptime(str(self.birthday), '%d.%m.%Y')
            current_date = datetime.now()
            next_birthday = datetime(current_date.year, birthday.month, birthday.day)
            if current_date > next_birthday:
                next_birthday = datetime(current_date.year + 1, birthday.month, birthday.day)
            days_until_birthday = (next_birthday - current_date).days
            return days_until_birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def __init__(self, filename='book.bin'):
        super().__init__()
        self.filename = filename
        self.load_from_file()

    def add_record(self, value):
        self.data[str(value.name)] = value
        self.save_to_file()       

    def find(self, name):
        name = name.title()
        return self.data.get(name)

    def search(self, value= None): # пошук за за кількома цифрами номера телефону або літерами імені
        if value:
            data_match = str()
            value = value.lower()
            for _, record in book.data.items():
                phon = str([str(i) for i in record.phones])
                if value in str(record.name).lower() or value in phon:
                    data_match += f'{record}\n'
            print(data_match)
        
    def delete(self, name):
        try:
            del self.data[name]
            self.save_to_file()
        except KeyError:
            return None
        
    def iterator(self, iter_num=1):
        values = list(self.data.values())
        total_items = len(self.data)

        for i in range(0, total_items, iter_num):
            page_str = str()
            chunk_values = values[i:i + iter_num]

            for value in chunk_values:
                page_str += f'{str(value)}\n'
            
            yield page_str

    def save_to_file(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self):
        try:
            with open(self.filename, 'rb') as file:
                data = pickle.load(file)
                if data:
                    self.data = data
        except FileNotFoundError:
            print('A new file has been created')
                

book = AddressBook()

# # Створення та додавання нового запису для John
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.birthday = "20.02.2022"
# john_record.add_phone("5555555555")
# book.add_record(john_record)

# # Створення та додавання нового запису для Vasia
# vasia_record = Record("Vasia")
# vasia_record.add_phone("1234567890")
# book.add_record(vasia_record)

# # Створення та додавання нового запису для Sasha
# sasha_record = Record("Sasha", '14.02.1989')
# sasha_record.add_phone("1234567890")
# book.add_record(sasha_record)

# # Створення та додавання нового запису для Ibragim
# ibragim_record = Record("Ibragim")
# ibragim_record.add_phone("1234567890")
# book.add_record(ibragim_record)

# # Створення та додавання нового запису для Sveta
# sveta_record = Record("Sveta", "15.12.1987")
# sveta_record.add_phone("1234567890")
# book.add_record(sveta_record)

# # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# jane_record.add_birthday('11.05.1999')
# book.add_record(jane_record)

# # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")
# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555
# print(john.days_to_birthday())

# # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# for _, record in book.data.items():
#     print(record)

# iter = book.iterator()
# for i in iter:
#     print(i)

# book.search('ja') # пошук спивпадінь у записах
