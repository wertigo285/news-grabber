from bs4 import BeautifulSoup
from datetime import datetime
from xml.etree.ElementTree import ElementTree as ET
from urllib.request import urlopen
from urllib.parse import urljoin

'''
Список сайтов и параметов.
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

Для примера добавлен сайт ria.ru
'''
SITES = [
    {'name': 'lenta',
     'rss_url': 'https://lenta.ru/rss/',
     'art_parser_config': {
         'article_mask': ['div', {'class': 'b-topic__content'}],
         'title_mask': ['h1', {'itemprop': 'headline'}],
         'image_mask': ['img'],
         'text_mask': ['div', {'itemprop': 'articleBody'}],
         'parag_mask': ['p']
     }
     },
    {'name': 'interfax',
     'rss_url': 'https://www.interfax.ru/rss.asp',
     'art_parser_config': {
         'article_mask': ['article', {'itemprop': 'articleBody'}],
         'title_mask': ['h1', {'itemprop': 'headline'}],
         'image_mask': ['img', {'itemprop': 'image'}],
         'text_mask': [],
         'parag_mask': ['p']
     }
     },
    {'name': 'm24',
     'rss_url': 'https://www.m24.ru/rss.xml',
     'art_parser_config': {
         'article_mask': ['div', {'class': 'b-material-body'}],
         'title_mask': ['h1'],
         'image_mask': ['img'],
         'text_mask': [],
         'parag_mask': ['p', {'class': None}]
     }
     },
    {'name': 'kommersant',
     'rss_url': 'http://www.kommersant.ru/RSS/news.xml',
     'art_parser_config': {
         'article_mask': ['article', {'class': 'lenta__item'}],
         'title_mask': ['h1', {'class': 'article_name'}],
         'image_mask': ['img', {'class': 'fallback_image'}],
         'text_mask': ['div', {'class': 'article_text_wrapper'}],
         'parag_mask': ['p', {'class': 'b-article__text'}]
     }
     },
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
]


class ArticleParser:
    '''
    Парсер статьи с сайта
    '''
    config_keys = ['article_mask', 'title_mask',
                   'image_mask', 'text_mask', 'parag_mask']

    def __init__(self, config):
        for key in self.config_keys:
            setattr(self, key, config[key])

    def grub(self, url):
        '''
        Получить новость с сайта
        '''
        base_url = self._get_base_url(url)    
        soup = self._get_soup(url)
        article = soup.find(*self.article_mask) or soup
        title = self._get_title(soup)
        image = self._get_image(article, base_url)
        content = self._get_content(article)
        return {'title': title, 'image': image, 'content': content}

    def _get_title(self, soup):
        return soup.find(*self.title_mask).getText()

    def _get_image(self, soup, base_url):
        image = soup.find(*self.image_mask)
        image = image['src'] if image else None
        if image and base_url not in image:
            image = urljoin(base_url, image)
        return image

    def _get_content(self, soup):
        text_block = soup.find(*self.text_mask) if self.text_mask else soup
        content = [string.getText().strip()
                   for string in text_block.find_all(*self.parag_mask)
                   if string.getText().strip()]
        return content

    @staticmethod
    def _get_soup(url):
        with urlopen(url) as page:
            soup = BeautifulSoup(page, 'html.parser')
        return soup
    
    @staticmethod
    def _get_base_url(url):
        external_level = url.count('/') - 2
        return urljoin(url, '.' * external_level)



class RSSParser:
    '''
    Парсер RSS сайта
    '''
    # Формат вывода новости
    article_struct = {
        'title': 'title',
        'link': 'link',
        'description': 'desc',
        'pubDate': 'published'
    }

    def __init__(self, config):
        self.rss_url = config['rss_url']
        self.in_date_format = '%a, %d %b %Y %H:%M:%S %z'
        self.out_date_format = '%d.%m.%Y %H:%M'

    def news(self, limit=0, **kwargs):
        '''
        Получить список новостей RSS
        '''
        news = []
        start_date = kwargs.get('start_date', None)
        end_date = kwargs.get('end_date', None)
        with urlopen(self.rss_url) as rss:
            tree = ET(file=rss)
            root = tree.getroot()
            for num, item in enumerate(root.iter('item'), 1):
                article = {item.tag: item.text for item in list(item)}
                article = self.__transform_article(article)
                date = self.__get_date(article['published'])
                # Фильтр по дате
                if (start_date and date < start_date
                    or end_date and date > end_date):
                    continue
                article['published'] = self.__format_date(date)
                news.append(article)
                # Фильтр по лимиту записей
                if limit and num >= limit:
                    break
        return news

    def __transform_article(self, article):
        result = {}
        for raw_tag, tag in self.article_struct.items():
            result[tag] = article[raw_tag].strip()
        return result

    def __get_date(self, date_str):
        return datetime.strptime(date_str, self.in_date_format)
        
    def __format_date(self, date):    
        return date.strftime(self.out_date_format)


class Site:
    '''
   Класс-интерфейс для получения данных с сайта
    '''
    def __init__(self, config):
        self.__rss_parser = RSSParser(config)
        self.__article_parser = ArticleParser(config['art_parser_config'])

    def news(self, limit=0):
        '''
        Получить список новостей RSS
        '''
        return self.__rss_parser.news(limit)

    def grub(self, url):
        '''
        Получить новость с сайта
        '''
        return self.__article_parser.grub(url)


class Graber:
    '''
    Класс-интерфейс для получения данных с сайтов
    '''
    def __init__(self):
        for site in SITES:
            setattr(self, site['name'], Site(site))
