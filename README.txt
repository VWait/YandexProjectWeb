нужно сделать:
1)бд items: id, type, halls_id(внешний ключ), top, left, width, height
2)бд halls: id, name, top, left, width, height

3)Подключить в main.py:
3.1)/login
3.2)/registration
3.3)/map вот тут алгоритм надо написать, который преобразует данные из бд в следующее:
3.3.1)список классов Hall со св-ми name, top, left, width, height, items
3.3.2)св-во items содержит список классов Item со св-ми type, top, left, width, height

P.S. С организацией бд я могу быть не прав и можешь найти решение лучше, потому что это первое, что в голову пришло. Главное, чтобы
сработали вложенные циклы в файле map.html, изучи перед началом
