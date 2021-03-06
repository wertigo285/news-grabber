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
## Запуск и проверка базового решения

Для проверки работы выполнить команду
```
python test_graber.py
```
Для каждого нового сайта скрипт выведет в консоль 3 новости из RSS ленты и первую новость из RSS ленты с сайта.

Правила и алгоритмы находятся в файле [graber/graber.py](https://github.com/wertigo285/news-grabber/blob/main/graber/graber.py)

## Запуск на FastAPI

После старта проекта, раз в минуту, фоновое задание загружает в БД новости из RSS каналов настроенных сайтов.
### Docker
Для запуска в Docker можно загрузить построенный контейнер и запустить его:
```
docker pull skhortyuk/news-grabber
...
docker run -it -p 8000:8000 skhortyuk/news-grabber
```

Или построить и запустить выполнив команды в папке клонированного репозитория:
```
docker build -t news-grabber .
...
docker run -it -p 8000:8000 news-grabber
```


После запуска контейнера сервис будет доступен по адресу 127.0.0.1:8000
### Локально

Для запуска бэкенда в папке репозитория выполнить команду
```
uvicorn src.main:app --host 0.0.0.0 --port 8000
```
Проект будет доступен по адресу 127.0.0.1:8000

### Описание эндпоинтов

**/news/** - выдает по 3 последние сгруппированные новости для каждого настроенного сайта

Пример:
```
http://127.0.0.1:8000/news/
```
Результат:
```
[
  {
    "site": "interfax",
    "news": [
      {
        "date": "2021-03-23T22:06:00",
        "title": "ХК \"Локомотив\" сравнял счет в четвертьфинальной серии плей-офф с ЦСКА",
        "desc": "Хоккеисты московского ЦСКА на выезде проиграли соперникам из ярославского \"Локомотива\" в четвертом матче серии 1/4 финала Кубка Гагарина.",
        "link": "https://www.sport-interfax.ru/757469"
      },
      {
        "date": "2021-03-23T22:38:00",
        "title": "Карантин в Нидерландах продлен на месяц",
        "desc": "Общенациональный карантин в Нидерландах продлен по решению правительства до 20 апреля, сообщил во вторник на пресс-конференции премьер-министр Марк Рютте.",
        "link": "https://www.interfax.ru/world/757471"
      },
      {
        "date": "2021-03-23T22:42:00",
        "title": "В РФ осталось 130 тыс. свободных коек для больных COVID-19",
        "desc": "В России на данный момент свободно 130 тысяч \"ковидных\" коек, сообщила вице-премьер РФ Татьяна Голикова.",
        "link": "https://www.interfax.ru/russia/757470"
      }
    ]
  },
  {
    "site": "kommersant",
    "news": [...]
  },
  ...
  }
```



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

# Использованные технологии

* [Python 3.8](https://www.python.org/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy ORM](https://www.sqlalchemy.org/)
* [SQLite](https://www.sqlite.org/)
