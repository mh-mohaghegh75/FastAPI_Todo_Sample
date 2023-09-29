import sys
from fastapi import status, Depends, HTTPException, APIRouter, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
from jose import jwt, JWTError
from starlette.responses import RedirectResponse

from database import get_db
import model

sys.path.append("..")

SECRET_KEY = "firsttry"
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["auth"], responses={401: {"user": "Not Authorized"}})

templates = Jinja2Templates(directory="templates")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
    phone: str
    is_admin: bool


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user = db.query(model.Users).filter(model.Users.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode = {"sub": username, "id": user_id, "exp": expire}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            return None
        return jsonable_encoder({"username": username, "id": user_id})
    except JWTError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")


@router.get("/user")
async def get_all_user(db: Session = Depends(get_db)):
    return db.query(model.Users).all()


@router.post("/create/user", status_code=status.HTTP_201_CREATED)
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = model.Users()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.first_name = create_user.first_name
    create_user_model.last_name = create_user.last_name
    create_user_model.hashed_password = get_password_hash(create_user.password)
    create_user_model.phone = create_user.phone
    create_user_model.is_admin = create_user.is_admin
    create_user_model.is_active = False

    db.add(create_user_model)
    db.commit()
    return db.query(model.Users).all()


@router.post("/token")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return False
        # return JSONResponse(content=jsonable_encoder({"Message": "Uer Not Found"}),
        #                     status_code=status.HTTP_404_NOT_FOUND)
    token_expire = timedelta(minutes=30)
    token = create_access_token(user.username, user.id, expires_delta=token_expire)

    response.set_cookie(key="access_token", value=token, httponly=True)
    return True


@router.get("/", response_class=HTMLResponse)
async def auth_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

        validate_user_cookie = await login_for_access_token(response=response, form_data=form, db=db)

        if not validate_user_cookie:
            msg = "Incorrect Username or Password"
            return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
        return response
    except HTTPException:
        msg = "Unknown Error"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})


@router.get("/logout")
async def logout(request: Request):
    msg = "Logout Successful"
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")
    return response


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})
