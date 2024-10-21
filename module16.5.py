from fastapi import FastAPI, HTTPException, Body, Request
from fastapi.responses import HTMLResponse
from starlette import status
from typing import List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")
users = {}


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "users.html",
        {"request": request, "users": users.values()}
    )


@app.get("/users")
async def get_users():
    return users


@app.post("/user/{username}/{age}")
async def create_user(request: Request, username: str, age: int):
    next_id = str(int(max(users.keys(), default="0")) + 1)
    users[next_id] = {"id": int(next_id), "username": username, "age": age}
    return templates.TemplateResponse(
        "users.html",
        {"request": request, "users": users.values()}
    )


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: str, username: str, age: int):
    if user_id in users:
        users[user_id] = {"id": int(user_id), "username": username, "age": age}
        return f"The user {user_id} is updated"
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: str):
    if user_id in users:
        users.pop(user_id)
        return f"The user {user_id} has been deleted"
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@app.get("/user/{user_id}")
async def get_user(request: Request, user_id: int):
    user = users.get(str(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return templates.TemplateResponse(
        "user.html",
        {"request": request, "user": user}
    )
