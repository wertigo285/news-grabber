from datetime import datetime
from typing import List

from pydantic import AnyHttpUrl, BaseModel


class News(BaseModel):
    date: datetime
    title: str
    desc: str
    link: AnyHttpUrl

    class Config:
        orm_mode = True


class SiteNews(BaseModel):
    site: str
    news: List[News]
