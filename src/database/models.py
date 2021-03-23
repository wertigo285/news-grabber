from sqlalchemy import Column, String, Text, DateTime

from .sql import Base, engine


class News(Base):
    __tablename__ = 'news'

    link = Column('link', String, primary_key=True)
    # Для совместимости с базовой реализацией не учитваем tz
    date = Column('date', DateTime)
    site = Column('site', String)
    title = Column('title', String)
    desc = Column('description', Text)


Base.metadata.create_all(bind=engine)
