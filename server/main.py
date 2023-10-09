from fastapi import FastAPI
from routers import auth, todos
from company import companies
from starlette.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(companies.router, prefix="/company", tags=["company"])
