from fastapi import APIRouter, HTTPException
from app.schemas import Task, TaskCreate
from app.storage import tasks, task_id_counter, users

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=Task)
def create_task(task: TaskCreate, user_id: int):
    global task_id_counter

    if not any(u["id"] == user_id for u in users):
        raise HTTPException(status_code=404, detail="User not found")

    new_task = {
        "id": task_id_counter,
        "title": task.title,
        "is_completed": False,
        "user_id": user_id
    }

    tasks.append(new_task)
    task_id_counter += 1
    return new_task

@router.get("/", response_model=list[Task])
def list_tasks():
    return tasks

@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, is_completed: bool):
    for task in tasks:
        if task["id"] == task_id:
            task["is_completed"] = is_completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Task not found")