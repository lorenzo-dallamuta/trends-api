from datetime import datetime
import logging
from typing import Optional
from fastapi import FastAPI
from driver import list_topics

date = datetime.now()
logging.basicConfig(
    filename=f'logs/{date.strftime("%m-%d-%Y_%H-%M-%S")}.log',
    encoding='utf-8',
    level=logging.INFO
)


app = FastAPI()


@app.get('/trend/{key}')
def get_trend(
    key: str,
    geo: Optional[str] = None,
    wait: Optional[int] = None,
    full: Optional[bool] = None
):
    args = {
        'key': key,
        'geo': geo,
        'wait': wait,
        'full': full
    }
    args = {k: v for (k, v) in args.items() if v != None}
    topics = list_topics(**args)
    return {'key': key, 'topics': topics}
