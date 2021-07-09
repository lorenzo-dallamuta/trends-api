from datetime import datetime
import logging

from typing import Optional
from fastapi import FastAPI
from celery.result import AsyncResult
from starlette.responses import JSONResponse

from worker import create_query

date = datetime.now()
logging.basicConfig(
    filename=f'logs/{date.strftime("%y%m%d_%H%M%S")}.log',
    encoding='utf-8',
    level=logging.INFO
)
# TODO: set the log folder to hold a maximum number of files


app = FastAPI()


@app.post('/trend/{key}')
def send_trend_query(
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
    kwargs = {k: v for (k, v) in args.items() if v != None}
    query = create_query.delay(**kwargs)
    # return {'key': key, 'topics': topics}
    return query.id


@app.get('/trend/{key}')
def get_trend_result(query_id):
    task_result = AsyncResult(query_id)
    return JSONResponse(task_result)
