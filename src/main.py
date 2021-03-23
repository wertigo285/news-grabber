from typing import List

from fastapi import FastAPI

from fastapi_utils.tasks import repeat_every

from .schemas import SiteNews
from .database import Base
from .grabbing import fill_news


app = FastAPI()

base = Base()


@app.get("/news/", response_model=List[SiteNews])
def show_statistic():
    return base.show()


@app.on_event("startup")
@repeat_every(seconds=60)
def fill_news_task():
    fill_news(base)
