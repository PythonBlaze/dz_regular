import csv
import re
from pprint import pprint

# читаем адресную книгу в формате CSV в список contact_list
with open("phonebook_raw.csv", 'r', encoding='utf8') as f:
    row = csv.reader(f, delimiter=',')
    contact_list = list(row)

def format_fio(contact):  # функция для последующего цикла, выводит нам первые 3 слова без лишних пробелов
    fio_parts = contact[:3]  # первые три слова являются частями ФИО
    fio_split = " ".join(fio_parts).split(" ")  # очищаем от лишних пробелов
    return fio_split[:3]

# Шаг 2: Приведение телефонов к нужному формату
def format_phone(phone):
    phone_pattern = re.compile(
        r'(\+?\d{1,3}\s?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2})\s*\(?(?:\s*(?:доб\.?)\s*(\d+))?\)?')
    match = phone_pattern.match(phone)
    if match:
        # Извлекаем номер телефона
        phone_number = match.group(1)  # Это весь номер телефона
        # Проверяем, есть ли добавочный номер
        extension = match.group(2) if match.group(2) else ''

        # Разбиваем номер телефона на части
        phone_parts = re.sub(r'\D', '', phone_number)  # Убираем все нецифровые символы
        if len(phone_parts) == 11:  # Если номер состоит из 11 цифр
            formatted_phone = f"+7({phone_parts[1:4]}){phone_parts[4:7]}-{phone_parts[7:9]}-{phone_parts[9:11]}"
        else:
            formatted_phone = phone_number  # Если формат не соответствует, возвращаем оригинальный номер

        if extension:
            formatted_phone += f" доб.{extension}"
        return formatted_phone
    return phone

# Шаг 3: Объединение дублирующихся записей
def merge_contacts(contacts):
    merged_contacts = {}
    for contact in contacts:
        fio = format_fio(contact)
        key = (fio[0], fio[1])  # Ключ по Фамилии и Имени
        if key not in merged_contacts:
            merged_contacts[key] = contact
        else:
            # Объединяем данные
            for i in range(3, len(contact)):
                if merged_contacts[key][i] == '' and contact[i]:
                    merged_contacts[key][i] = contact[i]
    return list(merged_contacts.values())

# Приводим записи к правильному формату и объединяем
for index, contact in enumerate(contact_list):
    contact_list[index][:3] = format_fio(contact)  # Форматируем ФИО
    contact_list[index][5] = format_phone(contact[5])  # Форматируем телефон

# Объединяем дубликаты
contact_list = merge_contacts(contact_list)

# Сохраняем получившиеся данные в другой файл
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contact_list)

# Для проверки результата
pprint(contact_list)
