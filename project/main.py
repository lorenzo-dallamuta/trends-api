from fastapi import FastAPI

app = FastAPI()

@app.get('/trend/{key}')
def get_trend(key:str):
    return {'key':key}