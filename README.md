# Talk trends to Google Trends

```sh
docker-compose up -d --build
docker-compose up -d --build --scale worker=3
```

```sh
http://localhost:8004/docs
```

```sh
redis-server /etc/redis/6379.conf
celery -A worker worker --loglevel=INFO
uvicorn main:app --reload
```