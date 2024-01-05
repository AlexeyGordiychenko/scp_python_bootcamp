import logging
from os import getenv
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, HttpUrl, Field
from uuid import uuid4, UUID
from typing import List, Dict, Literal
from aiohttp import ClientSession, ClientTimeout
import asyncio
import uvicorn
import aioredis
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

try:
    CACHE_CLEANUP_TIMEOUT = int(getenv("CACHE_CLEANUP_TIMEOUT", 60))
except (TypeError, ValueError):
    CACHE_CLEANUP_TIMEOUT = 60
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)-10s%(message)s')


class Task(BaseModel):
    id: UUID
    status: Literal["running", "ready"]
    result: Dict[HttpUrl, int] = Field(default_factory=dict)


class Domain(BaseModel):
    domain: str
    count: int


class Request(BaseModel):
    urls: List[HttpUrl]


redis = None


async def lifespan(app: FastAPI):
    global redis
    redis = await aioredis.Redis.from_url('redis://localhost')
    try:
        await redis.ping()
    except aioredis.ConnectionError as e:
        logging.error(f"Couldn't connect to Redis")
        redis = None
    if redis:
        asyncio.ensure_future(cleanup_cache(CACHE_CLEANUP_TIMEOUT))
    yield
    if redis:
        await redis.close()


app = FastAPI(lifespan=lifespan)
tasks: Dict[UUID, Task] = {}


async def fetch_url(session, url, task_id):
    url_str = str(url)
    cached_status = None
    if redis:
        await redis.incr(urlparse(url_str).netloc)
        cached_status = await redis.get(url_str)
    if cached_status is not None:
        tasks[task_id]["result"][url] = cached_status
    else:
        try:
            async with session.get(str(url), timeout=ClientTimeout(total=5)) as response:
                tasks[task_id]["result"][url] = response.status
                if redis:
                    await redis.set(url_str, response.status)
        except Exception as e:
            logging.info(f"Error fetching {url}: {str(e)}")
            tasks[task_id]["result"][url] = -1


async def cleanup_cache(interval: int):
    while True:
        await asyncio.sleep(interval)
        logging.info('Cleaning up cache...')
        cursor = b'0'
        while cursor:
            cursor, keys = await redis.scan(cursor, match='http*')
            if keys:
                await redis.delete(*keys)


async def fetch_all_urls(urls: List[HttpUrl], task_id: UUID):
    async with ClientSession() as session:
        workers = []
        for url in urls:
            workers.append(asyncio.ensure_future(
                fetch_url(session, url, task_id)))
        await asyncio.gather(*workers)

    tasks[task_id]["status"] = "ready"


@app.post("/api/v1/tasks/", response_model=Task, status_code=201)
async def create_task(request: Request, background_tasks: BackgroundTasks):
    task_id = uuid4()
    task = Task(id=task_id, status="running")
    tasks[task_id] = task.model_dump()
    background_tasks.add_task(fetch_all_urls, request.urls, task_id)

    return task


@app.get("/api/v1/tasks/{task_id}", response_model=Task)
async def read_task(task_id: UUID):
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/api/v1/domains/", response_model=List[Domain])
async def read_domains():
    if not redis:
        raise HTTPException(status_code=503, detail="Redis not available")
    cursor = b'0'
    all_keys = []
    all_values = []

    while cursor:
        cursor, keys = await redis.scan(cursor, match='[^http]*')
        values = await redis.mget(keys=keys)

        all_keys.extend(keys)
        all_values.extend(values)

    return [Domain(domain=key.decode('utf-8'), count=value.decode('utf-8')) for key, value in zip(all_keys, all_values)]


if __name__ == "__main__":
    uvicorn.run(app, port=8888)
