from fastapi import FastAPI
from pydantic import BaseModel
from celery.result import AsyncResult
from worker.tasks import scrape_url


app = FastAPI()

class TaskRequest(BaseModel):
    url: str


@app.post('/tasks/scrape')
def add_request(req: TaskRequest):
    res = scrape_url.delay(req.url)
    return {'task_id': res.task_id}


@app.get('/tasks/get/{task_id}')
def get_task_status(task_id: str):
    task = AsyncResult(task_id)
    response = {'task_id': task_id, 'status': task.status}
    if task.status == 'SUCCESS':
        response['result'] = task.get()
    return response