# news-grabber
Граббер новостей разработанный по заданию [TASK.md](https://github.com/wertigo285/news-grabber/blob/main/TASK.md)

# Запуск

Для запуска необходимо клонировать репозиторий
```
git clone https://github.com/wertigo285/news-grabber.git
```
Создать виртуальное окружение, активировать его и установить зависимости
```
python -m venv venv
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Для проверки работы выполнить команду
```
python test_graber.py
```
Для каждого нового сайта скрипт выведет в консоль 3 новости из RSS ленты и первую новость из RSS ленты с сайта.

# Добавление нового сайта
В файле graber/graber.py в глобальную переменную SITES добавить описание параметров парсинга сайта в виде словаря со структурой
```
    - name : имя сайта
    - rss_url: адрес RSS
    - art_parser_config: словарь с параметрами для парсера страниц новости
        Формат масок : ['тэг', {'аттрибут':'значение', ...}]
        - article_mask: маска враппера статьи
        - title_mask: маска враппера заголовка
        - image_mask: маска враппера изображения
        - text_mask: маска враппера текста статьи,
                     пустое значение если враппера нет
        - parag_mask: маска враппера параграфа статьи
```

Пример для ria.ru
```
{'name': 'ria',
     'rss_url': 'https://ria.ru/export/rss2/archive/index.xml',
     'art_parser_config': {
         'article_mask': ['div', {'class': 'layout-article__main'}],
         'title_mask': ['h1', {'class': 'article__title'}],
         'image_mask': ['img'],
         'text_mask': ['div', {'class': 'article__body'}],
         'parag_mask': ['div', {'class': 'article__block',
                                'data-type': 'text'}]
     }
     }
```