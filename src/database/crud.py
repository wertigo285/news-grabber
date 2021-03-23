from datetime import datetime
from typing import List
from itertools import groupby

from sqlalchemy import func

from . import models
from ..schemas import News, SiteNews
from .sql import SessionLocal


class Base:

    def __init__(self):
        self._session = SessionLocal()

    def add(self, site, newses: List[News]):
        for news in newses:
            date = datetime.strptime(news['published'], '%d.%m.%Y %H:%M')
            db_record = models.News(
                site=site, date=date, title=news['title'],
                desc=news['desc'], link=news['link']
            )
            self._session.merge(db_record)
        self._session.commit()

    def get_last_news_date(self, site):
        results = self._session.query(
            func.max(models.News.date).label('last_date')
        ).group_by(models.News.site).filter(models.News.site == site).all()
        return results[0].last_date if results else None

    def show(self):
        # Выбераем по 3 последние новости для каждого сайта
        subquery = self._session.query(
            models.News.link,
            func.rank().over(
                order_by=models.News.date.desc(),
                partition_by=models.News.site
            ).label('rank')
        ).subquery()
        links = self._session.query(subquery).filter(
            subquery.c.rank <= 3).all()
        # Составляем список новостей
        links = [link.link for link in links]
        # Получаем новости
        newses = self._session.query(
            models.News).filter(
                models.News.link.in_(links)
        ).order_by('site', 'date').all()
        result = []
        # Групперуем результат
        for site, entries in groupby(newses, key=lambda x: getattr(x, 'site')):
            result.append(SiteNews(site=site, news=list(entries)))
        return result
