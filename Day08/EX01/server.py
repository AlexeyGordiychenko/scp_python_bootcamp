import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, HttpUrl, Field
from uuid import uuid4, UUID
from typing import List, Dict, Literal
from aiohttp import ClientSession, ClientTimeout
import asyncio
import uvicorn

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)-10s%(message)s')


class Task(BaseModel):
    id: UUID
    status: Literal["running", "ready"]
    result: Dict[HttpUrl, int] = Field(default_factory=dict)


class Request(BaseModel):
    urls: List[HttpUrl]


app = FastAPI()
tasks: Dict[UUID, Task] = {}


async def fetch_url(session, url, task_id):
    try:
        async with session.get(str(url), timeout=ClientTimeout(total=5)) as response:
            tasks[task_id]["result"][url] = response.status
    except Exception as e:
        logging.info(f"Error fetching {url}: {str(e)}")
        tasks[task_id]["result"][url] = -1


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

if __name__ == "__main__":
    uvicorn.run(app, port=8888)
