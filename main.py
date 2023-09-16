from fastapi import FastAPI
from routers import auth, todos, address
from company import companies

app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(companies.router, prefix="/company", tags=["company"])
app.include_router(address.router)
