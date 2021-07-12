from typing import Optional
from fastapi import FastAPI
from starlette.responses import JSONResponse
from worker import create_query
from celery.result import AsyncResult

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
    task_result = AsyncResult(query_id)
    if task_result.status != 'PENDING':
        return JSONResponse(task_result.result)
    return task_result.status
