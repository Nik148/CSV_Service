

load_csv_description = "Загрузка файла csv. Имена файла у одного пользователя не должны повторяться"

delete_csv_description = "Удаление файла csv"

my_csv_description = "Информация о ваших csv файлах"

query_csv_description = """
Получение данных из csv файла с возможностью редактирования\n
column - список, состоящий из колонок файла, которые нужно вернуть\n
filter - фильтры, которые мы хотим применить.\n 
При одном фильтре структура такая:\n
"filter": {\n
        "compare":{\n
            "column_name": "name",\n
            "filter": "EQUALS",\n
            "value": "Robert"\n
        }
        
При нескольких фильтрах добавляются операторы 'and' или 'or':\n
"filter": {\n
        "and": 
            [\n
                {"or":\n
                    [\n
                        {"compare":{\n
                            "column_name": "name",\n
                            "filter": "EQUALS",\n
                            "value": "Robert"\n
                            }\n
                        },\n
                        {"compare":{\n
                            "column_name": "age",\n
                            "filter": "GREATER_THAN_EQUALS",\n
                            "value": 40\n
                            }\n
                        },\n 
                    ]\n
                },\n
                {"compare":{\n
                    "column_name": "salary",\n
                    "filter": "LESS_THAN",\n
                    "value": 20000\n
                    }\n   
                }\n 
            ]\n
    }\n
Верхнее выражение эквивалентно: (name=="Robert" or age>=40) and salary<20000\n
В объектах "and" или "or" длина списка должна равняться 2 и вложенность может быть любой.\n
Операторы сравнения:\n
    "EQUALS": ==\n
    "NOT_EQUALS": !=\n
    "GREATER_THAN": >\n
    "GREATER_THAN_EQUALS": >=\n
    "LESS_THAN": <\n
    "LESS_THAN_EQUALS": <=\n
sorted - Строки, которые нужно отсортировать. Название колонок обязательно должны
присутствоать в column\n
    "ASC": От низких значений к высоким\n
    "DESC": От высоких значений к низким\n
"""