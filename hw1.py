from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()

tasks = {}

# Создаем модель данных
class Task(BaseModel):
    title: str = Field(..., max_length=50)
    description: str = Field(..., max_length=100)
    completed: Optional[bool] = True # По умолчанию задача выполнена

@app.get("/") # GET запросы используются для получения данных с сервера.
async def root():
    return {"Hello": "World"}


@app.get('/tasks/') # Возвращает список всех задач
async def read_tasks():
    return tasks


@app.get('/tasks/{task_id}') # Возвращает задачу с указанным идентификатором
async def read_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@app.post('/tasks/') # Добавляет новую задачу
async def create_task(task: Task):
    task_id = max(tasks.keys(), default=0) + 1 # Создаем уникальный идентификатор задачи
    tasks[task_id] = task # Добавляем задачу
    return task


@app.put('/tasks/{task_id}') # Обновляет задачу с указанным идентификатором
async def update_task(task_id: int, task: Task):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = task # Обновляем задачу
    return task


@app.delete('/tasks/{task_id}') # Удаляет задачу с указанным идентификатором
async def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    task = tasks[task_id]
    task.completed = False # Помечаем задачу как не выполненную
    tasks[task_id] = task # Обновляем задачу
    return {"detail": "Task deleted"}


'''
Запуск сервера:
uvicorn hw1:app --reload

отправка curl запросов:
Remove-item alias:curl
curl -X 'POST' 'http://127.0.0.1:8000/tasks/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{\"title\": \"Task1\", \"description\": \"Description1\", \"completed\": false}'
curl -X 'POST' 'http://127.0.0.1:8000/tasks/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{\"title\": \"Task2\", \"description\": \"Description2\", \"completed\": false}'
curl -X 'POST' 'http://127.0.0.1:8000/tasks/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{\"title\": \"Task3\", \"description\": \"Description3\", \"completed\": false}'
curl -X 'POST' 'http://127.0.0.1:8000/tasks/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{\"title\": \"Task4\", \"description\": \"Description4\", \"completed\": false}'

INFO:     127.0.0.1:54456 - "GET /tasks/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:54468 - "POST /tasks/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:54469 - "POST /tasks/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:54470 - "POST /tasks/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:54471 - "POST /tasks/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:54472 - "PUT /tasks/3 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54473 - "GET /tasks/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:54475 - "DELETE /tasks/3 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54480 - "GET /tasks/ HTTP/1.1" 200 OK
Список всех задач после добавления 4 задач:
http://127.0.0.1:8000/tasks/
{
  "1": {
    "title": "Task1",
    "description": "Description1",
    "completed": true
  },
  "2": {
    "title": "Task2",
    "description": "Description2",
    "completed": true
  },
  "3": {
    "title": "Task5",
    "description": "Description5",
    "completed": false
  },
  "4": {
    "title": "Task4",
    "description": "Description4",
    "completed": true
  }
}
'''


