import sys
from typing import Optional
from fastapi import HTTPException, status, Form, Depends, APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID
import model
from database import db_engine, get_db
from sqlalchemy.orm import Session
from routers.auth import get_current_user
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

sys.path.append("..")

router = APIRouter(prefix="/todos", tags=["todos"], responses={404: {"user": "Not Found"}})

templates = Jinja2Templates(directory="templates")

BOOKS = []


class Todo(BaseModel):
    title: str
    description: str
    priority: int = Field(gt=0, lt=6)
    complete: bool


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str]
    rating: int = Field(gt=-1, lt=101)


class DirectionName(str, Enum):
    north = "North"
    south = "South"
    west = "West"
    east = "East"


@router.get("/test")
async def test(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# Migration api
@router.get("/createdb")
async def create_database():
    model.Base.metadata.create_all(bind=db_engine)
    return {"Database": "Created"}


@router.get("/todo")
async def read_all(db: Session = Depends(get_db)):
    return db.query(model.Todos).all()


@router.get("/todo/user")
async def read_all_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"user not found"})
    return db.query(model.Todos).filter(model.Todos.user_id == user.get("id")).all()


@router.get("/todo/{id}")
async def read_todo_by_id(user_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"user not found"})
    todo_model = db.query(model.Todos).filter(model.Todos.id == user_id).filter(
        model.Todos.user_id == user.get("id")).first()
    if todo_model is not None:
        return todo_model
    else:
        return JSONResponse(content=jsonable_encoder({"Message": "Item Not Found"}), status_code=404)


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: Todo, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"user not found"})
    todo_model = model.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.user_id = user.get("id")

    db.add(todo_model)
    db.commit()
    return db.query(model.Todos).all()


@router.put("/todo/{id}", status_code=status.HTTP_201_CREATED)
async def update_todo(id: int, todo: Todo, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    todo_model = db.query(model.Todos).filter(model.Todos.id == id).filter(
        model.Todos.user_id == user.get("id")).first()
    if todo_model is None:
        return JSONResponse(content=jsonable_encoder({"Message": "Item Not Found"}), status_code=404)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"user not found"})

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    return db.query(model.Todos).filter(model.Todos.id == id).first()


@router.delete("/todo/{id}")
async def delete_todo(user_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    todo_model = db.query(model.Todos).filter(model.Todos.id == user_id).filter(
        model.Todos.user_id == user.get("id")).first()
    if todo_model is None:
        return JSONResponse(content=jsonable_encoder({"Message": "Item Not Found"}), status_code=404)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"user not found"})

    db.delete(todo_model)
    db.commit()
    return JSONResponse(content=jsonable_encoder({"Message": "Item deleted successfully"}),
                        status_code=status.HTTP_200_OK)


###########################################

@router.get("/hello")
async def hello():
    return {"Message": "Hello mama "}


@router.get("/")
async def get_all_books():
    return BOOKS


@router.get("/book/{book_id}")
async def get_by_id(book_id: UUID):
    i = []
    for x in BOOKS:
        if x.id == book_id:
            i.append(x)
    if len(i) != 0:
        return i
    else:
        raise HTTPException(status_code=404, detail="file not exist")


@router.get("/books")
async def get_all_books(book_title: Optional[str]):
    return {"book_title": BOOKS[book_title]}


@router.get("/books/{book_title}")
async def get_a_book(book_title: str):
    return {"book_title": BOOKS[book_title]}


@router.get("/direction/{direction_name}")
async def get_direction(direction_name: str):
    if direction_name == DirectionName.north:
        return {"Direction": direction_name}
    elif direction_name == DirectionName.south:
        return {"Direction": direction_name}
    elif direction_name == DirectionName.west:
        return {"Direction": direction_name}
    elif direction_name == DirectionName.east:
        return {"Direction": direction_name}
    else:
        return {"Message": "Direction is not valid"}


@router.delete("/books")
async def create_book(book_name: str):
    del BOOKS[book_name]
    return BOOKS


@router.post("/books/login")
async def book_login(username: str = Form(), password: str = Form()):
    response = jsonable_encoder({"username": username, "password": password})
    return response


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    j = jsonable_encoder(book)
    return JSONResponse(content=j, status_code=201)
