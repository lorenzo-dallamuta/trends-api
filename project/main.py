from datetime import datetime
import logging
from typing import Optional

from fastapi import FastAPI
from starlette.responses import JSONResponse
from worker import create_query, celery

date = datetime.utcnow()
# TODO: append with datetime prefix
logging.basicConfig(
    filename=f'logs/{date.strftime("%y%m%d_%H%M%S")}.log',
    encoding='utf-8',
    level=logging.INFO
)


app = FastAPI()


@app.post('/trend/{key}')
async def send_trend_query(
    key: str,
    geo: Optional[str] = None,
    wait: Optional[int] = None,
    full: Optional[bool] = None
):
    kwargs = {
        'key': key,
        'geo': geo,
        'wait': wait,
        'full': full
    }
    kwargs = {k: v for (k, v) in kwargs.items() if v != None}
    query = create_query.delay(**kwargs)
    return query.id


@app.get('/trend/')
async def get_trend_result(query_id):
    task_result = celery.AsyncResult(query_id)
    if task_result.status != 'PENDING':
        return JSONResponse(task_result.result)
